from tinderbotz.session_data import SessionData
from tinderbotz.steps.popups_handler import PopupsHandler

class BotContext:
    driver = None
    session_data: SessionData = SessionData()
    popups_handler: PopupsHandler

    def __init__(self, driver, popups_handler: PopupsHandler):
        self.driver = driver
        self.popups_handler = popups_handler

    @property
    def profile_expanded(self) -> bool:
        return str.lower(self.driver.current_url).find("profile") != -1
