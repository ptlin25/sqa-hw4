from pages.playwright.base_page import BasePage
from pages.playwright.modals.login_modal import LoginModal
from pages.playwright.modals.signup_modal import SignupModal


class NavBar(BasePage):
    URL = "https://www.demoblaze.com/index.html"

    def open(self):
        self.page.goto(self.URL)
        return self

    def click_login(self) -> LoginModal:
        self.page.click("#login2")
        return LoginModal(self.page)

    def click_signup(self) -> SignupModal:
        self.page.click("#signin2")
        return SignupModal(self.page)

    def login(self, username: str, password: str):
        self.click_login().login(username, password)
        return self

    def is_username_shown(self, username: str) -> bool:
        try:
            return username in self.page.locator("#nameofuser").inner_text(timeout=5000)
        except Exception:
            return False
