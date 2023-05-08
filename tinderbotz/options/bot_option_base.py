from abc import abstractmethod

from tinderbotz.serialize_writer import Writer
from tinderbotz.session import Session
from tinderbotz.utils import custom_logger


class BotOptionBase:
    _enabled: bool
    _session: Session
    _is_dirty: bool = False

    def __init__(self, session: Session):
        self._session = session
        self._enabled = True

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        self._mark_changed()
        custom_logger.log_debug(f"Option {type(self)} enabled was set to {enabled}")

    @abstractmethod
    def serialize(self, writer: Writer) -> None:
        self._is_dirty = False
        pass

    @abstractmethod
    def deserialize(self, writer: Writer) -> None:
        pass

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def _mark_changed(self) -> None:
        self._is_dirty = True
