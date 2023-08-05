from __future__ import annotations

import functools
import signal
import subprocess
import sys
import threading
import time
import traceback
from types import FrameType
from typing import Dict, Iterator, NamedTuple, Protocol

_POLL_INTERVAL = 0.1
_SIGTERM_TIMEOUT = 15
_MONITOR_THREAD_TIMEOUT = 5
_CONDITION_CHECK_INTERVAL = 1
_CONDITION_CHECK_TIMEOUT = 10


class WorkerConfig(NamedTuple):
    name: str
    num_workers: int
    cmd: list[str]
    env: dict[str, str] | None = None
    start_condition_cmd: list[str] | None = None


WorkerConfigDict = Dict[str, WorkerConfig]


class WorkerProcessInfo(NamedTuple):
    name: str
    popen_obj: subprocess.Popen
    monitor: threading.Thread


class WorkerProcess(NamedTuple):
    worker_config: WorkerConfig
    process_info_list: list[WorkerProcessInfo]


class _PrinterType(Protocol):
    def __call__(self, prefix: str, txt: str, *, is_stdout: bool = False) -> None:
        ...


def _process_launcher(
    term_event: threading.Event,
    printer: _PrinterType,
    worker_process: WorkerProcess,
) -> None:
    worker_config = worker_process.worker_config
    process_info_list = worker_process.process_info_list

    if worker_config.start_condition_cmd is not None:
        printer(worker_config.name, 'Check start condition...')

        while not term_event.is_set():
            try:
                condition_result = subprocess.run(
                    worker_config.start_condition_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                    timeout=_CONDITION_CHECK_TIMEOUT,
                )
                if condition_result.returncode == 0:
                    break
            except Exception:
                pass

            printer(worker_config.name, 'Start condition is not met')

            time.sleep(_CONDITION_CHECK_INTERVAL)

    for idx in range(worker_config.num_workers):
        if term_event.is_set():
            return

        process_name = f'{worker_config.name}_{idx + 1}'

        popen_obj = subprocess.Popen(
            worker_config.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=worker_config.env,
            text=True,
            start_new_session=True,
        )

        printer(process_name, f'Started a process with PID {popen_obj.pid}')

        monitor = threading.Thread(
            target=functools.partial(_process_monitor, printer, process_name, popen_obj),
            daemon=True,
        )
        monitor.start()

        process_info_list.append(
            WorkerProcessInfo(
                name=process_name,
                popen_obj=popen_obj,
                monitor=monitor,
            )
        )


def _process_monitor(
    printer: _PrinterType,
    process_name: str,
    popen_obj: subprocess.Popen,
) -> None:
    assert popen_obj.stdout is not None

    while True:
        try:
            output: str = popen_obj.stdout.readline()
        except Exception:
            print(
                'Error while reading outputs from "%s"\n%s' % (process_name, traceback.format_exc()),
                flush=True,
            )
            break

        if not output:
            break

        printer(process_name, output.rstrip(), is_stdout=True)

    while True:
        retcode = popen_obj.poll()
        if retcode is not None:
            break
        time.sleep(_POLL_INTERVAL)

    printer(process_name, f'Terminated (retcode: {retcode})')


def run(worker_config_dict: WorkerConfigDict) -> None:
    '''Run a set of processes defined by `worker-config`

    .. note:: Example Configuration

        import os

        worker_config = {
            'manager': {
                'num_workers': 1,
                'cmd': ['python', 'launcher_manager.py'],
                'env': {
                    'MANAGER_IN_PORT': '80',
                    'MANAGER_OUT_PORT': '1234',
                },
            },
            'http-server': {
                'num_workers': 1,
                'cmd': [
                    'gunicorn',
                    '-c', './assets/gunicorn_conf.py',
                    'launcher_http_server:server.app',
                ],
            },
            'http-server-nginx': {
                'num_workers': 1,
                'cmd': ['nginx', '-g', 'daemon off;'],
                'start_condition_cmd': [
                    'curl',
                    '--fail', '-s',
                    'http://0.0.0.0:8080/ping',
                ],
            },
            'tcp-server': {
                'num_workers': int(os.environ.get('TCP_SERVER_NUM_WORKERS', 1)),
                'cmd': ['python', 'launcher_tcp_server.py'],
            }
        }
    '''

    term_signal = signal.Signals.SIGTERM
    term_event = threading.Event()

    def _signal_handler(signum: int, frame: FrameType) -> None:
        if term_event.is_set():
            print('Forced termination of manager', flush=True)
            sys.exit(1)

        nonlocal term_signal
        term_signal = signal.Signals(signum)
        term_event.set()
        print('Signal handler called with signal :', term_signal.name, flush=True)

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    max_name_length = max(
        len('%s_%d' % (worker_config.name, worker_config.num_workers + 1))
        for worker_config in worker_config_dict.values()
    )

    def _printer(prefix: str, txt: str, *, is_stdout: bool = False) -> None:
        formatstr = '%-{:d}s %s %s'.format(max_name_length)
        print(formatstr % (prefix, '|' if is_stdout else '>', txt), flush=True)

    worker_processes: list[WorkerProcess] = []
    for worker_config in worker_config_dict.values():
        worker_process = WorkerProcess(worker_config, [])
        worker_processes.append(worker_process)

        worker_process_launcher = threading.Thread(
            target=functools.partial(_process_launcher, term_event, _printer, worker_process),
            daemon=True
        )
        worker_process_launcher.start()

    def _all_worker_process_info_iterator() -> Iterator[WorkerProcessInfo]:
        for worker_process in worker_processes:
            for process_info in worker_process.process_info_list:
                yield process_info

    # Monitor the liveness of all worker processes
    any_done_process_info: WorkerProcessInfo | None = None
    try:
        while not term_event.is_set():
            for process_info in _all_worker_process_info_iterator():
                if process_info.popen_obj.poll() is not None:
                    any_done_process_info = process_info
                    term_event.set()
                    break

                time.sleep(_POLL_INTERVAL)
        else:
            print(
                'Terminate all workers... (cuased by %s)' % (
                    any_done_process_info.name if any_done_process_info else 'unknown'
                ),
                flush=True
            )

    except Exception:
        traceback.print_exc()

    # Send stop signals to worker processes
    for process_info in _all_worker_process_info_iterator():
        retcode = process_info.popen_obj.poll()
        if retcode is not None:
            continue
        _printer(process_info.name, '%s is requested' % term_signal.name)
        process_info.popen_obj.send_signal(term_signal.value)

    # Wait until all worker processes termintate
    wait_until_ts = time.monotonic() + _SIGTERM_TIMEOUT
    while time.monotonic() < wait_until_ts:
        for process_info in _all_worker_process_info_iterator():
            retcode = process_info.popen_obj.poll()
            if retcode is None:
                break
        else:
            break
        time.sleep(_POLL_INTERVAL)
    else:
        print('Timeout while waiting the termination of worker processes', flush=True)

    wait_until_ts = time.monotonic() + _MONITOR_THREAD_TIMEOUT
    while time.monotonic() < wait_until_ts:
        for process_info in _all_worker_process_info_iterator():
            process_info.monitor.join(0)
            if process_info.monitor.is_alive():
                break
        else:
            break
        time.sleep(_POLL_INTERVAL)
    else:
        print('Timeout while waiting the termination of monitor threads', flush=True)

        print('Live monitor threads:', flush=True)
        for process_info in _all_worker_process_info_iterator():
            if process_info.monitor.is_alive():
                print('- %s' % process_info.name, flush=True)
