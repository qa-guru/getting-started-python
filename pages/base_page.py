import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT_S = 10


class BasePage:
    path = "/"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT_S)

    @allure.step("Открыть страницу")
    def open(self):
        self.driver.get(f"{self.driver.base_url}{self.path}")
        return self

    def is_opened(self) -> bool:
        return self.driver.current_url.startswith(f"{self.driver.base_url}{self.path}")

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def js_click(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click()", element)

    def type_text(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
