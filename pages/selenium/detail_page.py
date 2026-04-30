from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.selenium.base_page import BasePage


class DetailPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "h2.name")
    PRICE = (By.CSS_SELECTOR, "h3.price-container")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a.btn[onclick*='addToCart']")

    def get_title(self):
        return self.find(self.TITLE).text.strip()

    def get_price(self):
        return self.find(self.PRICE).text.strip().split(" ")[0].strip()

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def accept_cart_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text
