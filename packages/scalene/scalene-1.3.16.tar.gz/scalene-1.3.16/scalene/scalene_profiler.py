"""Scalene: a scripting-language aware profiler for Python.

    https://github.com/plasma-umass/scalene

    See the paper "docs/scalene-paper.pdf" in this repository for technical
    details on an earlier version of Scalene's design; note that a
    number of these details have changed.

    by Emery Berger
    https://emeryberger.com

    usage: scalene test/testme.py
    usage help: scalene --help

"""
import argparse
import atexit
import builtins
import contextlib
import functools
import gc
import inspect
import json
import math
import multiprocessing
import pathlib
import os
import random
import re
import resource
import signal
import stat
import sys
import tempfile
import threading
import time
import traceback

from collections import defaultdict
from functools import lru_cache
from signal import Handlers, Signals
from types import FrameType
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)

from scalene.scalene_arguments import ScaleneArguments
from scalene.scalene_funcutils import ScaleneFuncUtils
from scalene.scalene_json import ScaleneJSON
from scalene.scalene_mapfile import ScaleneMapFile
from scalene.scalene_statistics import (
    Address,
    ByteCodeIndex,
    Filename,
    LineNumber,
    ScaleneStatistics,
)
from scalene.scalene_output import ScaleneOutput
from scalene.scalene_preload import ScalenePreload
from scalene.scalene_signals import ScaleneSignals
from scalene.scalene_gpu import ScaleneGPU
from scalene.scalene_parseargs import ScaleneParseArgs, StopJupyterExecution
from scalene.scalene_sigqueue import ScaleneSigQueue


def require_python(version: Tuple[int, int]) -> None:
    assert (
        sys.version_info >= version
    ), f"Scalene requires Python version {version[0]}.{version[1]} or above."


require_python((3, 7) if sys.platform != "win32" else (3, 8))


# Scalene fully supports Unix-like operating systems; in
# particular, Linux, Mac OS X, and WSL 2 (Windows Subsystem for Linux 2 = Ubuntu).
# It also has partial support for Windows.

# Install our profile decorator.


def scalene_redirect_profile(func: Any) -> Any:
    return Scalene.profile(func)


builtins.profile = scalene_redirect_profile  # type: ignore


def start() -> None:
    Scalene.start()


def stop() -> None:
    Scalene.stop()


class Scalene:
    """The Scalene profiler itself."""

    # Debugging flag, for internal use only.
    __debug: bool = False
    # Whether the current profiler is a child
    __is_child = -1
    # the pid of the primary profiler
    __parent_pid = -1

    __last_profiled: Tuple[Filename, LineNumber] = (
        Filename("NADA"),
        LineNumber(0),
    )
    __last_profiled_invalidated: bool = False

    # Support for @profile
    # decorated files
    __files_to_profile: Dict[Filename, bool] = defaultdict(bool)
    # decorated functions
    __functions_to_profile: Dict[Filename, Dict[Any, bool]] = defaultdict(
        lambda: {}
    )

    # Cache the original thread join function, which we replace with our own version.
    __original_thread_join = threading.Thread.join

    # As above; we'll cache the original thread and replace it.
    __original_lock = threading.Lock

    __args = ScaleneArguments()
    __signals = ScaleneSignals()
    __stats = ScaleneStatistics()
    __output = ScaleneOutput()
    __json = ScaleneJSON()
    __gpu = ScaleneGPU()

    __output.gpu = __gpu.has_gpu()
    __json.gpu = __gpu.has_gpu()

    @staticmethod
    def get_original_lock() -> threading.Lock:
        return Scalene.__original_lock()

    # Likely names for the Python interpreter.
    __all_python_names = [
        os.path.basename(sys.executable),
        os.path.basename(sys.executable) + str(sys.version_info.major),
        os.path.basename(sys.executable)
        + str(sys.version_info.major)
        + "."
        + str(sys.version_info.minor),
    ]

    # last num seconds between interrupts for CPU sampling.
    __last_cpu_sampling_rate: float = 0

    # when did we last receive a signal?
    __last_signal_time_virtual: float = 0
    __last_signal_time_wallclock: float = 0
    __last_signal_time_sys: float = 0
    __last_signal_time_user: float = 0

    # path for the program being profiled
    __program_path: str = ""
    # temporary directory to hold aliases to Python

    __python_alias_dir: pathlib.Path

    # Profile output parameters

    # when we output the next profile
    __next_output_time: float = float("inf")
    # pid for tracking child processes
    __pid: int = 0

    __malloc_mapfile: ScaleneMapFile
    __memcpy_mapfile: ScaleneMapFile

    # Program-specific information:
    #   the name of the program being profiled
    __program_being_profiled = Filename("")

    # Is the thread sleeping? (We use this to properly attribute CPU time.)
    __is_thread_sleeping: Dict[int, bool] = defaultdict(
        bool
    )  # False by default
    __child_pids: Set[int] = set()

    # Signal queues for CPU timers, allocations, and memcpy
    __cpu_sigq: ScaleneSigQueue[Any]
    __alloc_sigq: ScaleneSigQueue[Any]
    __memcpy_sigq: ScaleneSigQueue[Any]
    __sigqueues: List[ScaleneSigQueue[Any]]

    @staticmethod
    def interruption_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
    ) -> None:
        raise KeyboardInterrupt

    @staticmethod
    def invalidate_lines(frame: FrameType, _event: str, _arg: str) -> Any:
        # Mark the last_profiled information as invalid as soon as we execute a different line of code.
        # FIXME this only correctly supports single-threaded programs at the moment.
        if (
            False
        ):  # for testing purposes only - if true, measure overhead when on all the time.
            try:
                return Scalene.invalidate_lines
            except:
                return None
        try:
            # Stop tracing when we've invalidated or when we're done profiling.
            # This needs to be inside the try-except because during shutdown,
            # the members of Scalene disappear.
            if Scalene.__last_profiled_invalidated or Scalene.__done:
                sys.settrace(None)
                return None
        except:
            sys.settrace(None)
            return None
        f = frame
        if f.f_code.co_filename and (f.f_code.co_filename[0] == "<" or "scalene" in f.f_code.co_filename):
            # Don't trace this scope, since it is executing inside of Scalene or Python internals.
            f.f_trace_lines = False
            return None
        if Scalene.__last_profiled != (f.f_code.co_filename, f.f_lineno):
            # We've executed a different line. Mark this as
            # invalidated and stop tracing IF we aren't still executing
            # the last-profiled line at a higher scope.
            while f:
                if (f.f_code.co_filename, f.f_lineno) == Scalene.__last_profiled:
                    # Still on the stack; keep tracing.
                    return Scalene.invalidate_lines
                f = cast(FrameType, f.f_back)
            # Not on the stack anywhere - we are done tracing.
            Scalene.__last_profiled_invalidated = True
            sys.settrace(None)
            return None
        return Scalene.invalidate_lines

    @classmethod
    def clear_metrics(cls) -> None:
        """
        Clears the various states so that each forked process
        can start with a clean slate
        """
        cls.__stats.clear()
        cls.__child_pids.clear()

    @classmethod
    def add_child_pid(cls, pid: int) -> None:
        cls.__child_pids.add(pid)

    @classmethod
    def remove_child_pid(cls, pid: int) -> None:
        cls.__child_pids.remove(pid)

    # Replacement @profile decorator function.
    # We track which functions - in which files - have been decorated,
    # and only report stats for those.
    @staticmethod
    def profile(func: Any) -> Any:
        # Record the file and function name
        Scalene.__files_to_profile[func.__code__.co_filename] = True
        Scalene.__functions_to_profile[func.__code__.co_filename][func] = True

        @functools.wraps(func)
        def wrapper_profile(*args: Any, **kwargs: Any) -> Any:
            value = func(*args, **kwargs)
            return value

        return wrapper_profile

    @staticmethod
    def shim(func: Callable[[Any], Any]) -> Any:
        """
        Provides a decorator that, when used, calls the wrapped function with the Scalene type

        Wrapped function must be of type (s: Scalene) -> Any

        This decorator allows for marking a function in a separate file as a drop-in replacement for an existing
        library function. The intention is for these functions to replace a function that indefinitely blocks (which
        interferes with Scalene) with a function that awakens periodically to allow for signals to be delivered
        """
        func(Scalene)
        # Returns the function itself to the calling file for the sake
        # of not displaying unusual errors if someone attempts to call
        # it
        @functools.wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)  # type: ignore

        return wrapped

    @staticmethod
    def cleanup_files() -> None:
        Scalene.__malloc_mapfile.cleanup()
        Scalene.__memcpy_mapfile.cleanup()

    @staticmethod
    def set_thread_sleeping(tid: int) -> None:
        Scalene.__is_thread_sleeping[tid] = True

    @staticmethod
    def reset_thread_sleeping(tid: int) -> None:
        Scalene.__is_thread_sleeping[tid] = False

    timer_signals = True

    @staticmethod
    def windows_timer_loop() -> None:
        """For Windows, send periodic timer signals; launch as a background thread."""
        Scalene.timer_signals = True
        while Scalene.timer_signals:
            time.sleep(Scalene.__args.cpu_sampling_rate)
            signal.raise_signal(Scalene.__signals.cpu_signal)

    @staticmethod
    def start_signal_queues() -> None:
        """Starts the signal processing queues (i.e., their threads)"""
        for sigq in Scalene.__sigqueues:
            sigq.start()

    @staticmethod
    def stop_signal_queues() -> None:
        """Stops the signal processing queues (i.e., their threads)"""
        for sigq in Scalene.__sigqueues:
            sigq.stop()

    @staticmethod
    def malloc_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
    ) -> None:
        Scalene.__alloc_sigq.put((signum, this_frame))
        del this_frame
        if not Scalene.__last_profiled_invalidated:  # and not sys.gettrace():
            sys.settrace(Scalene.invalidate_lines)

    @staticmethod
    def free_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
    ) -> None:
        Scalene.__alloc_sigq.put((signum, this_frame))
        del this_frame

    @staticmethod
    def memcpy_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
    ) -> None:
        Scalene.__memcpy_sigq.put((signum, this_frame))
        del this_frame

    @staticmethod
    def enable_signals() -> None:
        """Set up the signal handlers to handle interrupts for profiling and start the
        timer interrupts."""
        if sys.platform == "win32":
            Scalene.timer_signals = True
            signal.signal(
                Scalene.__signals.cpu_signal,
                Scalene.cpu_signal_handler,
            )
            # On Windows, we simulate timer signals by running a background thread.
            Scalene.timer_signals = True
            t = threading.Thread(target=Scalene.windows_timer_loop)
            t.start()
            Scalene.start_signal_queues()
            return
        Scalene.start_signal_queues()
        # Set signal handlers for memory allocation and memcpy events.
        signal.signal(
            Scalene.__signals.malloc_signal, Scalene.malloc_signal_handler
        )
        signal.signal(
            Scalene.__signals.free_signal, Scalene.free_signal_handler
        )
        signal.signal(
            Scalene.__signals.memcpy_signal,
            Scalene.memcpy_signal_handler,
        )
        # Set every signal to restart interrupted system calls.
        signal.siginterrupt(Scalene.__signals.cpu_signal, False)
        signal.siginterrupt(Scalene.__signals.malloc_signal, False)
        signal.siginterrupt(Scalene.__signals.free_signal, False)
        signal.siginterrupt(Scalene.__signals.memcpy_signal, False)
        # Turn on the CPU profiling timer to run at the sampling rate (exactly once).
        signal.signal(
            Scalene.__signals.cpu_signal,
            Scalene.cpu_signal_handler,
        )
        signal.setitimer(
            Scalene.__signals.cpu_timer_signal,
            Scalene.__args.cpu_sampling_rate,
            0,
        )

    def __init__(
        self,
        arguments: argparse.Namespace,
        program_being_profiled: Optional[Filename] = None,
    ) -> None:
        # gc.set_debug(gc.DEBUG_SAVE)
        import scalene.replacement_pjoin

        # Hijack lock, poll, thread_join, fork, and exit.
        import scalene.replacement_lock
        import scalene.replacement_thread_join
        import scalene.replacement_exit
        import scalene.replacement_mp_lock

        if sys.platform != "win32":
            import scalene.replacement_poll_selector
            import scalene.replacement_fork

        Scalene.__args = cast(ScaleneArguments, arguments)
        Scalene.__cpu_sigq = ScaleneSigQueue(Scalene.cpu_sigqueue_processor)
        Scalene.__alloc_sigq = ScaleneSigQueue(
            Scalene.alloc_sigqueue_processor
        )
        Scalene.__memcpy_sigq = ScaleneSigQueue(
            Scalene.memcpy_sigqueue_processor
        )
        Scalene.__sigqueues = [
            Scalene.__cpu_sigq,
            Scalene.__alloc_sigq,
            Scalene.__memcpy_sigq,
        ]

        # Initialize the malloc related files; if for whatever reason
        # the files don't exist and we are supposed to be profiling
        # memory, exit.
        try:
            Scalene.__malloc_mapfile = ScaleneMapFile("malloc")
            Scalene.__memcpy_mapfile = ScaleneMapFile("memcpy")
        except:
            # Ignore if we aren't profiling memory; otherwise, exit.
            if not arguments.cpu_only:
                sys.exit(-1)

        Scalene.__signals.set_timer_signals(arguments.use_virtual_time)
        if arguments.pid:
            # Child process.
            # We need to use the same directory as the parent.
            # The parent always puts this directory as the first entry in the PATH.
            # Extract the alias directory from the path.
            dirname = os.environ["PATH"].split(os.pathsep)[0]
            Scalene.__python_alias_dir = pathlib.Path(dirname)
            Scalene.__pid = arguments.pid

        else:
            # Parent process.
            Scalene.__python_alias_dir = pathlib.Path(
                tempfile.mkdtemp(prefix="scalene")
            )
            # Create a temporary directory to hold aliases to the Python
            # executable, so scalene can handle multiple processes; each
            # one is a shell script that redirects to Scalene.
            Scalene.__pid = 0
            cmdline = ""
            # Pass along commands from the invoking command line.
            cmdline += f" --cpu-sampling-rate={arguments.cpu_sampling_rate}"
            if arguments.use_virtual_time:
                cmdline += " --use-virtual-time"
            if "off" in arguments and arguments.off:
                cmdline += " --off"
            if arguments.cpu_only:
                cmdline += " --cpu-only"

            environ = ScalenePreload.get_preload_environ(arguments)
            preface = " ".join(
                "=".join((k, str(v))) for (k, v) in environ.items()
            )

            # Add the --pid field so we can propagate it to the child.
            cmdline += f" --pid={os.getpid()} ---"
            payload = """#!/bin/bash
    echo $$
    %s %s -m scalene %s $@
    """ % (
                preface,
                sys.executable,
                cmdline,
            )
            # Now create all the files.
            for name in Scalene.__all_python_names:
                fname = os.path.join(Scalene.__python_alias_dir, name)
                with open(fname, "w") as file:
                    file.write(payload)
                os.chmod(fname, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
            # Finally, insert this directory into the path.
            sys.path.insert(0, str(Scalene.__python_alias_dir))
            os.environ["PATH"] = (
                str(Scalene.__python_alias_dir)
                + os.pathsep
                + os.environ["PATH"]
            )
            # Force the executable (if anyone invokes it later) to point to one of our aliases.
            sys.executable = Scalene.__all_python_names[0]

        # Register the exit handler to run when the program terminates or we quit.
        atexit.register(Scalene.exit_handler)
        # Store relevant names (program, path).
        if program_being_profiled:
            Scalene.__program_being_profiled = Filename(
                os.path.abspath(program_being_profiled)
            )

    @staticmethod
    def cpu_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
    ) -> None:
        """Wrapper for CPU signal handlers."""
        ru = resource.getrusage(resource.RUSAGE_SELF)
        now_sys = ru.ru_stime
        now_user = ru.ru_utime
        now_virtual = time.process_time()
        now_wallclock = time.perf_counter()
        if (
            Scalene.__last_signal_time_virtual == 0
            or Scalene.__last_signal_time_wallclock == 0
        ):
            Scalene.__last_signal_time_virtual = now_virtual
            Scalene.__last_signal_time_wallclock = now_wallclock
            Scalene.__last_signal_time_sys = now_sys
            Scalene.__last_signal_time_user = now_user
        # Sample GPU load as well.
        gpu_load = Scalene.__gpu.load()
        gpu_mem_used = Scalene.__gpu.memory_used()
        Scalene.__cpu_sigq.put(
            (
                signum,
                this_frame,
                now_virtual,
                now_wallclock,
                now_sys,
                now_user,
                gpu_load,
                gpu_mem_used,
                Scalene.__last_signal_time_virtual,
                Scalene.__last_signal_time_wallclock,
                Scalene.__last_signal_time_sys,
                Scalene.__last_signal_time_user,
            )
        )
        if sys.platform != "win32":
            signal.setitimer(
                Scalene.__signals.cpu_timer_signal,
                Scalene.__args.cpu_sampling_rate,
                0,
            )
        ru = resource.getrusage(resource.RUSAGE_SELF)
        now_sys = ru.ru_stime
        now_user = ru.ru_utime
        Scalene.__last_signal_time_virtual = time.process_time()
        Scalene.__last_signal_time_wallclock = time.perf_counter()
        Scalene.__last_signal_time_sys = now_sys
        Scalene.__last_signal_time_user = now_user

    @staticmethod
    def output_profile() -> bool:
        if Scalene.__args.json:
            json_output = Scalene.__json.output_profiles(
                Scalene.__stats,
                Scalene.__pid,
                Scalene.profile_this_code,
                Scalene.__python_alias_dir,
                profile_memory=not Scalene.__args.cpu_only,
            )
            if json_output:
                if not Scalene.__output.output_file:
                    Scalene.__output.output_file = "/dev/stdout"
                with open(Scalene.__output.output_file, "w") as f:
                    f.write(
                        json.dumps(json_output, sort_keys=True, indent=4)
                        + "\n"
                    )
                return True
            else:
                return False
        else:
            output = Scalene.__output
            did_output: bool = output.output_profiles(
                Scalene.__stats,
                Scalene.__pid,
                Scalene.profile_this_code,
                Scalene.__python_alias_dir,
                profile_memory=not Scalene.__args.cpu_only,
                reduced_profile=Scalene.__args.reduced_profile,
            )
            return did_output

    @staticmethod
    def profile_this_code(fname: Filename, lineno: LineNumber) -> bool:
        """When using @profile, only profile files & lines that have been decorated."""
        if not Scalene.__files_to_profile:
            return True
        if fname not in Scalene.__files_to_profile:
            return False
        # Now check to see if it's the right line range.
        line_info = (
            inspect.getsourcelines(fn)
            for fn in Scalene.__functions_to_profile[fname]
        )
        found_function = any(
            line_start <= lineno < line_start + len(lines)
            for (lines, line_start) in line_info
        )
        return found_function

    @staticmethod
    def cpu_sigqueue_processor(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
        now_virtual: float,
        now_wallclock: float,
        now_sys: float,
        now_user: float,
        gpu_load: float,
        gpu_mem_used: float,
        prev_virtual: float,
        prev_wallclock: float,
        prev_sys: float,
        prev_user: float,
    ) -> None:
        """Handle interrupts for CPU profiling."""
        # We have recorded how long it has been since we received a timer
        # before.  See the logic below.
        # If it's time to print some profiling info, do so.

        if now_wallclock >= Scalene.__next_output_time:
            # Print out the profile. Set the next output time, stop
            # signals, print the profile, and then start signals
            # again.
            Scalene.__next_output_time += Scalene.__args.profile_interval
            stats = Scalene.__stats
            # pause (lock) all the queues to prevent updates while we output
            with contextlib.ExitStack() as stack:
                locks = [
                    stack.enter_context(s.lock) for s in Scalene.__sigqueues
                ]
                stats.stop_clock()
                Scalene.output_profile()
                stats.start_clock()

        # Here we take advantage of an ostensible limitation of Python:
        # it only delivers signals after the interpreter has given up
        # control. This seems to mean that sampling is limited to code
        # running purely in the interpreter, and in fact, that was a limitation
        # of the first version of Scalene, meaning that native code was entirely ignored.
        #
        # (cf. https://docs.python.org/3.9/library/signal.html#execution-of-python-signal-handlers)
        #
        # However: lemons -> lemonade: this "problem" is in fact
        # an effective way to separate out time spent in
        # Python vs. time spent in native code "for free"!  If we get
        # the signal immediately, we must be running in the
        # interpreter. On the other hand, if it was delayed, that means
        # we are running code OUTSIDE the interpreter, e.g.,
        # native code (be it inside of Python or in a library). We
        # account for this time by tracking the elapsed (process) time
        # and compare it to the interval, and add any computed delay
        # (as if it were sampled) to the C counter.
        elapsed_virtual = now_virtual - prev_virtual
        elapsed_wallclock = now_wallclock - prev_wallclock
        # CPU utilization is the fraction of time spent on the CPU
        # over the total time.
        elapsed_user = now_user - prev_user
        elapsed_sys = now_sys - prev_sys
        try:
            cpu_utilization = elapsed_user / elapsed_wallclock
        except ZeroDivisionError:
            cpu_utilization = 0.0
        # Deal with an odd case reported here: https://github.com/plasma-umass/scalene/issues/124
        # (Note: probably obsolete now that Scalene is using the nvidia wrappers, but just in case...)
        # We don't want to report 'nan', so turn the load into 0.
        if math.isnan(gpu_load):
            gpu_load = 0.0
        gpu_time = gpu_load * Scalene.__last_cpu_sampling_rate
        Scalene.__stats.total_gpu_samples += gpu_time
        python_time = Scalene.__last_cpu_sampling_rate
        c_time = elapsed_virtual - python_time
        if c_time < 0:
            c_time = 0

        # Update counters for every running thread.

        new_frames = Scalene.compute_frames_to_record(this_frame)

        # Now update counters (weighted) for every frame we are tracking.
        total_time = python_time + c_time

        # First, find out how many frames are not sleeping.  We need
        # to know this number so we can parcel out time appropriately
        # (equally to each running thread).
        total_frames = sum(
            1
            for (frame, tident, orig_frame) in new_frames
            if not Scalene.__is_thread_sleeping[tident]
        )

        if total_frames == 0:
            normalized_time = total_time
        else:
            normalized_time = total_time / total_frames

        # Now attribute execution time.
        for (frame, tident, orig_frame) in new_frames:
            fname = Filename(frame.f_code.co_filename)
            lineno = LineNumber(frame.f_lineno)
            Scalene.enter_function_meta(frame, Scalene.__stats)
            if frame == new_frames[0][0]:
                # Main thread.
                if not Scalene.__is_thread_sleeping[tident]:

                    Scalene.__stats.cpu_samples_python[fname][lineno] += (
                        python_time / total_frames
                    )
                    Scalene.__stats.cpu_samples_c[fname][lineno] += (
                        c_time / total_frames
                    )
                    Scalene.__stats.cpu_samples[fname] += (
                        python_time + c_time
                    ) / total_frames
                    Scalene.__stats.cpu_utilization[fname][lineno].push(
                        cpu_utilization
                    )
                    Scalene.__stats.gpu_samples[fname][lineno] += (
                        gpu_time / total_frames
                    )

            else:
                # We can't play the same game here of attributing
                # time, because we are in a thread, and threads don't
                # get signals in Python. Instead, we check if the
                # bytecode instruction being executed is a function
                # call.  If so, we attribute all the time to native.
                # NOTE: for now, we don't try to attribute GPU time to threads.
                if not Scalene.__is_thread_sleeping[tident]:
                    # Check if the original caller is stuck inside a call.
                    if ScaleneFuncUtils.is_call_function(
                        orig_frame.f_code,
                        ByteCodeIndex(orig_frame.f_lasti),
                    ):
                        # It is. Attribute time to native.
                        Scalene.__stats.cpu_samples_c[fname][
                            lineno
                        ] += normalized_time
                    else:
                        # Not in a call function so we attribute the time to Python.
                        Scalene.__stats.cpu_samples_python[fname][
                            lineno
                        ] += normalized_time
                    Scalene.__stats.cpu_samples[fname] += normalized_time
                    Scalene.__stats.cpu_utilization[fname][lineno].push(
                        cpu_utilization
                    )

        # Clean up all the frames
        del new_frames[:]
        del new_frames
        del this_frame

        Scalene.__stats.total_cpu_samples += total_time

        if False:
            # Pick a new random interval, distributed around the mean.
            next_interval = 0.0
            while next_interval <= 0.0:
                # Choose a normally distributed random number around the
                # mean for the next interval. By setting the standard
                # deviation to a fraction of the mean, we know by
                # properties of the normal distribution that the
                # likelihood of iterating this loop more than once is
                # low. For a fraction 1/f, the probability is
                # p = 1-(math.erf(f/math.sqrt(2)))/2
                next_interval = random.normalvariate(
                    Scalene.__args.cpu_sampling_rate,
                    Scalene.__args.cpu_sampling_rate / 3.0,
                )
        else:
            next_interval = Scalene.__args.cpu_sampling_rate
        Scalene.__last_cpu_sampling_rate = next_interval

    # Returns final frame (up to a line in a file we are profiling), the thread identifier, and the original frame.
    @staticmethod
    def compute_frames_to_record(
        _this_frame: FrameType,
    ) -> List[Tuple[FrameType, int, FrameType]]:
        """Collects all stack frames that Scalene actually processes."""
        frames: List[Tuple[FrameType, int]] = [
            (
                cast(
                    FrameType,
                    sys._current_frames().get(cast(int, t.ident), None),
                ),
                cast(int, t.ident),
            )
            for t in threading.enumerate()
            if t != threading.main_thread()
        ]
        # Put the main thread in the front.

        tid = cast(int, threading.main_thread().ident)
        frames.insert(
            0,
            (
                sys._current_frames().get(tid, cast(FrameType,None)),
                tid,
            ),
        )

        # Process all the frames to remove ones we aren't going to track.
        new_frames: List[Tuple[FrameType, int, FrameType]] = []
        for (frame, tident) in frames:
            orig_frame = frame
            if not frame:
                continue
            fname = frame.f_code.co_filename
            # Record samples only for files we care about.
            if not fname:
                # 'eval/compile' gives no f_code.co_filename.  We have
                # to look back into the outer frame in order to check
                # the co_filename.
                back = cast(FrameType, frame.f_back)
                fname = Filename(back.f_code.co_filename)
            while not Scalene.should_trace(fname):
                # Walk the stack backwards until we hit a frame that
                # IS one we should trace (if there is one).  i.e., if
                # it's in the code being profiled, and it is just
                # calling stuff deep in libraries.
                if frame:
                    frame = cast(FrameType, frame.f_back)
                    if frame:
                        fname = frame.f_code.co_filename
                        continue
                else:
                    break
            if frame:
                new_frames.append((frame, tident, orig_frame))
        del frames[:]
        return new_frames

    @staticmethod
    def enter_function_meta(
        frame: FrameType, stats: ScaleneStatistics
    ) -> None:
        """Update tracking info so we can correctly report line number info later."""
        fname = Filename(frame.f_code.co_filename)
        lineno = LineNumber(frame.f_lineno)
        f = frame
        try:
            while "<" in Filename(f.f_code.co_name):
                f = cast(FrameType, frame.f_back)
                if (
                    "<genexpr>" in f.f_code.co_name
                    or "<module>" in f.f_code.co_name
                    or "<listcomp>" in f.f_code.co_name
                ):
                    return
        except:
            return
        if not Scalene.should_trace(f.f_code.co_filename):
            return

        fn_name = Filename(f.f_code.co_name)
        firstline = f.f_code.co_firstlineno
        # Prepend the class, if any
        while (
            f
            and f.f_back
            and f.f_back.f_code
            # NOTE: next line disabled as it is interfering with name resolution for thread run methods
            # and Scalene.should_trace(f.f_back.f_code.co_filename)
        ):
            if "self" in f.f_locals:
                prepend_name = f.f_locals["self"].__class__.__name__
                if "Scalene" not in prepend_name:
                    fn_name = prepend_name + "." + fn_name
                break
            if "cls" in f.f_locals:
                prepend_name = getattr(f.f_locals["cls"], "__name__", None)
                if not prepend_name or "Scalene" in prepend_name:
                    break
                fn_name = prepend_name + "." + fn_name
                break
            f = f.f_back

        stats.function_map[fname][lineno] = fn_name
        stats.firstline_map[fn_name] = LineNumber(firstline)

    @staticmethod
    def alloc_sigqueue_processor(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: FrameType,
    ) -> None:
        """Handle interrupts for memory profiling (mallocs and frees)."""
        stats = Scalene.__stats
        curr_pid = os.getpid()
        # Process the input array from where we left off reading last time.
        arr: List[
            Tuple[
                int,
                str,
                float,
                float,
                str,
                Filename,
                LineNumber,
                ByteCodeIndex,
            ]
        ] = []
        with contextlib.suppress(FileNotFoundError):
            while Scalene.__malloc_mapfile.read():
                count_str = Scalene.__malloc_mapfile.get_str()
                if count_str.strip() == "":
                    break
                (
                    action,
                    alloc_time_str,
                    count_str,
                    python_fraction_str,
                    pid,
                    pointer,
                    reported_fname,
                    reported_lineno,
                    bytei_str,
                ) = count_str.split(",")
                # assert action in ["M", "f", "F"]
                if int(curr_pid) == int(pid):
                    arr.append(
                        (
                            int(alloc_time_str),
                            action,
                            float(count_str),
                            float(python_fraction_str),
                            pointer,
                            Filename(reported_fname),
                            LineNumber(int(reported_lineno)),
                            ByteCodeIndex(int(bytei_str)),
                        )
                    )

        arr.sort()

        # Iterate through the array to compute the new current footprint.
        # and update the global __memory_footprint_samples.
        before = stats.current_footprint
        prevmax = stats.max_footprint
        freed_last_trigger = 0

        for item in arr:
            (
                _alloc_time,
                action,
                count,
                python_fraction,
                pointer,
                fname,
                lineno,
                bytei,
            ) = item
            count /= 1024 * 1024
            is_malloc = action == "M"
            if is_malloc:
                stats.current_footprint += count
                if stats.current_footprint > stats.max_footprint:
                    stats.max_footprint = stats.current_footprint
            else:
                assert action == "f" or action == "F"
                stats.current_footprint -= count
                if action == "f":
                    # Check if pointer actually matches
                    if stats.last_malloc_triggered[2] == pointer:
                        freed_last_trigger += 1
            stats.memory_footprint_samples.add(stats.current_footprint)
        after = stats.current_footprint

        if freed_last_trigger:
            if freed_last_trigger > 1:
                # Ignore the case where we have multiple last triggers in the sample file,
                # since this can lead to false positives.
                pass
            else:
                # We freed the last allocation trigger. Adjust scores.
                this_fn, this_ln, this_ptr = stats.last_malloc_triggered
                if this_ln != 0:
                    mallocs, frees = stats.leak_score[this_fn][this_ln]
                    stats.leak_score[this_fn][this_ln] = (
                        mallocs,
                        frees + 1,
                    )
            stats.last_malloc_triggered = (
                Filename(""),
                LineNumber(0),
                Address("0x0"),
            )

        allocs = 0.0
        last_malloc = (Filename(""), LineNumber(0), Address("0x0"))
        malloc_pointer = "0x0"
        curr = before

        # Go through the array again and add each updated current footprint.
        for item in arr:
            (
                _alloc_time,
                action,
                count,
                python_fraction,
                pointer,
                fname,
                lineno,
                bytei,
            ) = item

            if Scalene.__last_profiled != (fname, lineno):
                Scalene.__last_profiled_invalidated = True

            # Add the byte index to the set for this line (if it's not there already).
            stats.bytei_map[fname][lineno].add(bytei)
            count /= 1024 * 1024
            is_malloc = action == "M"
            if is_malloc:
                allocs += count
                curr += count
                malloc_pointer = pointer
                stats.memory_malloc_samples[fname][lineno][bytei] += count
                stats.memory_python_samples[fname][lineno][bytei] += (
                    python_fraction * count
                )
                stats.malloc_samples[fname] += 1
                stats.total_memory_malloc_samples += count
                # Check if we executed any other lines since the last sample.
                if Scalene.__last_profiled_invalidated:
                    # Yes, new line, so we bump the counter (used for later computing the average memory consumption).
                    # print("MALLOC updating", fname, lineno, Scalene.__last_profiled, stats.memory_malloc_samples[fname][lineno][bytei])
                    stats.memory_malloc_count[fname][lineno][bytei] += 1
                    Scalene.__last_profiled = (fname, lineno)
                    Scalene.__last_profiled_invalidated = False

                else:
                    # print("checked but nope: ", fname, lineno, Scalene.__last_profiled, Scalene.__last_profiled_invalidated)
                    pass
            else:
                assert action == "f" or action == "F"
                curr -= count
                stats.memory_free_samples[fname][lineno][bytei] += count
                stats.memory_free_count[fname][lineno][bytei] += 1
                stats.total_memory_free_samples += count

            stats.per_line_footprint_samples[fname][lineno].add(curr)
            # If we allocated anything, then mark this as the last triggering malloc
            if allocs > 0:
                last_malloc = (
                    Filename(fname),
                    LineNumber(lineno),
                    Address(malloc_pointer),
                )
        if False:
            stats.allocation_velocity = (
                stats.allocation_velocity[0] + (after - before),
                stats.allocation_velocity[1] + allocs,
            )
            # Update leak score if we just increased the max footprint (starting at a fixed threshold, currently 100MB,
            if prevmax < stats.max_footprint and stats.max_footprint > 100:
                stats.last_malloc_triggered = last_malloc
                mallocs, frees = stats.leak_score[fname][lineno]
                stats.leak_score[fname][lineno] = (mallocs + 1, frees)
        del _this_frame

    @staticmethod
    def before_fork() -> None:
        """Executed just before a fork."""
        Scalene.stop_signal_queues()

    @staticmethod
    def after_fork_in_parent(child_pid: int) -> None:
        """Executed by the parent process after a fork."""
        Scalene.add_child_pid(child_pid)
        Scalene.start_signal_queues()

    @staticmethod
    def after_fork_in_child() -> None:
        """
        Executed by a child process after a fork and mutates the
        current profiler into a child.
        """
        Scalene.__is_child = True

        Scalene.clear_metrics()
        if Scalene.__gpu.has_gpu():
            Scalene.__gpu.nvml_reinit()
        # Note-- __parent_pid of the topmost process is its own pid
        Scalene.__pid = Scalene.__parent_pid
        if not "off" in Scalene.__args or not Scalene.__args.off:
            Scalene.enable_signals()

    @staticmethod
    def memcpy_sigqueue_processor(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        frame: FrameType,
    ) -> None:
        curr_pid = os.getpid()
        arr: List[Tuple[int, int]] = []
        # Process the input array.
        with contextlib.suppress(ValueError):
            while Scalene.__memcpy_mapfile.read():
                count_str = Scalene.__memcpy_mapfile.get_str()
                (memcpy_time_str, count_str2, pid) = count_str.split(",")
                if int(curr_pid) == int(pid):
                    arr.append((int(memcpy_time_str), int(count_str2)))
        arr.sort()

        stats = Scalene.__stats
        new_frames = Scalene.compute_frames_to_record(frame)
        if not new_frames:
            del frame
            return

        for item in arr:
            _memcpy_time, count = item
            for (the_frame, _tident, _orig_frame) in new_frames:
                fname = Filename(the_frame.f_code.co_filename)
                line_no = LineNumber(the_frame.f_lineno)
                bytei = ByteCodeIndex(the_frame.f_lasti)
                # Add the byte index to the set for this line.
                stats.bytei_map[fname][line_no].add(bytei)
                stats.memcpy_samples[fname][line_no] += count
        del new_frames[:]
        del new_frames
        del frame

    @staticmethod
    @lru_cache(None)
    def should_trace(filename: str) -> bool:
        """Return true if the filename is one we should trace."""
        if not filename:
            return False
        # If the @profile decorator has been used,
        # we restrict profiling to files containing decorated functions.
        if Scalene.__files_to_profile:
            return filename in Scalene.__files_to_profile
        # Generic handling follows (when no @profile decorator has been used).
        profile_only_list = Scalene.__args.profile_only.split(",")
        if "site-packages" in filename or "/lib/python" in filename:
            # Don't profile Python internals by default.
            if not Scalene.__args.profile_all:
                return False
        if filename[0] == "<":
            if "<ipython" in filename:
                # Profiling code created in a Jupyter cell:
                # create a file to hold the contents.
                import IPython
                import re

                # Find the input where the function was defined;
                # we need this to properly annotate the code.
                result = re.match("<ipython-input-([0-9]+)-.*>", filename)
                if result:
                    # Write the cell's contents into the file.
                    with open(filename, "w+") as f:
                        f.write(
                            IPython.get_ipython().history_manager.input_hist_raw[
                                int(result.group(1))
                            ]
                        )
                return True
            else:
                # Not a real file and not a function created in Jupyter.
                return False
        if "scalene/scalene" in filename:
            # Don't profile the profiler.
            return False
        # If (a) `profile-only` was used, and (b) the file matched
        # NONE of the provided patterns, don't profile it.
        not_found_in_profile_only = profile_only_list and not any(
            prof in filename for prof in profile_only_list
        )
        if not_found_in_profile_only:
            return False
        # Now we've filtered out any non matches to profile-only patterns.
        # If `profile-all` is specified, profile this file.
        if Scalene.__args.profile_all:
            return True
        # Profile anything in the program's directory or a child directory,
        # but nothing else, unless otherwise specified.
        filename = os.path.abspath(filename)
        return Scalene.__program_path in filename

    @staticmethod
    def clear_mmap_data() -> None:
        if not Scalene.__args.cpu_only:
            while Scalene.__malloc_mapfile.read():
                pass
            while Scalene.__memcpy_mapfile.read():
                pass

    __done = False

    @staticmethod
    def start() -> None:
        """Initiate profiling."""
        # Scalene.clear_mmap_data()
        Scalene.__stats.start_clock()
        Scalene.enable_signals()
        Scalene.__done = False

    @staticmethod
    def stop() -> None:
        """Complete profiling."""
        Scalene.__done = True
        Scalene.disable_signals()
        Scalene.__stats.stop_clock()

    @staticmethod
    def isDone() -> bool:
        return Scalene.__done

    @staticmethod
    def start_signal_handler(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: FrameType,
    ) -> None:
        for pid in Scalene.__child_pids:
            os.kill(pid, Scalene.__signals.start_profiling_signal)
        Scalene.start()

    @staticmethod
    def stop_signal_handler(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: FrameType,
    ) -> None:
        for pid in Scalene.__child_pids:
            os.kill(pid, Scalene.__signals.stop_profiling_signal)
        Scalene.stop()

    @staticmethod
    def disable_signals(retry: bool = True) -> None:
        """Turn off the profiling signals."""
        if sys.platform == "win32":
            Scalene.timer_signals = False
            return
        try:
            signal.setitimer(Scalene.__signals.cpu_timer_signal, 0)
            signal.signal(Scalene.__signals.malloc_signal, signal.SIG_IGN)
            signal.signal(Scalene.__signals.free_signal, signal.SIG_IGN)
            signal.signal(Scalene.__signals.memcpy_signal, signal.SIG_IGN)
            Scalene.stop_signal_queues()
        except:
            # Retry just in case we get interrupted by one of our own signals.
            if retry:
                Scalene.disable_signals(retry=False)

    @staticmethod
    def exit_handler() -> None:
        """When we exit, disable all signals."""
        Scalene.disable_signals()
        # Delete the temporary directory.
        with contextlib.suppress(Exception):
            if not Scalene.__pid:
                Scalene.__python_alias_dir.cleanup()  # type: ignore
        with contextlib.suppress(Exception):
            os.remove(f"/tmp/scalene-malloc-lock{os.getpid()}")

    @staticmethod
    def termination_handler(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: FrameType,
    ) -> None:
        sys.exit(-1)

    def profile_code(
        self,
        code: str,
        the_globals: Dict[str, str],
        the_locals: Dict[str, str],
    ) -> int:
        # If --off is set, tell all children to not profile and stop profiling before we even start.
        if "off" not in Scalene.__args or not Scalene.__args.off:
            self.start()
        # Run the code being profiled.
        exit_status = 0
        try:
            exec(code, the_globals, the_locals)
        except SystemExit as se:
            # Intercept sys.exit and propagate the error code.
            exit_status = se.code
        except KeyboardInterrupt:
            # Cleanly handle keyboard interrupts (quits execution and dumps the profile).
            print("Scalene execution interrupted.")
            pass
        except Exception as e:
            print("Error in program being profiled:\n", e)
            traceback.print_exc()
        finally:
            self.stop()
            # If we've collected any samples, dump them.
            if Scalene.output_profile():
                pass
            else:
                print(
                    "Scalene: Program did not run for long enough to profile."
                )
        return exit_status

    @staticmethod
    def process_args(args: argparse.Namespace) -> None:
        Scalene.__args = cast(ScaleneArguments, args)
        Scalene.__next_output_time = (
            time.perf_counter() + Scalene.__args.profile_interval
        )
        Scalene.__output.html = args.html
        Scalene.__output.output_file = args.outfile
        Scalene.__is_child = args.pid != 0
        # the pid of the primary profiler
        Scalene.__parent_pid = args.pid if Scalene.__is_child else os.getpid()

    @staticmethod
    def main() -> None:
        (
            args,
            left,
        ) = ScaleneParseArgs.parse_args()
        Scalene.run_profiler(args, left)

    @staticmethod
    def run_profiler(args: argparse.Namespace, left: List[str]) -> None:
        # Set up signal handlers for starting and stopping profiling.
        signal.signal(
            Scalene.__signals.start_profiling_signal,
            Scalene.start_signal_handler,
        )
        signal.signal(
            Scalene.__signals.stop_profiling_signal,
            Scalene.stop_signal_handler,
        )
        if sys.platform != "win32":
            signal.siginterrupt(
                Scalene.__signals.start_profiling_signal, False
            )
            signal.siginterrupt(Scalene.__signals.stop_profiling_signal, False)

        signal.signal(signal.SIGINT, Scalene.interruption_handler)

        did_preload = ScalenePreload.setup_preload(args)
        if not did_preload:
            with contextlib.suppress(Exception):
                # If running in the background, print the PID.
                if os.getpgrp() != os.tcgetpgrp(sys.stdout.fileno()):
                    # In the background.
                    print(f"Scalene now profiling process {os.getpid()}")
                    print(
                        f"  to disable profiling: python3 -m scalene.profile --off --pid {os.getpid()}"
                    )
                    print(
                        f"  to resume profiling:  python3 -m scalene.profile --on  --pid {os.getpid()}"
                    )
        Scalene.__stats.clear_all()
        sys.argv = left
        with contextlib.suppress(Exception):
            multiprocessing.set_start_method("fork")
        try:
            Scalene.process_args(args)
            try:
                # Look for something ending in '.py'. Treat the first one as our executable.
                progs = [x for x in sys.argv if re.match(".*\.py$", x)]
                # Just in case that didn't work, try sys.argv[0] and __file__.
                with contextlib.suppress(Exception):
                    progs.append(sys.argv[0])
                    progs.append(__file__)
                with open(progs[0], "rb") as prog_being_profiled:
                    # Read in the code and compile it.
                    try:
                        code = compile(
                            prog_being_profiled.read(),
                            progs[0],
                            "exec",
                        )
                    except SyntaxError:
                        traceback.print_exc()
                        sys.exit(-1)
                    # Push the program's path.
                    program_path = os.path.dirname(os.path.abspath(progs[0]))
                    sys.path.insert(0, program_path)
                    if len(args.program_path) > 0:
                        Scalene.__program_path = os.path.abspath(
                            args.program_path
                        )
                    else:
                        Scalene.__program_path = program_path
                    # Grab local and global variables.
                    if not Scalene.__args.cpu_only:
                        from scalene import pywhere

                        pywhere.register_files_to_profile(
                            list(Scalene.__files_to_profile.keys()),
                            Scalene.__program_path,
                            Scalene.__args.profile_all,
                        )

                    import __main__

                    the_locals = __main__.__dict__
                    the_globals = __main__.__dict__
                    # Splice in the name of the file being executed instead of the profiler.
                    the_globals["__file__"] = os.path.basename(progs[0])
                    # Some mysterious module foo to make this work the same with -m as with `scalene`.
                    the_globals["__spec__"] = None
                    # Start the profiler.
                    fullname = os.path.join(
                        program_path, os.path.basename(progs[0])
                    )
                    # Do a GC before we start.
                    gc.collect()
                    profiler = Scalene(args, Filename(fullname))
                    try:
                        # We exit with this status (returning error code as appropriate).
                        exit_status = profiler.profile_code(
                            code, the_locals, the_globals
                        )
                        sys.exit(exit_status)
                    except StopJupyterExecution:
                        # Running in Jupyter notebooks
                        pass
                    except AttributeError:
                        # don't let the handler below mask programming errors
                        raise
                    except Exception as ex:
                        template = "Scalene: An exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        print(message)
                        print(traceback.format_exc())
            except (FileNotFoundError, IOError):
                print("Scalene: could not find input file " + progs[0])
                sys.exit(-1)
        except SystemExit:
            pass
        except StopJupyterExecution:
            pass
        except Exception:
            print("Scalene failed to initialize.\n" + traceback.format_exc())
            sys.exit(-1)
        finally:
            with contextlib.suppress(Exception):
                Scalene.__malloc_mapfile.close()
                Scalene.__memcpy_mapfile.close()
                if not Scalene.__is_child:
                    Scalene.cleanup_files()


if __name__ == "__main__":
    Scalene.main()
