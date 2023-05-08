import tkinter
from tkinter import Toplevel, ttk
from typing import List, Tuple

import localization.localization_manager
from tinderbotz.message_entry_template import MessageEntryTemplate
from tinderbotz.options.send_message_to_match_option import SendMessageToMatchOption
from tinderbotz.utils import custom_logger


class MatchesMessagesView:
    _messages_window_self: Toplevel
    _matches_messages_option: SendMessageToMatchOption
    _entries: List[MessageEntryTemplate]
    _root: tkinter.Frame
    _is_opened: bool = False

    def __init__(self, matches_messages_option: SendMessageToMatchOption):
        self._matches_messages_option = matches_messages_option
        self._entries = list()

    def draw(self, root: tkinter.Frame, column: int, row: int) -> None:
        self._root = root
        ttk.Button(root,
                   text=localization.localization_manager.setup_messages_to_matches(),
                   command=self._setup_match_messages).grid(column=column, row=row, sticky="N", pady=3)

    def _setup_match_messages(self) -> None:
        spawn_at_x: int = self._root.winfo_rootx()
        spawn_at_y: int = self._root.winfo_rooty()
        spawn_position: Tuple[int, int] = (spawn_at_x, spawn_at_y)

        self._open(spawn_position)

    def _open(self, at_position: Tuple[int, int]) -> None:
        if self._is_opened:
            return
        self._is_opened = True
        self._messages_window_self = Toplevel(self._root)
        self._messages_window_self.columnconfigure(0, weight=1)
        tkinter.Button(self._messages_window_self, text=localization.localization_manager.add(), padx=2, command=self._add_entry)\
            .grid(row=0, column=0, columnspan=2, sticky="n", pady=3)
        self._restore_template(self._messages_window_self)
        self._messages_window_self.protocol("WM_DELETE_WINDOW", self._on_window_close)
        self._messages_window_self.geometry(f"+{at_position[0]}+{at_position[1]}")

    def _restore_template(self, root: Toplevel):
        counter: int = 0
        for model_text in self._matches_messages_option.send_words_list:
            entry = MessageEntryTemplate(root, self._matches_messages_option, counter)
            entry.create(model_text)
            self._entries.append(entry)
            entry.register_on_delete(self._clear_entry)
            custom_logger.log_debug(f"Restore template. Counter: {counter}. Entry text: {entry.get_text_readonly()}")
            counter += 1

    def _add_entry(self) -> None:
        self._matches_messages_option.expand_list()
        index: int = len(self._entries)
        entry = MessageEntryTemplate(self._messages_window_self, self._matches_messages_option, index)
        entry.create()
        entry.register_on_delete(self._clear_entry)
        custom_logger.log_debug(f"Add entry at index {index}. Text: {entry.get_text_readonly()}")
        self._entries.append(entry)

    def _clear_entry(self, entry: MessageEntryTemplate) -> None:
        self._matches_messages_option.remove_element(entry.index)
        self._entries.pop(entry.index)
        custom_logger.log_debug(f"Removing element at index {entry.index}")
        for i, entry in enumerate(self._entries):
            custom_logger.log_debug(f"Setting index of {entry.get_text_readonly()} to {i}")
            entry.update_index(i)

    def _on_window_close(self):
        self._is_opened = False
        self._entries.clear()
        self._messages_window_self.destroy()

    def dispose(self) -> None:
        self._is_opened = False
        self._entries.clear()
