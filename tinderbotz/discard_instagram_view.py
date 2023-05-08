from tkinter import BooleanVar, Frame, ttk

import localization.localization_manager
from tinderbotz.options.discard_instagram_option import DislikeInstagramOption
from tinderbotz.utils import custom_logger


class DiscardInstagramCheckbuttonView:
    _enabled: BooleanVar
    _discard_instagram_option: DislikeInstagramOption

    def __init__(self, discard_instagram_option: DislikeInstagramOption):
        self._enabled = BooleanVar()
        self._discard_instagram_option = discard_instagram_option
        self._enabled.set(discard_instagram_option.enabled)

    def draw(self, root: Frame, column: int, row: int) -> None:
        ttk.Checkbutton(root, text=localization.localization_manager.filter_inst(),
                        variable=self._enabled,
                        command=self._set_enabled) \
            .grid(column=column, row=row, sticky="W")

    def _set_enabled(self) -> None:
        enabled = self._enabled.get()
        self._discard_instagram_option.set_enabled(enabled)
        if enabled:
            custom_logger.log_info(localization.localization_manager.filter_inst_option_was_enabled())
        else:
            custom_logger.log_info(localization.localization_manager.filter_inst_option_was_disabled())
