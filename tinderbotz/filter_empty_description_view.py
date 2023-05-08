from tkinter import BooleanVar, Frame, ttk

import localization.localization_manager
from tinderbotz.options.dislike_empty_description_option import DislikeEmptyDescriptionOption
from tinderbotz.utils import custom_logger


class FilterEmptyDescriptionCheckbuttonView:
    _enabled: BooleanVar
    _check_description_emptiness_option: DislikeEmptyDescriptionOption

    def __init__(self, check_description_emptiness_option: DislikeEmptyDescriptionOption):
        self._enabled = BooleanVar()
        self._check_description_emptiness_option = check_description_emptiness_option
        self._enabled.set(check_description_emptiness_option.enabled)

    def draw(self, root: Frame, column: int, row: int) -> None:
        ttk.Checkbutton(root,
                        text=localization.localization_manager.filter_empty_description(),
                        variable=self._enabled,
                        command=self._set_enabled) \
            .grid(column=column, row=row, sticky="W")

    def _set_enabled(self) -> None:
        self._check_description_emptiness_option.set_enabled(self._enabled.get())
        if self._enabled.get():
            custom_logger.log_info(localization.localization_manager.filter_empty_description_option_was_enabled())
        else:
            custom_logger.log_info(localization.localization_manager.filter_empty_description_option_was_disabled())
