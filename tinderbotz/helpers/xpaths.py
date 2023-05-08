class Xpaths:
    _content = '/html/body/div[1]'
    _modal_manager = '/html/body/div[2]'
    _front_photo_description_relative = '//*/div/div/div[2]/div[3]/div/div[2]/div/div/div'
    _full_description_relative = '//*/div/div[1]/div[1]/div/div[2]/div[2]/div'
    _first_element_of_empty_description_relative = '//*/div/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]'
    _open_profile_button_relative = '//*/div/div/div[2]/div[3]/button'
    _open_profile_button_backing = '//*/div[2]/div/div[2]/div[1]/div[2]'
    _open_profile_buton_backing_backing = '//*/div/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/div[2]'
    _frontpage_profile_slider = '//*/div/div/div[2]/div[1]/div[1]/span[1]'

    back_to_tinder_relative = '//*/div[2]/main/div/div/div/div[4]/button'
    back_to_tinder_search_eng = "//*[contains(@title, 'Back')]"
    back_to_tinder_search_ru = "//*[contains(@title, 'Назад')]"
    say_something_search_eng = "//textarea[starts-with(@placeholder, 'Say something')]"
    say_something_search_ru = "//textarea[starts-with(@placeholder, 'Напишите что')]"
    say_something_relative = "//*/div/div[3]/div[3]/form/textarea"
    match_submit_send_button_relative = "//*/div/div[3]/div[3]/form/button"
    match_submit_send_button_search = "//*[contains(@type, 'submit')]"

    add_to_home_screen_absolute = '/html/body/div[2]/main/div/div[2]/button[2]'
    boost_your_likes_absolute = '/html/body/div[2]/main/div/button[2]'
    you_have_first_like_absolute = '/html/body/div[2]/main/div[2]/div/div[3]/button[2]'
    you_have_x_likes = '/html/body/div[2]/main/div/div/div[3]/button[2]'

    out_of_likes_popup_by_link = "//img[contains(@src,'https://tinderphotos.s3.amazonaws.com/paywall_assets/plus_subscription_paywall/plus_header.png')]"
    out_of_likes_popup_by_text_ru = "//div[text()='Безлимит лайков. Ставь столько лайков, сколько захочешь.']"

    full_description_absolutes = [
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div', # horizontal orientation
        '/html/body/div[1]/div/div[1]/div/div/main/div/div[1]/div[1]/div/div[2]/div[2]/div' # profile orient
    ]

    full_description_invalid_selector = '//*/div/div[1]/div[1]/div/div[2]/div[2]/div/text()'
    full_description_invalid_selector_paths = [
        '//*/div/div[1]/div[1]/div/div[2]/div[2]/div/text()',
        '/html/body/div[1]/div/div[1]/div/div/main/div/div[1]/div[1]/div/div[2]/div[2]/div',
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div'
    ]

    open_profile_button_paths = [
        '//*/div/div/div[2]/div[3]/button',
        '//*/div[2]/div/div[2]/div[1]/div[2]',
        '//*/div/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/div[2]',
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/div[3]/button',
        '/html/body/div[1]/div/div[1]/div/div/main/div/div/div[1]/div/div[1]/div[3]/button'
    ]

    dislike_button_paths = [
        '//*/div[1]/div[2]/div/div/div[2]/button',
        '//*/div/div/div[4]/div/div[2]/button',
        '/html/body/div[1]/div/div[1]/div/div/main/div/div/div[1]/div/div[3]/div/div[2]/button',
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[2]/button',
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[2]/button',
        '/html/body/div[1]/div/div[1]/div/div/main/div/div[1]/div[2]/div/div/div[2]/button'
    ]
    like_button_paths = [
        '//*/div[1]/div[2]/div/div/div[4]/button',
        '//*/div/div/div[3]/div/div[4]/button',
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[4]/button',
        '/html/body/div[1]/div/div[1]/div/div/main/div/div[1]/div[2]/div/div/div[4]/button',
        '/html/body/div[1]/div/div[1]/div/div/main/div/div/div[1]/div/div[3]/div/div[4]/button',
        '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button',
        '//*/div/div[4]/div/div[4]/button',
        '//*/div/div[5]/div/div[4]/button',
        '//*/div/div[3]/div/div[4]/button',
        '//*/div/div[2]/div/div[4]/button',
        '//*/div/div[1]/div/div[4]/button'
    ]

    @property
    def content(self) -> str:
        return self._content

    @property
    def modal_manager(self) -> str:
        return self._modal_manager

    @property
    def front_photo_description(self) -> str:
        return self._front_photo_description_relative

    @property
    def full_description(self) -> str:
        return self._full_description_relative

    @property
    def first_element_of_empty_description(self) -> str:
        return self._first_element_of_empty_description_relative

    @property
    def open_profile_button(self) -> str:
        return self._open_profile_button_relative

    @property
    def open_profile_backing(self) -> str:
        return self._open_profile_button_backing

    @property
    def open_profile_backing_backing(self) -> str:
        return self._open_profile_buton_backing_backing

    @property
    def frontpage_photo_slider(self) -> str:
        return self._frontpage_profile_slider
