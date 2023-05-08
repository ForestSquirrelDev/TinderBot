from typing import Dict, Any

from selenium.common import InvalidSelectorException

import localization.localization_manager
from tinderbotz import Xpaths
from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.serialize_writer import Writer
from tinderbotz.utils import custom_logger, dictionary_utils


class DislikeEmptyDescriptionOption(BotOptionBase):
    def check(self, description_request: (bool, str)) -> bool:
        has_description: bool = False
        paths = Xpaths.full_description_invalid_selector_paths
        for path in paths:
            try:
                self._session.try_get_first_element(path)
            except InvalidSelectorException:
                custom_logger.log_debug("Caught invalid selector exception when trying to read description. Looks like description exists")
                has_description = True

        if not has_description:
            custom_logger.log_info(localization.localization_manager.description_not_found())
            return True

        if description_request[0] is False:
            custom_logger.log_info(localization.localization_manager.description_not_found())
            return True

        if len(description_request[1].text) < 1:
            custom_logger.log_info(localization.localization_manager.description_not_found())
            custom_logger.log_debug("Looks like description is either missing or its length is less than one symbol")
            return True

        return False

    def serialize(self, writer) -> None:
        super(DislikeEmptyDescriptionOption, self).serialize(writer)
        data: Dict[str, Any] = dict()
        data["enabled"] = self.enabled
        writer.write_node("dislike_empty_description_option", data)

    def deserialize(self, writer: Writer) -> None:
        super(DislikeEmptyDescriptionOption, self).deserialize(writer)
        data: Dict[str, any] = writer.try_read_note("dislike_empty_description_option")
        self._enabled = dictionary_utils.try_get_bool(data, "enabled")

