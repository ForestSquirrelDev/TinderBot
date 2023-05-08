from tkinter import ttk
from tkinter import *

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import *

from tinderbotz.bot import Bot
from tinderbotz.utils import custom_logger

class DeveloperTools:
    _root: Tk
    _bot: Bot

    _path_field_var: StringVar
    _code_exec_var: StringVar

    _inspected_element: WebElement

    def __init__(self, root: Tk, bot: Bot):
        self._root = root
        self._bot = bot

        self._path_field_var = StringVar()
        self._code_exec_var = StringVar()

    def _set_inspected_element(self) -> None:
        try:
            self._inspected_element = self._bot.session.driver.find_element(By.XPATH, self._path_field_var.get())
            custom_logger.log_info(f"Successfully obtained element: {self._inspected_element}")
        except BaseException as ex:
            custom_logger.log_error(f"Exception during developer find element: {ex}")

    def _exec(self) -> None:
        try:
            exec(self._code_exec_var.get())
            custom_logger.log_info("Successfully executed code")
        except BaseException as ex:
            custom_logger.log_error(f"Failed to exec code: {ex}")

    def open_developer_tools(self) -> None:
        new_window = Toplevel(self._root)
        new_window.title("Developer tools")
        new_window.geometry("570x500")
        Label(new_window, text="Developer tools window")

        ttk.Label(new_window, text="Path").grid(column=0, row=0)
        ttk.Entry(new_window, width=70, textvariable=self._path_field_var).grid(column=1, row=0)
        ttk.Button(new_window, text="Get element", command=lambda: self._set_inspected_element()).grid(column=2, row=0)

        ttk.Label(new_window, text="Code exec").grid(column=0, row=1)
        ttk.Entry(new_window, width=70, textvariable=self._code_exec_var).grid(column=1, row=1)
        ttk.Button(new_window, text="Execute", command=lambda: self._exec()).grid(column=2, row=1)
