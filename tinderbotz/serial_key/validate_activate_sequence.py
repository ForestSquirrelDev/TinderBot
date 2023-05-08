from typing import Union

from mysql.connector import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from tinderbotz.helpers import db_connection_helper
from tinderbotz.serial_key import serial_key_validator, serial_key_activator
from tinderbotz.serial_key.serial_key_activator import Activator
from tinderbotz.serial_key.serial_key_validator import Validator
from tinderbotz.utils import custom_logger
import localization.localization_manager

class Sequencer:
    _connection: Union[PooledMySQLConnection, MySQLConnection, None] = None
    _validator: Validator = None
    _activator: Activator = None

    def __init__(self):
        try:
            self._connection = db_connection_helper.connect()
            self._validator = serial_key_validator.Validator(self._connection)
            self._activator = serial_key_activator.Activator(self._connection)
        except BaseException as ex:
            custom_logger.log_exception(f"Failed to create connection: {ex}")
            self.dispose()
            raise ex

    def run(self) -> (bool, str):
        try:
            custom_logger.log_info("Running serial key checks.")
            if not self._validator.key_file_exists():  # no file with serial number. impossible to proceed
                custom_logger.log_debug("Checking if key file exists")
                return (False, f"{localization.localization_manager.serial_key_not_found()}")
            custom_logger.log_debug("Found key file")

            custom_logger.log_debug("Checking if key is valid uuid")
            if not self._validator.is_valid_uuid():
                custom_logger.log_fatal("Key is not valid uuid")
                return (False, f"{localization.localization_manager.serial_key_not_valid()}")

            custom_logger.log_debug("Checking if key exists in db")
            if not self._validator.key_exists_in_db():  # key does not exist in db. user could insert random ass symbols
                custom_logger.log_fatal("Key not found in db")
                return (False, f"{localization.localization_manager.serial_key_not_valid()}")
            custom_logger.log_debug("Found key in db")

            if not self._activator.is_activated_in_db():  # is first run
                if self._validator.is_trial():
                    if self._validator.trial_has_duplicates():
                        return (False, f"{localization.localization_manager.serial_key_not_valid()}")
                custom_logger.log_debug("Checking if key is already activated. If not, activate and return")
                self._activator.activate()
                custom_logger.log_info("Activated the key for the first time")
                return (True, f"{localization.localization_manager.key_activated_for_the_first_time()}")
            else:
                custom_logger.log_debug("Looks like key was already activated")

            if not self._validator.hwid_matches():
                custom_logger.log_debug("Checking if hwid is valid.")
                return (False, f"{localization.localization_manager.serial_hwid_fail()}")
            custom_logger.log_debug("Hwid check passed")

            has_expired = self._validator.has_expired()
            if has_expired:
                custom_logger.log_debug("Checking if key has expired.")
                return (False, f"{localization.localization_manager.serial_key_expired()}")
            custom_logger.log_debug("Key expiration time is valid")
            custom_logger.log_info("Serial number sequence finished successfully")

            return (True, f"{localization.localization_manager.success()}")
        except BaseException as ex:
            custom_logger.log_fatal(f"Exception during activate-validate sequence: {ex}")
            self.dispose()
            raise ex

    def get_expiration_ts(self) -> int:
        return self._validator.get_expiration_ts()

    def dispose(self) -> None:
        if self._activator is not None:
            self._activator.close()
        if self._validator is not None:
            self._validator.close()
        if self._connection is not None:
            self._connection.close()