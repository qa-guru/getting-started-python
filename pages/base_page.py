import allure
from playwright.sync_api import Page


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открыть страницу")
    def open(self):
        self.page.goto(f"{self.page.base_url}{self.path}")
        return self

    def is_opened(self) -> bool:
        return self.page.url.startswith(f"{self.page.base_url}{self.path}")
