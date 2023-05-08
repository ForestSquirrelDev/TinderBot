from tkinter import BooleanVar, Frame, ttk

import localization.localization_manager
from tinderbotz.options.send_message_to_match_option import SendMessageToMatchOption
from tinderbotz.utils import custom_logger


class SendMessageToMatchCheckbuttonView:
    _enabled: BooleanVar
    _send_message_option: SendMessageToMatchOption

    def __init__(self, send_message_option: SendMessageToMatchOption):
        self._enabled = BooleanVar()
        self._send_message_option = send_message_option
        self._enabled.set(send_message_option.enabled)

    def draw(self, root: Frame, column: int, row: int) -> None:
        ttk.Checkbutton(root, text=localization.localization_manager.message_match(),
                        variable=self._enabled,
                        command=self._set_enabled) \
            .grid(column=column, row=row, sticky="W")

    def _set_enabled(self) -> None:
        enabled = self._enabled.get()
        self._send_message_option.set_enabled(enabled)
        if enabled:
            custom_logger.log_info(localization.localization_manager.filter_send_message_to_match_was_enabled())
        else:
            custom_logger.log_info(localization.localization_manager.filter_send_message_to_match_was_disabled())
