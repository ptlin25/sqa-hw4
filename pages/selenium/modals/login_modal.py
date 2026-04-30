from selenium.webdriver.common.by import By

from pages.selenium.modals.base_modal import BaseModal


class LoginModal(BaseModal):
    MODAL = (By.ID, "logInModal")
    USERNAME_FIELD = (By.ID, "loginusername")
    PASSWORD_FIELD = (By.ID, "loginpassword")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[onclick='logIn()']")

    def login(self, username, password):
        self.type(self.USERNAME_FIELD, username)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BTN)
        self.wait_for_close()

    def is_open(self):
        return self.is_visible(self.MODAL)
