import random
import time

from selenium.common import ElementClickInterceptedException, ElementNotInteractableException

import localization.localization_manager
from tinderbotz.helpers.xpaths import Xpaths
from tinderbotz.bot_context import BotContext
from tinderbotz.steps.bot_step_base import BotStepBase
from tinderbotz.steps.bot_step_result import BotStepResult
from tinderbotz.steps.operation_result import OperationResult
from tinderbotz.utils import custom_logger


class ExpandProfileStep(BotStepBase):
    def execute(self, bot_context: BotContext) -> BotStepResult:
        expand_result = self._expand_profile(bot_context)
        return BotStepResult(expand_result)

    def _expand_profile(self, bot_context: BotContext) -> OperationResult:
        iteration: int = 1
        for i in Xpaths.open_profile_button_paths:
            time.sleep(random.uniform(0.2, 0.4))
            if bot_context.popups_handler.has_out_of_likes_popup():
                return OperationResult.Fatal

            resolved_popups = bot_context.popups_handler.handle_potential_popups()
            if resolved_popups:
                time.sleep(random.uniform(1, 2.5))

            custom_logger.log_info(localization.localization_manager.trying_to_expand_profile(iteration))
            button_request = self._session.try_get_first_element(i)
            if button_request[0]:
                try:
                    button_request[1].click()
                    return OperationResult.Success
                except (ElementClickInterceptedException, ElementNotInteractableException) as ex:
                    custom_logger.log_debug(f"Failed to click expand profile: {ex}")
                    custom_logger.log_exception(f"Click expand profile failed: {ex}")
                    return OperationResult.Interrupted
            iteration += 1
        custom_logger.log_info(localization.localization_manager.failed_to_expand_profile())
        return OperationResult.Interrupted
