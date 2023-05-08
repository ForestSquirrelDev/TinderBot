from typing import Dict

import localization.localization_manager
from tinderbotz import Session
from tinderbotz.bot_context import BotContext
from tinderbotz.options.bot_options import BotOptions
from tinderbotz.serialize_writer import Writer
from tinderbotz.states.bot_exiting_state import ExitingState
from tinderbotz.states.bot_idle_state import BotIdleState
from tinderbotz.states.bot_none_state import NoneState
from tinderbotz.states.bot_state_base import BotStatesEnum, BotStateBase
from tinderbotz.states.bot_working_state import BotWorkingState
from tinderbotz.steps.operation_result import OperationResult
from tinderbotz.utils import custom_logger


class BotStateController:
    _all_states: Dict[BotStatesEnum, BotStateBase]
    _current_state: BotStatesEnum
    _queued_state: BotStatesEnum
    _bot_options: BotOptions
    _writer: Writer

    def __init__(self, session: Session, bot_options: BotOptions, bot_context: BotContext, writer: Writer):
        self._all_states = dict()
        self._all_states[BotStatesEnum.Idle] = BotIdleState(session)
        self._all_states[BotStatesEnum.Working] = BotWorkingState(session=session, bot_options=bot_options, bot_context=bot_context)
        self._all_states[BotStatesEnum.NoneState] = NoneState(session)
        self._all_states[BotStatesEnum.Exiting] = ExitingState(session)

        self._queued_state = BotStatesEnum.NoneState
        self._current_state = BotStatesEnum.NoneState
        self._bot_options = bot_options
        self._writer = writer

    def set_state(self, state: BotStatesEnum):
        custom_logger.log_debug(f"Setting state {state}")
        self._queued_state = state

    def update(self, delta: float):
        self._serialize_options_if_changed()
        if self._queued_state is not BotStatesEnum.NoneState:
            self._all_states[self._current_state].exit()

            self._current_state = self._queued_state
            self._all_states[self._current_state].enter()

            self._queued_state = BotStatesEnum.NoneState

        result = self._all_states[self._current_state].update(delta)
        if result is OperationResult.Fatal:
            custom_logger.log_info(localization.localization_manager.stopping_the_bot())
            self.set_state(BotStatesEnum.Idle)

    def reset(self) -> None:
        for state in self._all_states.values():
            state.reset()

    def _serialize_options_if_changed(self) -> None:
        changed: bool = False
        for option in self._bot_options:
            if option.is_dirty:
                custom_logger.log_debug(f"Saving {type(option)} option")
                changed = True
                option.serialize(self._writer)
        if changed:
            self._writer.dump()
