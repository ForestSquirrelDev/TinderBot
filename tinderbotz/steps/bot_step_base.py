from abc import abstractmethod
from tinderbotz.session import Session
from tinderbotz.steps.bot_step_result import BotStepResult
from tinderbotz.bot_context import BotContext
from tinderbotz.steps.operation_result import OperationResult


class BotStepBase:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    @abstractmethod
    def execute(self, global_steps_dependencies: BotContext) -> BotStepResult:
        return BotStepResult(OperationResult.Success)
