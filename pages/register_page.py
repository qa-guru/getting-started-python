import os

import allure
from playwright.sync_api import Page, Locator

from pages.base_page import BasePage

DEFAULT_AUTH_URL = "https://auth.niffler.qa.guru"


class RegisterPage(BasePage):
    path = "/register"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def auth_url(self) -> str:
        return os.getenv("AUTH_URL", DEFAULT_AUTH_URL).rstrip("/")

    @allure.step("Открыть страницу регистрации")
    def open(self):
        self.page.goto(f"{self.auth_url}{self.path}")
        return self

    @property
    def username_input(self) -> Locator:
        return self.page.locator("#username")

    @property
    def password_input(self) -> Locator:
        return self.page.locator("#password")

    @property
    def password_submit_input(self) -> Locator:
        return self.page.locator("#passwordSubmit")

    @property
    def register_button(self) -> Locator:
        return self.page.locator("#register-button")

    @property
    def error_message(self) -> Locator:
        return self.page.locator(".form__error")

    @property
    def success_message(self) -> Locator:
        return self.page.locator(".form__paragraph_success")

    @property
    def login_link(self) -> Locator:
        return self.page.locator("a.form__link[href='/login']")

    @allure.step("Зарегистрировать пользователя {username}")
    def register(self, username: str, password: str, password_submit: str | None = None):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.password_submit_input.fill(password_submit if password_submit is not None else password)
        self.register_button.click()
        return self
