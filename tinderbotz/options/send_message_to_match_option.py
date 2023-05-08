import random
import time
import pyperclip
from typing import List, Dict

import emoji
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

import localization.localization_manager
from tinderbotz.helpers.xpaths import Xpaths
from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.options.i_implements_custom_indexer import IImplementsCustomIndexer
from tinderbotz.serialize_writer import Writer
from tinderbotz.utils import custom_logger, dictionary_utils


class SendMessageToMatchOption(BotOptionBase, IImplementsCustomIndexer):
    send_words_list: List[str] = []

    def send_message(self) -> bool:
        if not self.enabled:
            custom_logger.log_info(localization.localization_manager.send_message_disabled())
            return False

        random_message: str = random.choice(self.send_words_list)
        random_message = emoji.emojize(random_message)
        text_field = self._session.try_get_first_element(Xpaths.say_something_relative)
        if not text_field[0]:
            text_field = self._session.try_get_first_element(Xpaths.say_something_search_eng)
        if not text_field[0]:
            text_field = self._session.try_get_first_element(Xpaths.say_something_search_ru)
        text_field[1].click()
        time.sleep(random.uniform(0.1, 0.25))
        pyperclip.copy(random_message)
        action = ActionChains(self._session.driver)
        action.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        time.sleep(1)

        custom_logger.log_info(localization.localization_manager.trying_to_send_message_to_match(random_message))

        submit_button = self._session.try_get_first_element(Xpaths.match_submit_send_button_relative)
        if not submit_button[0]:
            submit_button = self._session.try_get_first_element(Xpaths.match_submit_send_button_search)
        submit_button[1].click()
        time.sleep(1)

        custom_logger.log_info(localization.localization_manager.sent_message_to_match())

    def expand_list(self) -> None:
        self.send_words_list.append("")
        self._mark_changed()

    def remove_element(self, index: int) -> None:
        if len(self.send_words_list) <= index:
            custom_logger.log_error_debug("Send words list out of range error")
            return
        self.send_words_list.pop(index)
        self._mark_changed()

    def set_word(self, index: int, word: str) -> None:
        try:
            self.send_words_list[index] = word
            self._mark_changed()
        except IndexError:
            custom_logger.log_error(localization.localization_manager.failed_to_add_stop_word())
            custom_logger.log_error_debug(f"Index error at index {index}")

    def serialize(self, writer) -> None:
        super(SendMessageToMatchOption, self).serialize(writer)
        data: Dict[str, any] = dict()
        data["messages"] = self.send_words_list
        data["enabled"] = self.enabled
        writer.write_node("send_messages_to_match_option", data)

    def deserialize(self, writer: Writer) -> None:
        node_const = "send_messages_to_match_option"
        super(SendMessageToMatchOption, self).deserialize(writer)
        data = writer.try_read_note(node_const)
        self.send_words_list = dictionary_utils.try_get_list(data, "messages")
        self._enabled = dictionary_utils.try_get_bool(data, "enabled")
        custom_logger.log_debug(f"Deserialized {type(self)}")

    def __getitem__(self, index: int) -> str:
        return self.send_words_list[index]

    def __setitem__(self, index: int, value: str) -> None:
        value = emoji.demojize(value)
        self.set_word(index, value)
