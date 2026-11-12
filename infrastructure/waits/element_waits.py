"""Общие явные ожидания элементов: обёртка над WebDriverWait.

Локаторы и специфичные условия конкретных страниц остаются в Page Object;
здесь только переиспользуемые механизмы ожидания.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ElementWaits:
    """Делегируемый механизм ожиданий для Page Object.

    Инкапсулирует WebDriverWait: общие условия доступны методами
    visible/clickable/present/url_contains, специфичные условия страницы
    передаются в until().
    """

    def __init__(self, driver: WebDriver, timeout_s: float):
        self._wait = WebDriverWait(driver, timeout_s)

    def until(self, condition):
        """Ждать произвольное условие expected_conditions или predicate."""
        return self._wait.until(condition)

    def visible(self, locator) -> WebElement:
        return self.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator) -> WebElement:
        return self.until(EC.element_to_be_clickable(locator))

    def present(self, locator) -> WebElement:
        return self.until(EC.presence_of_element_located(locator))

    def url_contains(self, fragment: str) -> bool:
        return self.until(EC.url_contains(fragment))
