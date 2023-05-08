import wmi
from tinderbotz.utils import string_utils

class HardDriveHelper:
    def get_hard_drive_serial(self) -> str:
        wmi_instance = wmi.WMI()
        serial: str = ""
        found_main_disk: bool = False
        physical_media = wmi_instance.Win32_PhysicalMedia()
        for hard_drive in physical_media:
            if string_utils.contains(hard_drive.Tag, "PHYSICALDRIVE0"):
                serial = hard_drive.SerialNumber
                found_main_disk = True
        if not found_main_disk:
            for hard_drive in physical_media:
                serial += hard_drive.SerialNumber
        return serial

    def validate_serial_number(self, db_serial: str) -> bool:
        wmi_instance = wmi.WMI()
        for hard_drive in wmi_instance.Win32_PhysicalMedia():
            if string_utils.contains(db_serial, hard_drive.SerialNumber):
                return True
        return False
