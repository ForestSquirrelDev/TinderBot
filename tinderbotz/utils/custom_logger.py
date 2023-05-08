import datetime
import sys
import traceback
from os import getcwd
from tkinter import *

from tinderbotz.utils import datetime_utils

_noprint_table = {
    i: ' ??? ' for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}
_log_path: str = getcwd() + "/log.txt"

text: Text = None

# this log does not go to widget
def log_debug(log: str) -> None:
    _print(f"[DEBUG]: {datetime.datetime.now()}: {log}")

def log_debug_debug(log: str) -> None:
    _print(f"[DEBUG] {datetime.datetime.now()}: {log}")
    _insert_in_widget(f"[DEBUG] {datetime.datetime.now()}: {log}")

# this and below logs go to widget
def log_info(log: str) -> None:
    print_string = f"[INFO]: {datetime.datetime.now()}: {log}"
    widget_string = f"[INFO]: {datetime_utils.hours_minutes_seconds(':')}: {log}"
    _print(print_string)
    _insert_in_widget(widget_string)

def log_warning(log: str) -> None:
    print_string = f"[WARNING]: {datetime.datetime.now()}: {log}"
    widget_string = f"[WARNING]: {datetime_utils.hours_minutes_seconds(':')}: {log}"
    _print(print_string)
    _insert_in_widget(widget_string)

def log_error(log: str) -> None:
    print_string = f"[ERROR]: {datetime.datetime.now()}: {log}"
    widget_string = f"[ERROR]: {datetime_utils.hours_minutes_seconds(':')}: {log}"
    _print(print_string)
    _insert_in_widget(widget_string)

def log_error_debug(log: str) -> None:
    print_string = f"[ERROR]: {datetime.datetime.now()}: {log}"
    _print(print_string)

def log_exception(log: str) -> None:
    print_string = f"[EXCEPTION]: {datetime.datetime.now()}: {log}"
    _print(print_string)
    _print_stacktrace(traceback.format_exc())

def log_fatal(log: str) -> None:
    print_string = f"[FATAL]: {datetime.datetime.now()}: {log}"
    _print(print_string)
    _print_stacktrace(traceback.format_exc())

def _print(log: str) -> None:
    try:
        print(log)
        with open(_log_path, "a") as logs:
            try:
                logs.write(f"\n{log}")
            except:
                pass
    except:
        pass

def _insert_in_widget(string: str) -> None:
    if text is None:
        return
    def append() -> None:
        try:
            text.configure(state='normal')
            text.insert(END, string + '\n')
            text.configure(state='disabled')
            text.yview(END)
        except:
            pass
    text.after(0, append())

def _print_stacktrace(stacktrace: str) -> None:
    print(stacktrace)
    with open(_log_path, "a") as logs:
        logs.write(f"\n[STACKTRACE]: {datetime.datetime.now()}: {stacktrace}")
