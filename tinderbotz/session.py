import random
from selenium.common import ElementClickInterceptedException, ElementNotInteractableException, WebDriverException
from tinderbotz.steps.operation_result import OperationResult
import localization.localization_manager
import os
import time
from pathlib import Path
from chromedriver_autoinstaller import get_chrome_version
import undetected_chromedriver_claimed as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tinderbotz.utils import custom_logger
from tinderbotz.helpers.xpaths import Xpaths

class Session:
    HOME_URL = "https://www.tinder.com/app/recs"
    driver: uc.Chrome

    def __init__(self, headless=False, store_session=True, proxy=None, user_data=False):
        options = uc.ChromeOptions()

        # Create empty profile to avoid annoying Mac Popup
        if store_session:
            if not user_data:
                user_data = f"{Path().absolute()}/chrome_profile/"
            if not os.path.isdir(user_data):
                os.mkdir(user_data)

            Path(f'{user_data}First Run').touch()
            options.add_argument(f"--user-data-dir={user_data}")

        options.add_argument("--start-maximized")
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_argument("--lang=en-US")

        custom_logger.log_info("Getting ChromeDriver ...")
        ver = get_chrome_version()
        dot = ver.find('.')
        version_short = ver[0: dot]
        custom_logger.log_info(f"Chromeversion is {version_short}")
        if version_short.isdigit():
            version_int = int(version_short)
        else:
            version_int = 111
        self.driver = uc.Chrome(options=options, version_main=version_int, use_subprocess=False)


    # Setting a custom location
    def set_custom_location(self, latitude, longitude, accuracy="100%"):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": int(accuracy.split('%')[0])
        }

        self.driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
        custom_logger.log_info(localization.localization_manager.geolocation_changed() + ". " + localization.localization_manager.refreshing_page())

    def try_get_first_element(self, xpath) -> (bool, WebElement):
        elements_list = self.driver.find_elements(By.XPATH, xpath)
        elements_count = len(elements_list)
        if (elements_count == 0):
            return (False, None)
        return (True, elements_list[0])

    def like(self, bot_context) -> OperationResult:
        try:
            for i in Xpaths.like_button_paths:
                time.sleep(0.3)
                handled_popups = bot_context.popups_handler.handle_potential_popups()
                if handled_popups:
                    time.sleep(random.uniform(1, 2.5))

                element_request = self.try_get_first_element(i)
                if element_request[0]:
                    try:
                        element_request[1].click()
                        bot_context.session_data.likes += 1
                        return OperationResult.Success
                    except (ElementClickInterceptedException, ElementNotInteractableException) as ex:
                        custom_logger.log_exception(f"Exception during like: {ex}")
                        custom_logger.log_debug(f"Failed to like: {type(ex)}")
            return OperationResult.Interrupted
        except WebDriverException as ex:
            custom_logger.log_error(localization.localization_manager.failed_to_like())
            custom_logger.log_exception(f"Exception: {ex}")
            return OperationResult.Interrupted

    def dislike(self, bot_context) -> OperationResult:
        try:
            for i in Xpaths.dislike_button_paths:
                time.sleep(0.3)
                handled_popups = bot_context.popups_handler.handle_potential_popups()
                if handled_popups:
                    time.sleep(random.uniform(1, 2.5))

                element_request = self.try_get_first_element(i)
                if element_request[0]:
                    try:
                        element_request[1].click()
                        bot_context.session_data.dislikes += 1
                        return OperationResult.Success
                    except (ElementClickInterceptedException, ElementNotInteractableException) as ex:
                        custom_logger.log_exception(f"Exception during dislike: {ex}")
                        custom_logger.log_debug(f"Failed to dislike: {type(ex)}")
            return OperationResult.Interrupted
        except WebDriverException as ex:
            custom_logger.log_error(localization.localization_manager.failed_to_dislike())
            custom_logger.log_exception(f"Exception: {ex}")
            return OperationResult.Interrupted
