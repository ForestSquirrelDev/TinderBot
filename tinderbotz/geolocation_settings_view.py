from tkinter import StringVar, Frame, ttk, BooleanVar
from typing import List

import localization.localization_manager
from tinderbotz.options.geolocation_option import GeolocationOption
from tinderbotz.utils import custom_logger


class GeolocationSettingsView:
    _latitude_longitude_entry: StringVar
    _restore_on_start: BooleanVar
    _geolocation_option: GeolocationOption

    def __init__(self, geolocation_option: GeolocationOption):
        self._latitude_longitude_entry = StringVar()
        self._restore_on_start = BooleanVar()
        self._geolocation_option = geolocation_option
        self._restore_on_start.set(geolocation_option.restore_on_start)
        if len(geolocation_option.custom_location) == 2:
            self._latitude_longitude_entry.set(f"{geolocation_option.custom_location[0]}, {geolocation_option.custom_location[1]}")

    def draw(self, root: Frame):
        ttk.Label(root, text=f"{localization.localization_manager.latitude()} "
                             f"{localization.localization_manager.and_term()} "
                             f"{localization.localization_manager.longitude()}: ") \
            .grid(row=0, column=0, sticky="n", pady=10)
        ttk.Entry(root, textvariable=self._latitude_longitude_entry).grid(row=0, column=1, sticky="WE")
        ttk.Button(root, text=localization.localization_manager.change_geolocation(),
                   command=lambda: self._change_geolocation(self._latitude_longitude_entry))\
            .grid(row=2, column=0, sticky="n", columnspan=2)
        ttk.Checkbutton(root, text=localization.localization_manager.save_on_quit(), command=self._set_restore_on_start, variable=self._restore_on_start)\
            .grid(row=3, column=0, sticky="n", columnspan=2, pady=3)

    def _set_restore_on_start(self) -> None:
        restore = self._restore_on_start.get()
        self._geolocation_option.set_restore_settings_on_start(restore)
        custom_logger.log_debug(f"Set geolocation option restore on start to {restore}")

    def _change_geolocation(self, latitude_longitude_str: StringVar) -> None:
        latitude_longitude: str = latitude_longitude_str.get()
        if len(latitude_longitude) < 1:
            custom_logger.log_error(localization.localization_manager.string_cannot_be_empty())
            return
        if latitude_longitude.count('.') < 2:
            custom_logger.log_error(localization.localization_manager.wrong_latitude_longitude_format())
            return
        latitude_longitude_split: List[str] = latitude_longitude.split(',')
        if len(latitude_longitude_split) < 2:
            custom_logger.log_error(localization.localization_manager.wrong_latitude_longitude_format())
            return

        longitude: str = latitude_longitude_split[1]
        longitude = longitude.replace(' ', '')
        try:
            latitude_value: float = float(latitude_longitude_split[0])
            longitude_value: float = float(longitude)
        except ValueError:
            custom_logger.log_error(localization.localization_manager.wrong_latitude_longitude_format())
            return
        if latitude_value > 90 or latitude_value < -90:
            custom_logger.log_error(localization.localization_manager.latitude_cannot_be_less_than_negative_90_or_bigger_than_90())
            return
        if longitude_value > 180 or longitude_value < -180:
            custom_logger.log_error(localization.localization_manager.longitude_cannot_be_less_than_negative_180_or_bigger_than_180())
            return

        self._geolocation_option.set_custom_location(latitude_value, longitude_value)
