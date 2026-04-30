from selenium.webdriver.support import expected_conditions as EC

from pages.selenium.base_page import BasePage


class BaseModal(BasePage):
    def wait_for_open(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.wait.until(EC.visibility_of_element_located(self.MODAL))
        return self

    def wait_for_close(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.wait.until(EC.invisibility_of_element_located(self.MODAL))
        return self
