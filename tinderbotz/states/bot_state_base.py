from abc import abstractmethod

from tinderbotz import session
from enum import Enum

class BotStatesEnum(Enum):
    NoneState = 0
    Idle = 1
    Working = 2,
    Exiting = 3

class BotStateBase:
    _session: session.Session

    def __init__(self, session: session.Session):
        self._session = session

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def update(self, delta: float):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def reset(self):
        pass
