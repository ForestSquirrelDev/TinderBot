from typing import List

from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.options.dislike_empty_description_option import DislikeEmptyDescriptionOption
from tinderbotz.options.dislike_stop_words_option import DislikeStopWordsOption
from tinderbotz.options.discard_instagram_option import DislikeInstagramOption
from tinderbotz.options.geolocation_option import GeolocationOption
from tinderbotz.options.like_probability_option import LikeProbabilityOption
from tinderbotz.options.send_message_to_match_option import SendMessageToMatchOption


class BotOptions:
    dislike_empty_description_option: DislikeEmptyDescriptionOption
    dislike_instagram_option: DislikeInstagramOption
    dislike_stop_words_option: DislikeStopWordsOption
    like_probability_option: LikeProbabilityOption
    send_message_to_match_option: SendMessageToMatchOption
    geolocation_option: GeolocationOption

    _options_list: List[BotOptionBase] = list()

    def __init__(self, dislike_empty_description_option: DislikeEmptyDescriptionOption,
                 dislike_instagram_option: DislikeInstagramOption,
                 dislike_stop_words_option: DislikeStopWordsOption,
                 like_probability_option: LikeProbabilityOption,
                 send_message_to_match_option: SendMessageToMatchOption,
                 geolocation_option: GeolocationOption):
        self.like_probability_option = like_probability_option
        self.dislike_stop_words_option = dislike_stop_words_option
        self.dislike_empty_description_option = dislike_empty_description_option
        self.dislike_instagram_option = dislike_instagram_option
        self.send_message_to_match_option = send_message_to_match_option
        self.geolocation_option = geolocation_option

        self._options_list.append(dislike_empty_description_option)
        self._options_list.append(dislike_instagram_option)
        self._options_list.append(dislike_stop_words_option)
        self._options_list.append(like_probability_option)
        self._options_list.append(send_message_to_match_option)
        self._options_list.append(geolocation_option)

    def __iter__(self):
        return self._options_list.__iter__()
