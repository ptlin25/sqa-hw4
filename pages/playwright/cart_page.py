from pages.playwright.base_page import BasePage
from pages.playwright.modals.order_modal import OrderModal


class CartPage(BasePage):
    URL = "https://www.demoblaze.com/cart.html"

    def open(self):
        self.page.goto(self.URL)
        return self

    def get_product_names(self) -> list[str]:
        rows = self.page.locator("#tbodyid tr").filter(has=self.page.locator("td + td"))
        rows.first.wait_for()
        return [rows.nth(i).locator("td").nth(1).inner_text().strip() for i in range(rows.count())]

    def click_place_order(self) -> OrderModal:
        self.page.click("button[data-target='#orderModal']")
        return OrderModal(self.page)
