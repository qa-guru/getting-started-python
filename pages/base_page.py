import allure
from selenium.webdriver.remote.webdriver import WebDriver

from infrastructure.waits import ElementWaits
from settings import Settings


class BasePage:
    path = "/"

    def __init__(self, driver: WebDriver, settings: Settings):
        self.driver = driver
        self.settings = settings
        self.base_url = settings.base_url
        self.wait = ElementWaits(driver, settings.timeout_s)

    @allure.step("Открыть страницу")
    def open(self):
        self.driver.get(f"{self.base_url}{self.path}")
        return self

    @allure.step("Проверить, что страница открыта")
    def is_opened(self) -> bool:
        return self.driver.current_url.startswith(f"{self.base_url}{self.path}")

    @allure.step("Найти элемент {locator}")
    def find(self, locator):
        return self.wait.visible(locator)

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator):
        self.wait.clickable(locator).click()

    @allure.step("Кликнуть по элементу {locator} через JS")
    def js_click(self, locator):
        element = self.wait.present(locator)
        self.driver.execute_script("arguments[0].click()", element)

    @allure.step("Ввести текст в элемент {locator}")
    def type_text(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
