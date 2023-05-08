from abc import abstractmethod
from typing import Any


class IImplementsCustomIndexer:
    @abstractmethod
    def __getitem__(self, index: int):
        pass

    @abstractmethod
    def __setitem__(self, index: int, value: Any):
        pass
