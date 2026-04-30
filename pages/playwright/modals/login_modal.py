from pages.playwright.base_page import BasePage


class LoginModal(BasePage):
    def fill_credentials(self, username: str, password: str):
        self.page.fill("#loginusername", username)
        self.page.fill("#loginpassword", password)
        return self

    def login(self, username: str, password: str):
        self.fill_credentials(username, password)
        self.page.click("button[onclick='logIn()']")
        self.page.locator("#logInModal").wait_for(state="hidden")

    def submit_and_capture_alert(self) -> str:
        with self.page.expect_event("dialog") as dialog_info:
            self.page.click("button[onclick='logIn()']")
        dialog = dialog_info.value
        text = dialog.message
        dialog.accept()
        return text
