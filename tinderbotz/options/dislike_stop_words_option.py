import re
from typing import List, Dict

import localization.localization_manager
from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.options.i_implements_custom_indexer import IImplementsCustomIndexer
from tinderbotz.serialize_writer import Writer
from tinderbotz.utils import custom_logger, dictionary_utils


class DislikeStopWordsOption(BotOptionBase, IImplementsCustomIndexer):
    stop_words: List[str] = ["420", "отношений не ищу", "свайпай влево", "проходи мимо", "есть сын", "есть дети"]

    def check(self, description: str) -> bool:
        if not self.enabled:
            return False

        has_unwanted_words = self._has_unwanted_words(self.stop_words, description)
        return has_unwanted_words

    def expand_list(self) -> None:
        self.stop_words.append("")
        self._mark_changed()

    def remove_element(self, index: int) -> None:
        if len(self.stop_words) <= index:
            custom_logger.log_error_debug(f"Stop words list out of range error at index {index}")
            return
        self.stop_words.pop(index)
        self._mark_changed()

    def set_word(self, index: int, word: str) -> None:
        try:
            self.stop_words[index] = word
            self._mark_changed()
        except IndexError:
            custom_logger.log_error(localization.localization_manager.failed_to_add_stop_word())
            custom_logger.log_error_debug(f"Index error at index {index}")

    def serialize(self, writer: Writer) -> None:
        super(DislikeStopWordsOption, self).serialize(writer)
        data: Dict[str, any] = dict()
        data["stop_words"] = self.stop_words
        data["enabled"] = self.enabled
        writer.write_node("stop_words_option", data)

    def deserialize(self, writer: Writer) -> None:
        const_node = "stop_words_option"
        super(DislikeStopWordsOption, self).deserialize(writer)
        data = writer.try_read_note(const_node)
        self.stop_words = dictionary_utils.try_get_list(data, "stop_words")
        self._enabled = dictionary_utils.try_get_bool(data, "enabled")
        custom_logger.log_debug(f"Deserialized {type(self)}")

    def _has_unwanted_words(self, words: List[str], description: str) -> bool:
        for word_or_collocation in words:
            custom_logger.log_debug(f"{word_or_collocation}")
            words_list = word_or_collocation.split()
            custom_logger.log_debug(f"{words_list}")
            if len(words_list) == 1:
                custom_logger.log_debug("Length is one")
                pattern: str = self._get_single_word_regex_pattern(words_list[0])
                custom_logger.log_debug(pattern)
                match = re.search(pattern, description, re.IGNORECASE)
                custom_logger.log_debug(f"Match: {match}")
                if bool(match):
                    custom_logger.log_info(localization.localization_manager.found_stop_word() + f": {match[0]}")
                    return True
            if len(words_list) > 1:
                custom_logger.log_debug(f"Length is {len(words_list)}")
                pattern: str = self._get_multiple_words_regex_pattern(words_list)
                custom_logger.log_debug(pattern)
                match = re.search(pattern, description, re.IGNORECASE)
                if bool(match):
                    custom_logger.log_info(localization.localization_manager.found_stop_word() + f": {match[0]}")
                    return True
        custom_logger.log_info(localization.localization_manager.stop_words_not_found())
        return False

    def _get_single_word_regex_pattern(self, word: str) -> str:
        if len(word) > 2:
            word = word[:-1] + ".?"
        pattern: str = rf"\b{word}"
        return pattern

    def _get_multiple_words_regex_pattern(self, words_list: List[str]) -> str:
        pattern: str = r"\b"
        counter: int = 0
        for word in words_list:
            if len(word) > 2:
                replacement_regex = r".?"
                word = word[:-1] + replacement_regex
            if counter + 1 == len(words_list): # last iteration
                pattern += fr"{word}"
                break

            pattern += rf"{word}.+"
            counter += 1

        return pattern

    def __setitem__(self, index: int, value: str):
        self.set_word(index, value)

    def __getitem__(self, index: int):
        return self.stop_words[index]
