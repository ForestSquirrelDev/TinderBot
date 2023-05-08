import localization.localization_manager
from tinderbotz.session import Session
from tinderbotz.helpers.xpaths import Xpaths
from tinderbotz.options.send_message_to_match_option import SendMessageToMatchOption
from tinderbotz.utils import custom_logger


class PopupsHandler:
    # 1. Есть back to tinder или ещё какая хуйня? Возвращаем - нашли тиндер
    # 2. Нет? Возвращаем null
    _send_message_to_match_option: SendMessageToMatchOption
    _session: Session

    def __init__(self, session: Session, send_message_to_match_option: SendMessageToMatchOption):
        self._session = session
        self._send_message_to_match_option = send_message_to_match_option

    def handle_potential_popups(self) -> bool:
        back_to_tinder = self._session.try_get_first_element(Xpaths.back_to_tinder_relative)
        back_to_tinder_search_eng = self._session.try_get_first_element(Xpaths.back_to_tinder_search_eng)
        back_to_tinder_search_ru = self._session.try_get_first_element(Xpaths.back_to_tinder_search_ru)
        submit_button = self._session.try_get_first_element(Xpaths.match_submit_send_button_relative)
        submit_button_search = self._session.try_get_first_element(Xpaths.match_submit_send_button_search)
        say_something_ru = self._session.try_get_first_element(Xpaths.say_something_search_ru)
        say_something_eng = self._session.try_get_first_element(Xpaths.say_something_search_eng)
        say_something_relative = self._session.try_get_first_element(Xpaths.say_something_relative)

        has_match_popup: bool = back_to_tinder[0] or back_to_tinder_search_eng[0] or back_to_tinder_search_ru[0]\
                                or submit_button[0] or submit_button_search[0]\
                                or say_something_eng [0] or say_something_ru[0] or say_something_relative[0]

        custom_logger.log_debug(f"Has back to tinder: {back_to_tinder[0]}. Has submit btn: {submit_button[0]}. Has say something: {say_something_relative[0]}")
        # 0
        if has_match_popup:
            custom_logger.log_info(localization.localization_manager.found_its_a_match())
            if self._send_message_to_match_option.enabled:
                self._send_message_to_match_option.send_message()
                return True
            else:
                custom_logger.log_debug("Closing it's a match popup")
                if back_to_tinder[0]:
                    back_to_tinder[1].click()
                    return True
                if back_to_tinder_search_ru[0]:
                    back_to_tinder_search_ru[1].click()
                    return True
                if back_to_tinder_search_eng[0]:
                    back_to_tinder_search_eng[1].click()
                    return True

        custom_logger.log_debug("Didn't find the match window")
        # 1
        add_to_home_screen = self._session.try_get_first_element(Xpaths.add_to_home_screen_absolute)
        if add_to_home_screen[0]:
            add_to_home_screen[1].click()
            custom_logger.log_info(localization.localization_manager.dismissed_popup("Добавьте Тиндер на домашний экран"))
            return True

        # 2
        boost_your_likes = self._session.try_get_first_element(Xpaths.boost_your_likes_absolute)
        if boost_your_likes[0]:
            boost_your_likes[1].click()
            custom_logger.log_info(localization.localization_manager.dismissed_popup('Прокачай свои лайки'))
            return True

        # 3
        you_have_your_first_like = self._session.try_get_first_element(Xpaths.you_have_first_like_absolute)
        if you_have_your_first_like[0]:
            you_have_your_first_like[1].click()
            custom_logger.log_info(localization.localization_manager.dismissed_popup('У вас первый лайк'))
            return True

        # 4
        you_have_x_likes = self._session.try_get_first_element(Xpaths.you_have_x_likes)
        if you_have_x_likes[0]:
            you_have_x_likes[1].click()
            custom_logger.log_info(localization.localization_manager.dismissed_popup('У тебя уже херова гора лайков'))
            return True

        return False

    def has_out_of_likes_popup(self) -> bool:
        out_of_likes_by_link = self._session.try_get_first_element(Xpaths.out_of_likes_popup_by_link)
        out_of_likes_by_text_ru = self._session.try_get_first_element(Xpaths.out_of_likes_popup_by_text_ru)
        if out_of_likes_by_link[0] or out_of_likes_by_text_ru[0]:
            custom_logger.log_info(localization.localization_manager.out_of_likes())
            return True
        return False