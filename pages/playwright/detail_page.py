from pages.playwright.base_page import BasePage


class DetailPage(BasePage):
    def goto(self, url: str):
        self.page.goto(url)
        return self

    def get_title(self) -> str:
        self.page.wait_for_function(
            "() => (document.querySelector('h2.name')?.innerText || '').trim() !== ''"
        )
        return self.page.locator("h2.name").inner_text().strip()

    def get_raw_title(self) -> str:
        return self.page.locator("h2.name").inner_text().strip()

    def add_to_cart(self) -> str:
        title = self.get_title()
        with self.page.expect_event("dialog") as dialog_info:
            self.page.click("a.btn[onclick*='addToCart']")
        dialog_info.value.accept()
        return title
