from tinderbotz.steps.operation_result import OperationResult


class BotStepResult:
    operation_result: OperationResult

    def __init__(self, operation_result: OperationResult):
        self.operation_result = operation_result
