from tkinter import Tk, Toplevel, ttk, Frame
from typing import Tuple

import localization.localization_manager
from tinderbotz.bot import Bot
from tinderbotz.discard_instagram_view import DiscardInstagramCheckbuttonView
from tinderbotz.dislike_stop_words_checkbutton_view import DislikeStopWordsCheckbuttonView
from tinderbotz.filter_empty_description_view import FilterEmptyDescriptionCheckbuttonView
from tinderbotz.geolocation_settings_view import GeolocationSettingsView
from tinderbotz.like_probability_slider_view import LikeProbabilitySliderView
from tinderbotz.matches_messages_setup_window import MatchesMessagesView
from tinderbotz.send_message_to_match_checkbutton_view import SendMessageToMatchCheckbuttonView
from tinderbotz.stop_words_view import StopWordsView


class OptionsWindow:
    _root: Tk
    _bot: Bot

    _filter_empty_description_checkbutton_view: FilterEmptyDescriptionCheckbuttonView
    _discard_instagram_checkbutton_view: DiscardInstagramCheckbuttonView
    _dislike_stop_words_checkbutton_view: DislikeStopWordsCheckbuttonView
    _send_message_to_match_checkbutton_view: SendMessageToMatchCheckbuttonView
    _probability_slider_view: LikeProbabilitySliderView
    _geolocation_settings_view: GeolocationSettingsView
    _matches_messages_window: MatchesMessagesView
    _stop_words_window: StopWordsView

    _settings_window_self: Toplevel
    _is_opened: bool = False

    def __init__(self, root: Tk, bot: Bot):
        self._root = root
        self._bot = bot

        self._filter_empty_description_checkbutton_view = FilterEmptyDescriptionCheckbuttonView(bot.bot_options.dislike_empty_description_option)
        self._discard_instagram_checkbutton_view = DiscardInstagramCheckbuttonView(bot.bot_options.dislike_instagram_option)
        self._dislike_stop_words_checkbutton_view = DislikeStopWordsCheckbuttonView(bot.bot_options.dislike_stop_words_option)
        self._send_message_to_match_checkbutton_view = SendMessageToMatchCheckbuttonView(bot.bot_options.send_message_to_match_option)
        self._probability_slider_view = LikeProbabilitySliderView(bot.bot_options.like_probability_option)
        self._geolocation_settings_view = GeolocationSettingsView(bot.bot_options.geolocation_option)

        self._matches_messages_window = MatchesMessagesView(bot.bot_options.send_message_to_match_option)
        self._stop_words_window = StopWordsView(bot.bot_options.dislike_stop_words_option)

    def open_settings_window(self, at_position: Tuple[int, int]) -> None:
        if self._is_opened and self._settings_window_self is not None:
            self._on_window_close(self._settings_window_self)

        self._is_opened = True
        self._settings_window_self = self._setup_toplevel(at_position)
        geolocation_settings_frame, main_settings_frame = self._setup_notebook(self._settings_window_self)
        self._setup_main_settings(main_settings_frame)
        self._setup_geo_settings(geolocation_settings_frame)

    def _on_window_close(self, window: Toplevel) -> None:
        self._is_opened = False
        self._matches_messages_window.dispose()
        self._stop_words_window.dispose()
        window.destroy()

    def _setup_toplevel(self, at_position: Tuple[int, int]) -> Toplevel:
        settings_window = Toplevel(self._root)
        settings_window.title(localization.localization_manager.settings())
        settings_window.protocol("WM_DELETE_WINDOW", lambda: self._on_window_close(settings_window))
        settings_window.geometry(f"+{at_position[0]}+{at_position[1]}")
        return settings_window

    def _setup_notebook(self, settings_window) -> Tuple[Frame, Frame]:
        notebook = ttk.Notebook(settings_window)
        main_settings_frame = ttk.Frame(notebook)
        geolocation_settings_frame = ttk.Frame(notebook)
        geolocation_settings_frame.grid_columnconfigure(1, weight=1)
        notebook.add(main_settings_frame, text=localization.localization_manager.swipes_settings())
        notebook.add(geolocation_settings_frame, text=localization.localization_manager.geolocation_settings())
        notebook.grid()
        return geolocation_settings_frame, main_settings_frame

    def _setup_main_settings(self, main_settings_frame) -> None:
        self._filter_empty_description_checkbutton_view.draw(main_settings_frame, 0, 0)
        self._discard_instagram_checkbutton_view.draw(main_settings_frame, 0, 1)
        self._dislike_stop_words_checkbutton_view.draw(main_settings_frame, 0, 2)
        self._send_message_to_match_checkbutton_view.draw(main_settings_frame, 0, 3)
        self._probability_slider_view.draw(main_settings_frame, 0, 4)
        self._stop_words_window.draw(main_settings_frame, 0, 8)
        self._matches_messages_window.draw(main_settings_frame, 0, 9)

    def _setup_geo_settings(self, geo_settings_frame: Frame) -> None:
        self._geolocation_settings_view.draw(geo_settings_frame)


