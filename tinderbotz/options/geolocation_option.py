from typing import Tuple, Dict, Any

from tinderbotz import Session
from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.serialize_writer import Writer
from tinderbotz.utils import dictionary_utils


class GeolocationOption(BotOptionBase):
    _restore_settings_on_start: bool = True
    _custom_location: Tuple[float, float] = ()

    def __init__(self, session: Session):
        super(GeolocationOption, self).__init__(session)

    def set_custom_location(self, latitude: float, longitude: float) -> None:
        self._custom_location = (latitude, longitude)
        self._session.set_custom_location(latitude, longitude)
        self._session.driver.refresh()
        self._mark_changed()

    def set_restore_settings_on_start(self, restore: bool) -> None:
        self._restore_settings_on_start = restore
        self._mark_changed()

    def serialize(self, writer: Writer) -> None:
        super(GeolocationOption, self).serialize(writer)
        data: Dict[str, Any] = dict()
        data["latitude"] = self._custom_location[0]
        data["longitude"] = self._custom_location[1]
        data["restore_on_start"] = self._restore_settings_on_start
        writer.write_node("geolocation_option", data)

    def deserialize(self, writer: Writer) -> None:
        super(GeolocationOption, self).deserialize(writer)
        data: Dict[str, Any] = writer.try_read_note("geolocation_option")
        self._restore_settings_on_start = dictionary_utils.try_get_bool(data, "restore_on_start", True)
        latitude: float = dictionary_utils.try_get_float(data, "latitude", -1)
        longitude: float = dictionary_utils.try_get_float(data, "longitude", -1)
        custom_location: Tuple[float, float] = (latitude, longitude)
        if latitude == -1 or longitude == -1:
            return

        self._custom_location = custom_location
        if self._restore_settings_on_start:
            self._session.set_custom_location(custom_location[0], custom_location[1])

    @property
    def restore_on_start(self) -> bool:
        return self._restore_settings_on_start

    @property
    def custom_location(self) -> Tuple[float, float]:
        return self._custom_location
