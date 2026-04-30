from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.selenium.modals.base_modal import BaseModal


class ContactModal(BaseModal):
    MODAL = (By.ID, "exampleModal")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[onclick='send()']")

    def submit(self):
        self.click(self.SUBMIT_BTN)

    def accept_alert_if_show(self):
        try:
            self.wait.until(EC.alert_is_present()).accept()
            return True
        except TimeoutException:
            return False
