import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from pages.main_page import MainPage
from pages.register_page import RegisterPage


class LoginPage(BasePage):
    path = "/"

    username_input = (By.CSS_SELECTOR, "#username")
    password_input = (By.CSS_SELECTOR, "#password")
    login_button = (By.CSS_SELECTOR, "#login-button")
    register_link = (By.CSS_SELECTOR, "#register-button")
    error_message = (By.CSS_SELECTOR, ".form__error")

    @allure.step("Ввести имя пользователя {username}")
    def fill_username(self, username: str) -> "LoginPage":
        self.type_text(self.username_input, username)
        return self

    @allure.step("Ввести пароль")
    def fill_password(self, password: str) -> "LoginPage":
        self.type_text(self.password_input, password)
        return self

    @allure.step("Нажать кнопку Log in")
    def submit(self) -> "LoginPage":
        self.click(self.login_button)
        return self

    @allure.step("Отправить форму логина клавишей Enter")
    def submit_with_enter(self) -> "LoginPage":
        self.find(self.password_input).send_keys(Keys.ENTER)
        return self

    @allure.step("Ожидание открытия страницы логина")
    def wait_until_open(self) -> "LoginPage":
        self.wait.visible(self.username_input)
        self.wait.visible(self.login_button)
        return self

    @allure.step("Получить текст ошибки")
    def error_text(self) -> str:
        error = self.find(self.error_message)
        self.wait.until(lambda _: error.text.strip() != "")
        return error.text.strip()

    @allure.step("Войти как {username}")
    def login(self, username: str, password: str) -> MainPage:
        self.fill_username(username).fill_password(password).submit()
        return MainPage(self.driver, self.settings).wait_until_open()

    @allure.step("Войти как {username} через Enter")
    def login_with_enter(self, username: str, password: str) -> MainPage:
        self.fill_username(username).fill_password(password).submit_with_enter()
        return MainPage(self.driver, self.settings).wait_until_open()

    @allure.step("Перейти к регистрации")
    def go_to_register(self) -> RegisterPage:
        self.click(self.register_link)
        return RegisterPage(self.driver, self.settings)
