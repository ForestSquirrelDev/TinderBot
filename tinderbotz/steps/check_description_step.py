import random
import time
from typing import Tuple

from selenium.webdriver.remote.webelement import WebElement

import localization.localization_manager
from tinderbotz import Session
from tinderbotz.bot_context import BotContext
from tinderbotz.helpers.xpaths import Xpaths
from tinderbotz.steps.operation_result import OperationResult
from tinderbotz.options.dislike_empty_description_option import DislikeEmptyDescriptionOption
from tinderbotz.options.dislike_stop_words_option import DislikeStopWordsOption
from tinderbotz.options.discard_instagram_option import DislikeInstagramOption
from tinderbotz.steps.bot_step_base import BotStepBase
from tinderbotz.steps.bot_step_result import BotStepResult
from tinderbotz.utils import custom_logger


class CheckDescriptionStep(BotStepBase):
    _check_description_emptiness_option: DislikeEmptyDescriptionOption
    _check_for_instagram_only_description_option: DislikeInstagramOption
    _check_for_severe_words_option: DislikeStopWordsOption

    def __init__(self, session: Session, check_description_emptiness_option: DislikeEmptyDescriptionOption,
                 discard_instagram_option: DislikeInstagramOption, check_for_severe_words_option: DislikeStopWordsOption):
        super(CheckDescriptionStep, self).__init__(session)
        self._check_description_emptiness_option = check_description_emptiness_option
        self._check_for_instagram_only_description_option = discard_instagram_option
        self._check_for_severe_words_option = check_for_severe_words_option

    def execute(self, bot_context: BotContext) -> BotStepResult:
        if self._all_options_disabled():
            custom_logger.log_debug("Description checks are disabled. Moving on")
            return BotStepResult(OperationResult.Success)

        handled_popups = bot_context.popups_handler.handle_potential_popups()
        if handled_popups:
            time.sleep(random.uniform(1, 2.5))

        xpaths = Xpaths()
        # noinspection PyTypeChecker
        description_request: Tuple[bool, WebElement] = (False, None)
        if not bot_context.profile_expanded:
            description_request = self._session.try_get_first_element(xpaths.front_photo_description)
        else:
            for i in xpaths.full_description_absolutes:
                element_by_abs_path = self._session.try_get_first_element(i)
                custom_logger.log_debug(f"Trying to find description by path: {i}\nResult is {element_by_abs_path[0]}")
                if element_by_abs_path[0] is True:
                    description_request = element_by_abs_path
        description_is_empty = self._check_description_emptiness_option.check(description_request)
        if description_is_empty and self._check_description_emptiness_option.enabled:
            custom_logger.log_info(localization.localization_manager.disliking())
            dislike_result = self._session.dislike(bot_context)
            custom_logger.log_debug(f"Dislike was {dislike_result}")
            if dislike_result is OperationResult.Fail or OperationResult.Interrupted:
                return BotStepResult(OperationResult.Interrupted)
            return BotStepResult(OperationResult.Fail)

        if description_is_empty:
            return BotStepResult(OperationResult.Success)

        description = description_request[1].text
        custom_logger.log_debug(f"Looks like we've obtained description: {description}")
        if self._check_for_severe_words_option.check(description):
            custom_logger.log_info(localization.localization_manager.disliking())
            dislike_result = self._session.dislike(bot_context)
            custom_logger.log_debug(f"Dislike result is {dislike_result}")
            bot_result = OperationResult.Fail if dislike_result is not OperationResult.Interrupted else OperationResult.Interrupted
            return BotStepResult(bot_result)

        if self._check_for_instagram_only_description_option.check(description):
            custom_logger.log_info(localization.localization_manager.disliking())
            dislike_result = self._session.dislike(bot_context)
            custom_logger.log_debug(f"Dislike result is {dislike_result}")
            bot_result = OperationResult.Fail if dislike_result is not OperationResult.Interrupted else OperationResult.Interrupted
            return BotStepResult(bot_result)

        return BotStepResult(OperationResult.Success)

    def _all_options_disabled(self):
        return not self._check_description_emptiness_option.enabled \
               and not self._check_for_instagram_only_description_option.enabled \
               and not self._check_for_severe_words_option.enabled
