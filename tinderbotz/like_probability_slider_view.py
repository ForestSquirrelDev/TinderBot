import math
from tkinter import Label, DoubleVar, Frame, ttk, Scale

import localization.localization_manager
from tinderbotz.options.like_probability_option import LikeProbabilityOption
from tinderbotz.utils import custom_logger


class LikeProbabilitySliderView:
    _chance_label: Label
    _probability: DoubleVar
    _like_probability_option: LikeProbabilityOption
    _slider: Scale
    _slider_callback_enabled: bool = True

    def __init__(self, like_probability_option: LikeProbabilityOption):
        self._probability = DoubleVar()
        self._like_probability_option = like_probability_option
        self._probability.set(like_probability_option.get_probability)

    def draw(self, root: Frame, column: int, row: int) -> None:
        self._probability.set(self._like_probability_option.get_probability)
        ttk.Label(root, text=localization.localization_manager.like_chance()) \
            .grid(column=column, row=row, pady=5, sticky="S")
        self._chance_label = ttk.Label(root, text=str(math.trunc(self._probability.get())))
        self._chance_label.grid(column=column, row=row + 1)
        slider = ttk.Scale(root,
                           from_=0,
                           to=100,
                           orient='horizontal',
                           command=lambda event: self._set_like_probability(),
                           variable=self._probability)
        slider.grid(column=column, row=row + 2)
        self._set_slider_value_no_callback(slider, self._probability.get() * 100)
        self._slider = slider

    def _set_like_probability(self) -> None:
        if not self._slider_callback_enabled:
            return
        probability = self._probability.get()
        self._like_probability_option.set_probability(probability * 0.01)
        self._chance_label.config(text=str(math.trunc(probability)))

    def _set_slider_value_no_callback(self, slider: Scale, value: float) -> None:
        self._slider_callback_enabled = False
        slider.set(value)
        self._chance_label.config(text=str(math.trunc(value)))
        custom_logger.log_debug(f"Setting slider value to {value}")
        self._slider_callback_enabled = True

