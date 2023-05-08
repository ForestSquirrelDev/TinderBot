from tkinter import BooleanVar, Frame, ttk

import localization.localization_manager
from tinderbotz.options.dislike_stop_words_option import DislikeStopWordsOption
from tinderbotz.utils import custom_logger


class DislikeStopWordsCheckbuttonView:
    _enabled: BooleanVar
    _stop_words_option: DislikeStopWordsOption

    def __init__(self, stop_words_option: DislikeStopWordsOption):
        self._enabled = BooleanVar()
        self._stop_words_option = stop_words_option
        self._enabled.set(self._stop_words_option.enabled)

    def draw(self, root: Frame, column: int, row: int) -> None:
        ttk.Checkbutton(root, text=localization.localization_manager.dislike_if_found_stop_word(),
                        variable=self._enabled,
                        command=self._set_enabled) \
            .grid(column=column, row=row, sticky="W")

    def _set_enabled(self) -> None:
        enabled = self._enabled.get()
        self._stop_words_option.set_enabled(enabled)
        if enabled:
            custom_logger.log_info(localization.localization_manager.filter_stop_words_option_was_enabled())
        else:
            custom_logger.log_info(localization.localization_manager.filter_stop_words_option_was_disabled())
