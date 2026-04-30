from pages.playwright.base_page import BasePage


class SignupModal(BasePage):
    def fill_credentials(self, username: str, password: str):
        self.page.fill("#sign-username", username)
        self.page.fill("#sign-password", password)
        return self

    def submit_and_capture_alert(self) -> str:
        captured = []
        self.page.once("dialog", lambda d: (captured.append(d.message), d.accept()))
        self.page.click("button[onclick='register()']")
        return captured[0] if captured else ""
