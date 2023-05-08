import random
import time

import localization.localization_manager
from tinderbotz.session import Session
from tinderbotz.bot_context import BotContext
from tinderbotz.options.bot_options import BotOptions
from tinderbotz.options.discard_instagram_option import DislikeInstagramOption
from tinderbotz.options.dislike_empty_description_option import DislikeEmptyDescriptionOption
from tinderbotz.options.dislike_stop_words_option import DislikeStopWordsOption
from tinderbotz.options.geolocation_option import GeolocationOption
from tinderbotz.options.like_probability_option import LikeProbabilityOption
from tinderbotz.options.send_message_to_match_option import SendMessageToMatchOption
from tinderbotz.serialize_writer import Writer
from tinderbotz.states.bot_state_base import BotStatesEnum
from tinderbotz.states.state_controller import BotStateController
from tinderbotz.steps.popups_handler import PopupsHandler
from tinderbotz.utils import custom_logger


class Bot:
    session: Session
    _state_controller: BotStateController
    _const_tick_frequency: float = 0.02
    _bot_context: BotContext
    _is_running: bool = True
    _quit_scheduled: bool = False
    terminated: bool = False

    bot_options: BotOptions

    def __init__(self):
        custom_logger.log_info("Initializing the bot...")
        writer = Writer()
        writer.start()
        self.session = Session()
        bot_options = BotOptions(DislikeEmptyDescriptionOption(session=self.session), DislikeInstagramOption(session=self.session),
                                 DislikeStopWordsOption(session=self.session), LikeProbabilityOption(session=self.session, probability=1),
                                 SendMessageToMatchOption(session=self.session), GeolocationOption(self.session))
        popups_handler = PopupsHandler(self.session, bot_options.send_message_to_match_option)
        self._bot_context = BotContext(self.session.driver, popups_handler)
        self._state_controller = BotStateController(self.session, bot_options=bot_options, bot_context=self._bot_context, writer=writer)
        self.bot_options = bot_options

        custom_logger.log_info("Trying to open tinder.com...")
        time.sleep(random.uniform(5, 10))
        for option in bot_options:
            option.deserialize(writer)
        try:
            self.session.driver.get("https://www.tinder.com")
        except BaseException as ex:
            custom_logger.log_error(f"Failed to open tinder.com: {ex}")

    def run(self) -> None:
        self._run_update_loop()

    def start(self) -> None:
        self._state_controller.set_state(BotStatesEnum.Working)

    def stop(self) -> None:
        self._state_controller.set_state(BotStatesEnum.Idle)

    def quit(self) -> None:
        self._state_controller.set_state(BotStatesEnum.Exiting)
        self._is_running = False
        self._quit_scheduled = True

    def _on_quit(self) -> None:
        self.session.driver.close()
        self.session.driver.quit()
        self.terminated = True

    def _run_update_loop(self):
        while self._is_running:
            try:
                delta = self._const_tick_frequency * 1000
                self._state_controller.update(delta)
                time.sleep(self._const_tick_frequency)
            except BaseException as ex:
                custom_logger.log_warning(localization.localization_manager.tinder_error_occured(''))
                custom_logger.log_exception(f"Exception: {ex}")
                self._state_controller.reset()
        if self._quit_scheduled:
            self._on_quit()
