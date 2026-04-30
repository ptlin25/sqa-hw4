from selenium.webdriver.common.by import By

from pages.selenium.base_page import BasePage
from pages.selenium.modals.login_modal import LoginModal
from pages.selenium.modals.contact_modal import ContactModal
from pages.selenium.modals.signup_modal import SignUpModal


class NavBar(BasePage):
    URL = "https://www.demoblaze.com/index.html"
    CONTACT_LINK = (By.LINK_TEXT, "Contact")
    LOG_IN_LINK = (By.LINK_TEXT, "Log in")
    LOG_OUT_LINK = (By.LINK_TEXT, "Log out")
    SIGN_UP_LINK = (By.LINK_TEXT, "Sign up")
    WELCOME_LINK = (By.ID, "nameofuser")

    def open(self):
        self.driver.get(self.URL)
        return self

    def click_login(self):
        self.click(self.LOG_IN_LINK)
        modal = LoginModal(self.driver)
        modal.wait_for_open()
        return modal

    def logout(self):
        self.click(self.LOG_OUT_LINK)

    def is_username_shown(self, username):
        return self.has_text(self.WELCOME_LINK, username)

    def click_contact(self):
        self.click(self.CONTACT_LINK)
        modal = ContactModal(self.driver)
        modal.wait_for_open()
        return modal

    def click_signup(self):
        self.click(self.SIGN_UP_LINK)
        modal = SignUpModal(self.driver)
        modal.wait_for_open()
        return modal
