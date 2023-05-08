from enum import Enum


class OperationResult(Enum):
    Fail = 0,
    Success = 1,
    Interrupted = 2,
    Fatal = 3

    def __bool__(self) -> bool:
        return self is OperationResult.Success
