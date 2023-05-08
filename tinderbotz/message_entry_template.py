from tkinter import Toplevel, StringVar, Entry, Button, ttk
from typing import Callable

import localization.localization_manager
from tinderbotz.options.i_implements_custom_indexer import IImplementsCustomIndexer


class MessageEntryTemplate:
    _root_toplevel: Toplevel
    _text_var: StringVar

    _entry: Entry
    _delete_button: Button
    _on_delete: Callable = None # Callable[[MessageEntryTemplate], None]

    index: int
    _model_words_container: IImplementsCustomIndexer

    _set_text_callback_enabled: bool = True

    def __init__(self, root: Toplevel, model_words_container: IImplementsCustomIndexer, self_index: int):
        self._root_toplevel = root
        self._text_var = StringVar()

        self._model_words_container = model_words_container
        self.index = self_index

        self._text_var.trace("w", lambda name, index, mode, sv=self._text_var: self._on_entry_changed())

    def create(self, text: str = "") -> None:
        self._entry = ttk.Entry(self._root_toplevel, textvariable=self._text_var)
        self.set_text_no_callback(text)
        self._delete_button = ttk.Button(self._root_toplevel, text=localization.localization_manager.delete(), command=self._delete)
        self._entry.grid(sticky="W", row=self.index + 1)
        self._delete_button.grid(sticky="W", row=self.index + 1, column=1)

    def set_text_no_callback(self, text: str) -> None:
        self._set_text_callback_enabled = False
        self._text_var.set(text)
        self._set_text_callback_enabled = True

    def register_on_delete(self, cb: Callable) -> None:
        self._on_delete = cb

    def get_text_readonly(self) -> str:
        return self._text_var.get()

    def update_index(self, index: int) -> None:
        self._entry.grid(sticky="W", row=index + 1)
        self._delete_button.grid(sticky="W", row=index + 1, column=1)
        self.index = index

    def _delete(self) -> None:
        self._entry.destroy()
        self._delete_button.destroy()
        if self._on_delete is not None:
            self._on_delete(self)
        del self._on_delete

    def _on_entry_changed(self) -> None:
        if not self._set_text_callback_enabled:
            return
        text = self._text_var.get()
        self._model_words_container[self.index] = text

