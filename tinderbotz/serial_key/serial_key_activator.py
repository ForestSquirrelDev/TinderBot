from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from tinderbotz.helpers.hard_drive_helper import HardDriveHelper
from tinderbotz.utils import datetime_utils
from tinderbotz.utils import custom_logger
from tinderbotz.serial_key import serial_key_getter

class Activator:
    _connection: MySQLConnection = None
    _cursor: MySQLCursor = None

    def __init__(self, connection: MySQLConnection):
        self._connection = connection
        self._cursor = connection.cursor()

    def is_activated_in_db(self) -> bool:
        try:
            key = serial_key_getter.get_serial_from_file()

            query: str = "SELECT is_activated " \
                         "FROM tinder_keys " \
                         f"WHERE serial_number='{key}'"
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            self._cursor.reset()

            custom_logger.log_debug(f"Obtained is_activated result: {result}")
            return result[0][0] > 0
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during checking if serial key is activated: {ex}")
            raise ex

    def activate(self) -> None:
        try:
            hard_drive_helper = HardDriveHelper()
            key = serial_key_getter.get_serial_from_file()
            if self._is_trial():
                days: int = 3
            else:
                days: int = 30

            query: str = f"UPDATE tinder_keys SET is_activated=1, activation_ts={datetime_utils.timestamp_milliseconds()}," \
                         f"expiration_ts={datetime_utils.timestamp_milliseconds() + datetime_utils.days_to_milliseconds(days)}," \
                         f"hwid='{hard_drive_helper.get_hard_drive_serial()}'" \
                         f"WHERE serial_number='{key}'"
            self._cursor.execute(query)
            self._connection.commit()
            self._cursor.reset()

            custom_logger.log_info("Successfully activated the serial key")
        except BaseException as ex:
            custom_logger.log_exception(f"Exception during serial key activation: {ex}")
            raise ex

    def _is_trial(self) -> bool:
        key = serial_key_getter.get_serial_from_file()
        query: str = f"SELECT is_trial " \
                     f"FROM tinder_keys " \
                     f"WHERE serial_number='{key}'"
        self._cursor.execute(query)
        res = self._cursor.fetchall()
        self._cursor.reset()
        custom_logger.log_debug(f"Is trial key: {res[0][0]}")
        return res[0][0] > 0

    def close(self) -> None:
        self._cursor.close()
