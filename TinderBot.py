import sys
import threading
from typing import Tuple

import PySimpleGUI
from chromedriver_autoinstaller import get_chrome_version

from tinderbotz.serial_key.thread_serial_time_checker import SerialTimeChecker

import tkinter
import atexit
from tinderbotz.utils import custom_logger
import multiprocessing
from threading import Thread
from tinderbotz.bot import Bot
from tkinter import ttk
from tkinter import *
from tinderbotz.serial_key.validate_activate_sequence import Sequencer
from tinderbotz.developer_tools import DeveloperTools
import localization.localization_manager
from tinderbotz import conditionals, single_instance_handler
from tinderbotz.options_window import OptionsWindow

def at_exit():
    single_instance_handler.remove_lock_file()

def show_warning_box(title: str, description: str):
    try:
        custom_logger.log_debug("PySimpleGUI.Popup")
        PySimpleGUI.Popup(title, description)
    except BaseException as ex:
        custom_logger.log_exception(f"{ex}")
        raise ex

def create_sequencer() -> Sequencer:
    return Sequencer()

def check_serial(sequencer: Sequencer) -> Tuple[bool, str]:
    custom_logger.log_debug("seduencer.run()")
    result = sequencer.run()
    return result

if __name__ == "__main__":
    multiprocessing.freeze_support()

class ThreadContainer:
    thread: Thread
    serial_key_checking_thread: Thread
    serial_key_stop_event: threading.Event

    def __init__(self, thread: Thread, serial_key_checking_thread: Thread, serial_key_stop_event: threading.Event):
        self.thread = thread
        self.serial_key_checking_thread = serial_key_checking_thread
        self.serial_key_stop_event = serial_key_stop_event


if __name__ == "__main__":
    _bot: Bot
    _serial_time_checker: SerialTimeChecker
    _thread_container: ThreadContainer
    _developer_tools: DeveloperTools
    _options_window: OptionsWindow

    _start_button: Button
    _pause_button: Button
    _settings_button: Button

    def start():
        custom_logger.log_info(localization.localization_manager.starting_the_bot())
        if not _thread_container.thread.is_alive():
            custom_logger.log_debug("Thread is not alive. Creating new thread")
            _thread_container.thread = Thread(target=_bot.run)
            _thread_container.thread.start()
        _bot.start()

    def stop() -> None:
        custom_logger.log_info(localization.localization_manager.stopping_the_bot())
        _bot.stop()

    def terminate() -> None:
        _thread_container.serial_key_stop_event.set()
        _bot.quit()
        custom_logger.text = None
        root.destroy()

    def on_key_expired() -> None:
        stop()
        _start_button.destroy()
        _settings_button.destroy()
        _pause_button.destroy()
        custom_logger.log_warning(localization.localization_manager.serial_key_expired())

    already_running: bool = single_instance_handler.is_instance_running()
    custom_logger.log_debug(f"Already running: {already_running}")
    if already_running:
        # noinspection PyUnboundLocalVariable
        show_warning_box(localization.localization_manager.error(), localization.localization_manager.already_running())
        sys.exit()
    else:
        custom_logger.log_info("Register atexit")
        atexit.register(at_exit)
        single_instance_handler.create_lock_file()

    not_found: bool = False
    ver: str = ""
    try:
        ver = get_chrome_version()
    except FileNotFoundError as ex:
        custom_logger.log_exception(f"{ex}")
        not_found = True
    dot = ver.find('.')
    version_short = ver[0: dot]
    custom_logger.log_info(f"Chromeversion is {version_short}")

    if ver == "" or not_found or (version_short.isdigit() and int(version_short) < 111):
        show_warning_box(localization.localization_manager.browser_error(),
                         localization.localization_manager.install_latest_chrome())
        sys.exit()

    expiration_ts: int = 9999999999999
    if not conditionals.DEVELOP:
        serial_valid: bool = False
        sequencer = create_sequencer()
        try:
            custom_logger.log_debug("check_serial_start")
            check_serial: Tuple[bool, str] = check_serial(sequencer)
            custom_logger.log_debug("check_serial_finish")
            if not check_serial[0]:
                custom_logger.log_debug("show_warning_box_start")
                # noinspection PyUnboundLocalVariable
                show_warning_box(localization.localization_manager.serial_key_error(),
                                 f"{check_serial[1]}\n{localization.localization_manager.telegram()}: @ayayaintensifies")
                custom_logger.log_debug("show_warning_box_finish")
            serial_valid = check_serial[0]
        except BaseException as ex:
            custom_logger.log_exception(f"Unhandled exception during serial checks: {ex}")
            show_warning_box(localization.localization_manager.serial_key_error(), localization.localization_manager.serial_key_check_failed()
                             + f"\n{localization.localization_manager.telegram()}: @ayayaintensifies")
            raise ex

        if not serial_valid:
            custom_logger.log_debug("sys.exit()")
            if sequencer is not None:
                sequencer.dispose()
            sys.exit()
        expiration_ts: int = sequencer.get_expiration_ts()
        sequencer.dispose()

    # main
    try:
        _bot = Bot()
        stop_event = threading.Event()
        _serial_time_checker = SerialTimeChecker(expiration_ts, on_key_expired, stop_event)
        _thread_container = ThreadContainer(Thread(target=_bot.run), Thread(target=_serial_time_checker.start_checking), stop_event)
        root = Tk()
        _developer_tools = DeveloperTools(root, _bot)
        _options_window = OptionsWindow(root, _bot)
        root.protocol("WM_DELETE_WINDOW", terminate)
        root.resizable(False, False)
        root.title("Tinder bot by Forest Squirrel")
        frame = ttk.Frame(root, padding=10)
        frame.grid()

        try:
            icon = PhotoImage(file="icon.ico")
            root.wm_iconphoto(True, icon)
        except BaseException as ex:
            custom_logger.log_error(f"Exception during icon config: {ex}")
            pass

        # noinspection PyUnboundLocalVariable
        _start_button = ttk.Button(frame, text=localization.localization_manager.start(), command=start)
        _start_button.grid(column=0, row=1, pady=1)

        _pause_button = ttk.Button(frame, text=localization.localization_manager.pause(), command=stop)
        _pause_button.grid(column=0, row=2, pady=1)

        _settings_button = ttk.Button(frame, text=localization.localization_manager.settings(),
                   command=lambda: _options_window.open_settings_window((root.winfo_rootx(), root.winfo_rooty())))
        _settings_button.grid(column=0, row=3, pady=1)

        ttk.Button(frame, text=localization.localization_manager.exit_app(), command=terminate).grid(column=0, row=4, pady=1)
        if conditionals.DEVELOP:
            ttk.Button(frame, text="Open developer tools", command=_developer_tools.open_developer_tools) \
                .grid(column=0, row=5, pady=5)
        t = tkinter.Text(root, width=60, height=10, borderwidth=5, relief='groove')
        t.grid(column=1, row=0, sticky="W", padx=7)
        custom_logger.text = t
        t.configure(state='disabled')
        custom_logger.log_info(localization.localization_manager.press_start())

        _thread_container.thread.start()
        _thread_container.serial_key_checking_thread.start()
        root.mainloop()
    except BaseException as ex:
        custom_logger.log_fatal(localization.localization_manager.fatal_error(f"{type(ex)}"))
        custom_logger.log_exception(f"Exception: {ex}")
        raise ex
