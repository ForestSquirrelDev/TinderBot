def settings_window() -> str:
    return 'Окно настроек'

def start() -> str:
    return 'Старт'

def pause() -> str:
    return 'Пауза'

def exit_app() -> str:
    return 'Выйти'

def filter_empty_description() -> str:
    return "Дизлайкать пустое описание?"

def filter_inst() -> str:
    return """Дизлайкать пустое описание со ссылкой на инсту?"""

def filter_negative() -> str:
    return """Фильтровать негатив в описании профиля?"""

def message_match() -> str:
    return "Отправлять сообщение новой паре?"

def messages_list() -> str:
    return "Список сообщений"

def like_chance() -> str:
    return "Шанс лайка"

def serial_key_not_found() -> str:
    return "Не получилось найти файл с ключом активации"

def serial_key_not_valid() -> str:
    return "Ключ активации недействителен"

def serial_hwid_fail() -> str:
    return "Ключ активации недействителен для этого устройства"

def serial_key_expired() -> str:
    return "Ключ активации истёк"

def serial_key_check_failed() -> str:
    return "Не получилось проверить ключ активации"

def success() -> str:
    return "Успех"

def key_activated_for_the_first_time() -> str:
    return "Ключ активирован впервые"

def starting_the_bot() -> str:
    return "Начинаю работу"

def stopping_the_bot() -> str:
    return "Останавливаю работу"

def press_start() -> str:
    return "Залогиньтесь в Тиндер и нажмите 'Старт'"

def discarded_upgrade_like() -> str:
    return "Закрыл всплывашку 'Проапгрейдите свой лайк'"

def failed_to_expand_profile() -> str:
    return "Не получилось открыть профиль"

def trying_to_expand_profile(iteration: int) -> str:
    return f"Пытаюсь открыть профиль. Попытка {iteration}"

def trying_to_like(iteration: int) -> str:
    return f"Пытаюсь лайкнуть профиль. Попытка {iteration}"

def description_not_found() -> str:
    return "Не получилось найти описание"

def found_stop_word(stop_word: str) -> str:
    return f"Нашёл стоп-слово: {stop_word}"

def instagram_discard() -> str:
    return f"Похоже, описание состоит из одной ссылки на инсту"

def send_message_disabled() -> str:
    return "Отправка сообщений новой паре отключена. Закрываю всплывашку"

def trying_to_send_message_to_match(message: str) -> str:
    return f"Пытаюсь отправить сообщение {message} паре"

def liked_disliked(liked: int, disliked: int) -> str:
    return f"Количество лайков/дизлайков в течение сессии: {liked} и {disliked}"

def sent_message_to_match() -> str:
    return "Отправил сообщение паре"

def description_checks_disabled() -> str:
    return "Кажется, профиль пустой. Фильтр пустых профилей включён - дизлайкаю."

def dismissed_popup(popup: str) -> str:
    return f"Закрыл всплывашку '{popup}'"

def probability_check_passed() -> str:
    return "Шанс лайка сработал"

def probability_check_failed() -> str:
    return "Шанс лайка не сработал"

def disliking() -> str:
    return "Дизлайкаю профиль..."

def settings() -> str:
    return 'Настройки'

def found_its_a_match() -> str:
    return "Нашёл всплывашку 'Это пара'"

def liking() -> str:
    return "Лайкаю профиль..."

def failed_to_like() -> str:
    return "Не получилось лайкнуть"

def failed_to_like(reason: str) -> str:
    return f"Не получилось лайкнуть: '{str}'"

def reload_tinder_failed() -> str:
    return "Перезагрузка страницы не помогла. Пытаюсь перезагрузить снова..."

def tinder_error_occured(error: str) -> str:
    return f"Работа была прервана ошибкой{error}. Пытаюсь перезагрузить страницу..."

def failed_to_dislike() -> str:
    return "Не получилось дизлайкнуть профиль"

def fatal_error(error: str) -> str:
    return f"Критическая ошибка: {error}"

def swipes_settings() -> str:
    return "Свайпы профилей"

def geolocation_settings() -> str:
    return "Смена геолокации"

def latitude() -> str:
    return "Широта"

def longitude() -> str:
    return "Долгота"

def change_geolocation() -> str:
    return "Сменить геолокацию"

def and_term() -> str:
    return 'и'

def wrong_latitude_longitude_format() -> str:
    return "Неверный формат широты/долготы. Формат должен быть: число, запятая, число. Например: 11.1111111111111, 11.1111111111111"

def string_cannot_be_empty() -> str:
    return "Строка не может быть пустой"

def latitude_cannot_be_less_than_negative_90_or_bigger_than_90() -> str:
    return "Широта не может быть меньше -90 или больше 90"

def longitude_cannot_be_less_than_negative_180_or_bigger_than_180() -> str:
    return "Долгота не может быть меньше -180 или больше 180"

def geolocation_changed() -> str:
    return "Геолокация изменена"

def serial_key_error() -> str:
    return "Ошибка ключа активации"

def telegram() -> str:
    return "Телеграм"

def refreshing_page() -> str:
    return "Перезагружаю страницу"

def likes() -> str:
    return "Лайки"

def messages_to_matches() -> str:
    return "Сообщения парам"

def found_stop_word() -> str:
    return "Нашёл стоп-слово"

def stop_words_not_found() -> str:
    return "Не нашёл стоп-слов"

def failed_to_add_stop_word() -> str:
    return "Не получилось добавить стоп-слово"

def dislike_if_found_stop_word() -> str:
    return "Дизлайкать если нашли стоп-слово?"

def filter_empty_description_option_was_enabled() -> str:
    return "Опция дизлайка профилей без описания включена"

def filter_empty_description_option_was_disabled() -> str:
    return "Опция дизлайка профилей без описания выключена"

def filter_inst_option_was_enabled() -> str:
    return "Опция дизлайка профилей с описанием, состоящим из одной лишь ссылки на инстаграм, включена"

def filter_inst_option_was_disabled() -> str:
    return "Опция дизлайка профилей с описанием, состоящим из одной лишь ссылки на инстаграм, выключена"

def filter_stop_words_option_was_enabled() -> str:
    return "Опция дизлайка по стоп-словам в описании включена"

def filter_stop_words_option_was_disabled() -> str:
    return "Опция дизлайка по стоп-словам в описании выключена"

def filter_send_message_to_match_was_enabled() -> str:
    return "Опция отправки сообщения новым парам включена"

def filter_send_message_to_match_was_disabled() -> str:
    return "Опция отправки сообщения новым парам выключена"

def setup_stop_words() -> str:
    return "Настроить стоп-слова"

def setup_messages_to_matches() -> str:
    return "Настроить сообщения парам"

def add() -> str:
    return "Добавить"

def delete() -> str:
    return "Удалить"

def save_on_quit() -> str:
    return "Сохранять при выходе"

def already_running() -> str:
    return "Программа уже запущена"

def error() -> str:
    return "Ошибка"

def out_of_likes() -> str:
    return "Кажется, у нас закончились лайки"

def browser_error() -> str:
    return "Ошибка браузера"

def install_latest_chrome() -> str:
    return "Для работы бота нужен Google Chrome версии не ниже 111 :(\nДля удобства установщик есть прямо в файлах с ботом - просто запустите ChromeSetup.exe\n\n" \
           "Если ничего не работает - пишите в телеграм: @ayayaintensifies"