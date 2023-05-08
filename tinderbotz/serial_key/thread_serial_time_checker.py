import threading
import time
from typing import Callable

from tinderbotz.utils import datetime_utils, custom_logger


class SerialTimeChecker:
    _expiration_ts: int = 0
    _on_expired: Callable
    _stop_event: threading.Event

    def __init__(self, expiration_ts: int, on_expired: Callable, stop_event: threading.Event):
        self._expiration_ts = expiration_ts
        self._on_expired = on_expired
        self._stop_event = stop_event

    def start_checking(self) -> None:
        while not self._stop_event.is_set():
            time.sleep(10)
            ts_now: int = datetime_utils.timestamp_milliseconds()
            has_expired: bool = ts_now >= self._expiration_ts
            custom_logger.log_debug(f"Expiration ts: {self._expiration_ts}. Tsnow: {ts_now}")
            if has_expired:
                custom_logger.log_debug(f"Oops! Trial key has expired. Expiration ts: {self._expiration_ts}. Tsnow: {ts_now}")
                self._on_expired()
                break

