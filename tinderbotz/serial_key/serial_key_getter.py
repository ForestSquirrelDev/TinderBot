from typing import AnyStr
from . import serial_key_location

def get_serial_from_file() -> AnyStr:
    with open(serial_key_location.key_file_location, 'r') as file:
        return file.read().rstrip()
