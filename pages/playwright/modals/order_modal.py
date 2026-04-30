from pages.playwright.base_page import BasePage


class OrderModal(BasePage):
    def fill(self, name: str = "", country: str = "", city: str = "",
             card: str = "", month: str = "", year: str = ""):
        self.page.fill("#name", name)
        self.page.fill("#country", country)
        self.page.fill("#city", city)
        self.page.fill("#card", card)
        self.page.fill("#month", month)
        self.page.fill("#year", year)
        return self

    def submit_and_capture_alert(self) -> str:
        captured = []
        self.page.once("dialog", lambda d: (captured.append(d.message), d.accept()))
        self.page.click("button[onclick='purchaseOrder()']")
        return captured[0] if captured else ""
