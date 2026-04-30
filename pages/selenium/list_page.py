from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from pages.selenium.nav_bar import NavBar
from pages.selenium.detail_page import DetailPage


class ListPage(NavBar):
    MONITORS_CATEGORY = (By.CSS_SELECTOR, "a[onclick=\"byCat('monitor')\"]")
    NEXT_BTN = (By.ID, "next2")
    PREV_BTN = (By.ID, "prev2")
    PRODUCT_CARD = (By.CSS_SELECTOR, "#tbodyid .card")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".card-title a")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "h5")
    PRODUCT_TITLE_LINKS = (By.CSS_SELECTOR, "#tbodyid .card-title a")

    def are_n_products_shown(self, n=9):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CARD))
            return len(elements) >= n
        except TimeoutException:
            return False

    def get_product_names(self):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_TITLE_LINKS))
            return [el.text.strip() for el in elements]
        except (TimeoutException, StaleElementReferenceException):
            return []

    def wait_for_products_to_change(self, original_names):
        original = set(original_names)
        def check_names(d):
            try:
                current_elements = d.find_elements(*self.PRODUCT_TITLE_LINKS)
                if not current_elements:
                    return False
                current_names = set(el.text.strip() for el in current_elements if el.text.strip())
                return current_names != original
            except StaleElementReferenceException:
                return False

        try:
            self.wait.until(check_names)
            return True
        except TimeoutException:
            return False

    def get_first_tile_info(self):
        cards = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_CARD))
        name = cards[0].find_element(*self.PRODUCT_NAME).text.strip()
        price = cards[0].find_element(*self.PRODUCT_PRICE).text.strip()
        return name, price

    def click_first_product(self):
        links = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_TITLE_LINKS))
        links[0].click()
        return DetailPage(self.driver)

    def click_monitors_category(self):
        self.click(self.MONITORS_CATEGORY)

    def _paginate(self, btn):
        current = self.get_product_names()
        self.click(btn)
        self.wait_for_products_to_change(current)

    def click_next(self):
        self._paginate(self.NEXT_BTN)

    def click_prev(self):
        self._paginate(self.PREV_BTN)
