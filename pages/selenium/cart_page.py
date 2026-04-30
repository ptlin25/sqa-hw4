from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.selenium.base_page import BasePage
from pages.selenium.modals.order_modal import OrderModal


class CartPage(BasePage):
    URL = "https://www.demoblaze.com/cart.html"
    TABLE = (By.ID, "tbodyid")
    ROWS = (By.CSS_SELECTOR, "#tbodyid tr")
    PLACE_ORDER_BTN = (By.CSS_SELECTOR, "button[data-target='#orderModal']")

    def open(self):
        self.driver.get(self.URL)
        return self

    def wait_for_table(self):
        self.wait.until(EC.presence_of_element_located(self.TABLE))
        return self

    def wait_for_at_least_one_row(self):
        try:
            self.wait.until(lambda d: any(
                len(row.find_elements(By.TAG_NAME, "td")) > 1
                and row.find_elements(By.TAG_NAME, "td")[1].text.strip()
                for row in d.find_elements(*self.ROWS)
            ))
            return True
        except TimeoutException:
            return False

    def _rows(self):
        return self.driver.find_elements(*self.ROWS)

    def get_product_names(self):
        return [
            tds[1].text.strip()
            for row in self._rows()
            if len(tds := row.find_elements(By.TAG_NAME, "td")) > 1
        ]

    def is_product_present(self, product_name):
        return product_name in self.get_product_names()

    def delete_product(self, product_name):
        for row in self._rows():
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) > 1 and product_name == tds[1].text.strip():
                row.find_element(By.TAG_NAME, "a").click()
                return
        raise ValueError(f"'{product_name}' not found in cart")

    def wait_for_product_removed(self, product_name):
        try:
            self.wait.until(lambda d: not self.is_product_present(product_name))
            return True
        except TimeoutException:
            return False

    def click_place_order(self):
        self.click(self.PLACE_ORDER_BTN)
        modal = OrderModal(self.driver)
        modal.wait_for_open()
        return modal
