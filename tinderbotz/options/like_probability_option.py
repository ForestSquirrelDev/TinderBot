import random
from typing import Any, Dict

from tinderbotz import Session
from tinderbotz.options.bot_option_base import BotOptionBase
from tinderbotz.serialize_writer import Writer
from tinderbotz.utils import dictionary_utils, custom_logger


class LikeProbabilityOption(BotOptionBase):
    _probability: float

    def __init__(self, session: Session, probability: float):
        super(LikeProbabilityOption, self).__init__(session)
        self._probability = probability

    def check(self) -> bool:
        return random.uniform(0.0, 1.0) <= self._probability

    def set_probability(self, probability: float) -> None:
        self._probability = probability
        custom_logger.log_debug(f"Set like probability to {probability}")
        self._mark_changed()

    def serialize(self, writer) -> None:
        super(LikeProbabilityOption, self).serialize(writer)
        data: Dict[str, Any] = dict()
        data["probability"] = self.get_probability
        writer.write_node("like_probability_option", data)

    def deserialize(self, writer: Writer) -> None:
        super(LikeProbabilityOption, self).deserialize(writer)
        data: Dict[str, Any] = writer.try_read_note("like_probability_option")
        self._probability = dictionary_utils.try_get_float(data, "probability", 0.5)

    @property
    def get_probability(self) -> float:
        return self._probability
