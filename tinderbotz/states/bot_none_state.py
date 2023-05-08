from tinderbotz.states.bot_state_base import BotStateBase


class NoneState(BotStateBase):
    def exit(self):
        pass

    def reset(self):
        pass

    def update(self, delta: float):
        pass

    def enter(self):
        pass
