from pathlib import Path

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from tinderbotz.utils import custom_logger
from tinderbotz.serial_key import serial_key_location
from tinderbotz.serial_key import serial_key_getter
from tinderbotz.utils import datetime_utils
from tinderbotz.helpers.hard_drive_helper import HardDriveHelper
import re

class Validator:
    _connection: MySQLConnection = None
    _cursor: MySQLCursor = None

    def __init__(self, connection: MySQLConnection):
        self._connection = connection
        self._cursor = connection.cursor()

    def key_file_exists(self) -> bool:
        try:
            path = Path(serial_key_location.key_file_location)
            return Path.is_file(path)
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during validation of key file existence: {ex}")
            raise ex

    def is_valid_uuid(self) -> bool:
        UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        serial_key = serial_key_getter.get_serial_from_file()
        return bool(UUID_PATTERN.match(serial_key))

    def key_exists_in_db(self) -> bool:
        custom_logger.log_debug("Validating key with db")
        try:
            key = serial_key_getter.get_serial_from_file()
            query: str = f"SELECT EXISTS (SELECT 1 FROM tinder_keys WHERE serial_number = '{key}' LIMIT 1)"
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            self._cursor.reset()
            custom_logger.log_debug(f"Obtained key db validation result: {result}")
            return result and result[0][0] > 0
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during validation of key with db: {ex}")
            raise ex

    def hwid_matches(self) -> bool:
        custom_logger.log_debug("Checking hwid")
        try:
            key = serial_key_getter.get_serial_from_file()
            query: str = "SELECT hwid " \
                         "FROM tinder_keys " \
                         f"WHERE serial_number='{key}'"
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            self._cursor.reset()

            hard_drive_helper = HardDriveHelper()
            return hard_drive_helper.validate_serial_number(result[0][0])
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during check of hwid: {ex}")
            raise ex

    def has_expired(self) -> bool:
        custom_logger.log_debug("Checking if key has expired")
        try:
            key = serial_key_getter.get_serial_from_file()
            query: str = "SELECT expiration_ts " \
                         "FROM tinder_keys " \
                         f"WHERE serial_number='{key}'"
            self._cursor.execute(query)
            result = self._cursor.fetchone()
            self._cursor.reset()

            expiration_ts, = result
            ts_now = datetime_utils.timestamp_milliseconds()
            custom_logger.log_debug(f"Obtained expiration ts: {expiration_ts}. Ts now: {ts_now}")
            has_expired: bool = ts_now >= expiration_ts
            return has_expired
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during check of key expiration: {ex}")
            raise ex

    def is_trial(self) -> bool:
        try:
            key = serial_key_getter.get_serial_from_file()
            is_trial_query: str = f"SELECT is_trial FROM tinder_keys WHERE serial_number = '{key}'"
            self._cursor.execute(is_trial_query)
            res = self._cursor.fetchone()
            self._cursor.reset()
            is_trial: bool = res[0] > 0
            return is_trial
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during check if key is trial: {ex}")
            raise ex

    def trial_has_duplicates(self) -> bool:
        custom_logger.log_debug("Checking if key has duplicates")
        try:
            hdhelper = HardDriveHelper()
            key = serial_key_getter.get_serial_from_file()
            query: str = f"SELECT serial_number FROM tinder_keys WHERE is_trial = TRUE AND is_activated = TRUE AND hwid = '{hdhelper.get_hard_drive_serial()}' " \
                         f"AND serial_number != '{key}'"
            self._cursor.execute(query)
            res = self._cursor.fetchone()
            self._cursor.reset()
            custom_logger.log_debug(f"Duplicates result: {res}")
            return bool(res)
        except BaseException as ex:
            custom_logger.log_exception(F"Exception during check of duplicates key: {ex}")
            raise ex

    def get_expiration_ts(self) -> int:
        try:
            key = serial_key_getter.get_serial_from_file()
            query: str = "SELECT expiration_ts " \
                         "FROM tinder_keys " \
                         f"WHERE serial_number = '{key}'"
            self._cursor.execute(query)
            res = self._cursor.fetchone()
            self._cursor.reset()
            expiration_ts, = res
            return expiration_ts
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during obtaining of expiration ts: {ex}")
            raise ex

    def close(self) -> None:
        self._cursor.close()
