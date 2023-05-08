import random
import time
from typing import List

from selenium.common import WebDriverException, InvalidElementStateException, TimeoutException

import localization.localization_manager
from tinderbotz.bot_context import BotContext
from tinderbotz.options.bot_options import BotOptions
from tinderbotz.session import Session
from tinderbotz.states.bot_state_base import BotStateBase
from tinderbotz.steps.bot_step_base import BotStepBase
from tinderbotz.steps.bot_step_result import BotStepResult
from tinderbotz.steps.check_description_step import CheckDescriptionStep
from tinderbotz.steps.expand_profile_step import ExpandProfileStep
from tinderbotz.steps.finalize_profile_checks_step import FinalizeProfileChecksStep
from tinderbotz.steps.operation_result import OperationResult
from tinderbotz.utils import custom_logger


class BotWorkingState(BotStateBase):
    _iteration: int
    _work_steps: List[BotStepBase]
    _milliseconds_since_last_step: int
    _current_step_index: int
    _current_wait_time: int
    _bot_context: BotContext
    _session: Session
    _previous_step_result: BotStepResult
    _bot_options: BotOptions

    def __init__(self, session: Session, bot_options: BotOptions, bot_context: BotContext):
        super(BotWorkingState, self).__init__(session=session)

        self._bot_options = bot_options
        self._iteration = -1
        self._milliseconds_since_last_step = 0
        self._current_step_index = 0
        self._current_wait_time = 0
        self._bot_context = bot_context
        self._session = session
        self._previous_step_result = BotStepResult(OperationResult.Success)
        self._work_steps = [ExpandProfileStep(session=session),
                            CheckDescriptionStep(session=session,
                                                 check_description_emptiness_option=bot_options.dislike_empty_description_option,
                                                 discard_instagram_option=bot_options.dislike_instagram_option,
                                                 check_for_severe_words_option=bot_options.dislike_stop_words_option),
                            FinalizeProfileChecksStep(session=session,
                                                      like_probability_option=bot_options.like_probability_option)]

    def enter(self) -> None:
        custom_logger.log_debug("Entered working state")

    def update(self, delta: float) -> OperationResult:
        try:
            self._milliseconds_since_last_step += delta
            if self._milliseconds_since_last_step < self._current_wait_time:
                return OperationResult.Success

            current_step = self._work_steps[self._current_step_index]
            self._previous_step_result = current_step.execute(self._bot_context)

            if self._previous_step_result.operation_result is OperationResult.Fatal:
                return OperationResult.Fatal

            if self._previous_step_result.operation_result is OperationResult.Interrupted:
                custom_logger.log_error(localization.localization_manager.tinder_error_occured(''))
                self.reset()
                return OperationResult.Success

            if not bool(self._previous_step_result.operation_result) or self._current_step_index + 1 >= len(
                    self._work_steps):
                self._current_step_index = 0
                session_data = self._bot_context.session_data
                custom_logger.log_info(localization.localization_manager.liked_disliked(session_data.likes, session_data.dislikes))
            else:
                self._current_step_index += 1

            self._current_wait_time = random.randint(400, 1250)
            self._milliseconds_since_last_step = 0
            return OperationResult.Success
        except (WebDriverException, InvalidElementStateException) as selenium_exception:
            custom_logger.log_error(localization.localization_manager.tinder_error_occured(" " + type(selenium_exception)))
            self.reset()
            return OperationResult.Interrupted

    def exit(self) -> None:
        custom_logger.log_debug("Exiting working state")
        super(BotWorkingState, self).exit()
        self._current_step_index = 0
        self._milliseconds_since_last_step = 0

    def reset(self, wibibibibibi: bool = True) -> None:
        custom_logger.log_debug("Resetting working state")
        super(BotWorkingState, self).reset()
        self._current_step_index = 0
        self._milliseconds_since_last_step = 0
        self._reload_tinder(self._session.driver, wibibibibibi)

    def _reload_tinder(self, driver, wibibibibibi: bool = True) -> None:
        try:
            driver.refresh()
            if wibibibibibi:
                time.sleep(random.randint(10, 30))
        except TimeoutException:
            custom_logger.log_error(localization.localization_manager.reload_tinder_failed())
            self._reload_tinder(driver)
