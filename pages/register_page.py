import os

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage

DEFAULT_AUTH_URL = "https://auth.niffler.qa.guru"


class RegisterPage(BasePage):
    path = "/register"

    username_input = (By.CSS_SELECTOR, "#username")
    password_input = (By.CSS_SELECTOR, "#password")
    password_submit_input = (By.CSS_SELECTOR, "#passwordSubmit")
    register_button = (By.CSS_SELECTOR, "#register-button")
    error_message = (By.CSS_SELECTOR, ".form__error")
    success_message = (By.CSS_SELECTOR, ".form__paragraph_success")
    login_link = (By.CSS_SELECTOR, "a.form__link[href='/login']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    def auth_url(self) -> str:
        return os.getenv("AUTH_URL", DEFAULT_AUTH_URL).rstrip("/")

    @allure.step("Открыть страницу регистрации")
    def open(self):
        self.driver.get(f"{self.auth_url}{self.path}")
        return self

    @allure.step("Зарегистрировать пользователя {username}")
    def register(self, username: str, password: str, password_submit: str | None = None):
        self.type_text(self.username_input, username)
        self.type_text(self.password_input, password)
        self.type_text(
            self.password_submit_input,
            password_submit if password_submit is not None else password,
        )
        self.click(self.register_button)
        return self
