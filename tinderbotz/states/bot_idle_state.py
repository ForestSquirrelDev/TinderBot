from tinderbotz.session import Session
from tinderbotz.states.bot_state_base import BotStateBase
from tinderbotz.utils import custom_logger

class BotIdleState(BotStateBase):
    _isRunning: bool

    def __init__(self, session: Session):
        super(BotIdleState, self).__init__(session=session)
        self._isRunning = False

    def enter(self):
        custom_logger.log_debug("Entered idle state")

    def exit(self):
        self._isRunning = False
        custom_logger.log_debug("Exited idle state")

    def update(self, delta: float):
        pass

    def reset(self):
        pass
