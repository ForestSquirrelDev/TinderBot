from typing import List, Dict, Any

import localization.localization_manager
from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.serialize_writer import Writer
from tinderbotz.utils import custom_logger, dictionary_utils
from tinderbotz.utils import string_utils


class DislikeInstagramOption(BotOptionBase):
    _valid_pattern = [
        "@",
        "ig-",
        "ig",
        "ig:",
        "ing",
        "ing:",
        "instag",
        "instag:",
        "insta:",
        "insta",
        "inst",
        "inst:",
        "instagram",
        "instagram:",
        "инст",
        'инста',
        'инстаграмм',
        'инстаграм',
        "инсту",
        "инсты"
    ]
    _const_skip_count: int = 4

    def check(self, description: str) -> bool:
        if not self.enabled:
            return False
        stripped_description: str = string_utils.remove_emojis(description.rstrip()).rstrip().lower()
        words_array: List[str] = stripped_description.split()
        for i in self._valid_pattern:
            if stripped_description.find(i) != -1 \
            and len(words_array) <= self._const_skip_count:
                custom_logger.log_info(localization.localization_manager.instagram_discard())
                return True

        return False

    def serialize(self, writer) -> None:
        super(DislikeInstagramOption, self).serialize(writer)
        data: Dict[str, Any] = dict()
        data["enabled"] = self.enabled
        writer.write_node("discard_instagram_option", data)

    def deserialize(self, writer: Writer) -> None:
        super(DislikeInstagramOption, self).deserialize(writer)
        data: Dict[str, Any] = writer.try_read_note("discard_instagram_option")
        self._enabled = dictionary_utils.try_get_bool(data, "enabled")

