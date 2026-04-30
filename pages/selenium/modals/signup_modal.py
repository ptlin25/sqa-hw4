from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.selenium.modals.base_modal import BaseModal


class SignUpModal(BaseModal):
    MODAL = (By.ID, "signInModal")
    USERNAME_FIELD = (By.ID, "sign-username")
    PASSWORD_FIELD = (By.ID, "sign-password")
    REGISTER_BTN = (By.CSS_SELECTOR, "button[onclick='register()']")

    def register(self, username, password):
        self.type(self.USERNAME_FIELD, username)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.REGISTER_BTN)

    def accept_alert(self):
        try:
            alert = WebDriverWait(self.driver, 20).until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None
