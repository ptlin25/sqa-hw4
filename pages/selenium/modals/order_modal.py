from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.selenium.modals.base_modal import BaseModal


class OrderModal(BaseModal):
    MODAL = (By.ID, "orderModal")
    NAME_FIELD = (By.ID, "name")
    COUNTRY_FIELD = (By.ID, "country")
    CITY_FIELD = (By.ID, "city")
    CARD_FIELD = (By.ID, "card")
    MONTH_FIELD = (By.ID, "month")
    YEAR_FIELD = (By.ID, "year")
    PURCHASE_BTN = (By.CSS_SELECTOR, "button[onclick='purchaseOrder()']")
    CONFIRM_MODAL = (By.CSS_SELECTOR, "div.sweet-alert")
    CONFIRM_LEAD = (By.CSS_SELECTOR, "div.sweet-alert p.lead")

    def fill_order_form(
        self,
        name="Test User",
        country="USA",
        city="Chicago",
        card="4111111111111111",
        month="12",
        year="2030",
    ):
        self.type(self.NAME_FIELD, name)
        self.type(self.COUNTRY_FIELD, country)
        self.type(self.CITY_FIELD, city)
        self.type(self.CARD_FIELD, card)
        self.type(self.MONTH_FIELD, month)
        self.type(self.YEAR_FIELD, year)
        self.click(self.PURCHASE_BTN)

    def wait_for_confirmation(self):
        self.wait.until(EC.visibility_of_element_located(self.CONFIRM_MODAL))
        return self

    def get_confirmation_details(self):
        return self.find(self.CONFIRM_LEAD).text
