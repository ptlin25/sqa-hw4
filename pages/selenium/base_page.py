from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):

        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.find(locator).send_keys(text)

    def is_visible(self, locator) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return False

    def has_text(self, locator, text) -> bool:
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            return False
