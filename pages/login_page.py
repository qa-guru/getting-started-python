import allure
from playwright.sync_api import Page, Locator

from pages.base_page import BasePage
from pages.main_page import MainPage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def username_input(self) -> Locator:
        return self.page.locator("#username")

    @property
    def password_input(self) -> Locator:
        return self.page.locator("#password")

    @property
    def login_button(self) -> Locator:
        return self.page.locator("#login-button")

    @property
    def register_link(self) -> Locator:
        return self.page.locator("#register-button")

    @property
    def error_message(self) -> Locator:
        return self.page.locator(".form__error")

    @allure.step("Ввести имя пользователя {username}")
    def fill_username(self, username: str):
        self.username_input.fill(username)
        return self

    @allure.step("Ввести пароль")
    def fill_password(self, password: str):
        self.password_input.fill(password)
        return self

    @allure.step("Нажать кнопку Log in")
    def submit(self) -> MainPage:
        self.login_button.click()
        return MainPage(self.page)

    @allure.step("Отправить форму логина клавишей Enter")
    def submit_with_enter(self) -> MainPage:
        self.password_input.press("Enter")
        return MainPage(self.page)

    def login(self, username: str, password: str) -> MainPage:
        with allure.step(f"Войти как {username}"):
            return self.fill_username(username).fill_password(password).submit()

    def login_with_enter(self, username: str, password: str) -> MainPage:
        with allure.step(f"Войти как {username} через Enter"):
            return self.fill_username(username).fill_password(password).submit_with_enter()

    @allure.step("Перейти к регистрации")
    def go_to_register(self):
        self.register_link.click()
        from pages.register_page import RegisterPage
        return RegisterPage(self.page)
