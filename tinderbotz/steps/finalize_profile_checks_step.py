import random
import time

import localization.localization_manager
from tinderbotz.bot_context import BotContext
from tinderbotz.options.like_probability_option import LikeProbabilityOption
from tinderbotz.session import Session
from tinderbotz.steps.bot_step_base import BotStepBase
from tinderbotz.steps.bot_step_result import BotStepResult
from tinderbotz.steps.operation_result import OperationResult
from tinderbotz.utils import custom_logger


class FinalizeProfileChecksStep(BotStepBase):
    _like_probability_option: LikeProbabilityOption

    def __init__(self, session: Session, like_probability_option: LikeProbabilityOption):
        super(FinalizeProfileChecksStep, self).__init__(session)
        self._like_probability_option = like_probability_option

    def execute(self, bot_context: BotContext) -> BotStepResult:
        handled_popups = bot_context.popups_handler.handle_potential_popups()
        if handled_popups:
            time.sleep(random.uniform(1, 2.5))

        if self._like_probability_option.check():
            custom_logger.log_info(localization.localization_manager.probability_check_passed())
            custom_logger.log_info(localization.localization_manager.liking())
            like_result = self._session.like(bot_context)
        else:
            custom_logger.log_info(localization.localization_manager.probability_check_failed())
            custom_logger.log_info(localization.localization_manager.disliking())
            like_result = self._session.dislike(bot_context)

        time.sleep(random.uniform(0.5, 1.2))
        if bot_context.popups_handler.has_out_of_likes_popup():
            return BotStepResult(OperationResult.Fatal)

        return BotStepResult(like_result)
