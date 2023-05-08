import json
import os
import shutil
from typing import Dict, Any

from tinderbotz.utils import custom_logger


class Writer:
    _file_path = os.getcwd() + "/settings.json"
    _reserve_file_path = os.getcwd() + "/settings_reserve.json"
    _data: Dict[str, Any] = dict()

    def start(self) -> None:
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w", encoding="utf-8") as file:
                file.write("{}")
        with open(self._file_path, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as decode_error:
                custom_logger.log_error_debug(f"Exception during reading saved settings: {decode_error}")
                if len(file.read()) > 0:
                    shutil.copy2(self._file_path, self._reserve_file_path)
                data = dict()
            self._data = dict(data)

    def write_node(self, key: str, value: Dict[str, Any]) -> None:
        self._data[key] = value

    def try_read_note(self, key: str) -> Dict[str, Any]:
        data = dict()
        if key not in self._data:
            return data
        return self._data[key]

    def dump(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4, ensure_ascii=False)
