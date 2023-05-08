import os
from typing import List

import psutil

from tinderbotz.utils import custom_logger

_lockfile: str = f"{os.getcwd()}/tinderbot_lockfile"
_process_names: List[str] = ["TinderBot.exe", "Python.exe", "python.exe", "python"]

def is_instance_running() -> bool:
    try:
        custom_logger.log_info(f"Lockfile exists? {os.path.exists(_lockfile)}")
        if not os.path.exists(_lockfile):
            return False
        with open(_lockfile, "r") as file:
            pid: str = file.readline()
            if not (pid.isdigit()):
                custom_logger.log_debug(f"Pid is not digit. pid: {pid}")
                return False
            return _is_process_running_with_pid_and_name_pinpoint(int(pid), _process_names)
    except BaseException as ex:
        custom_logger.log_exception(f"Failed to check if instance is running: {ex}")
        return False


def create_lock_file() -> None:
    try:
        pid: int = psutil.Process().pid
        with open(_lockfile, "w") as file:
            file.write(str(pid))
    except BaseException as ex:
        custom_logger.log_exception(f"Failed to create lockfile: {ex}")

def remove_lock_file() -> None:
    if os.path.exists(_lockfile):
        os.remove(_lockfile)

def _is_process_running_with_pid_and_name_iter(pid: int, name: str) -> bool:
    for process in psutil.process_iter(['name', 'pid']):
        d = process.as_dict()
        print(f"Iterated over process with PID {d['pid']} and name {d['name']}")
        if (d['name'] == name and d['pid'] == pid):
            return True
    return False

def _is_process_running_with_pid_and_name_pinpoint(pid: int, names: List[str]) -> bool:
    if not psutil.pid_exists(pid):
        custom_logger.log_debug(f"Process with pid {pid} does not exist")
        return False
    custom_logger.log_debug(f"Process with pid {pid} exists")
    process_name: str = psutil.Process(pid).name()
    custom_logger.log_debug(f"Name of process with pid {pid} is {process_name}")
    for name in names:
        if process_name == name:
            return True
    return False
