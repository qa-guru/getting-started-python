import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.main_page import MainPage


class LoginPage(BasePage):
    path = "/"

    username_input = (By.CSS_SELECTOR, "#username")
    password_input = (By.CSS_SELECTOR, "#password")
    login_button = (By.CSS_SELECTOR, "#login-button")
    register_link = (By.CSS_SELECTOR, "#register-button")
    error_message = (By.CSS_SELECTOR, ".form__error")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Ввести имя пользователя {username}")
    def fill_username(self, username: str):
        self.type_text(self.username_input, username)
        return self

    @allure.step("Ввести пароль")
    def fill_password(self, password: str):
        self.type_text(self.password_input, password)
        return self

    @allure.step("Нажать кнопку Log in")
    def submit(self) -> MainPage:
        self.click(self.login_button)
        return MainPage(self.driver)

    @allure.step("Отправить форму логина клавишей Enter")
    def submit_with_enter(self) -> MainPage:
        self.find(self.password_input).send_keys(Keys.ENTER)
        return MainPage(self.driver)

    def login(self, username: str, password: str) -> MainPage:
        with allure.step(f"Войти как {username}"):
            return self.fill_username(username).fill_password(password).submit()

    def login_with_enter(self, username: str, password: str) -> MainPage:
        with allure.step(f"Войти как {username} через Enter"):
            return self.fill_username(username).fill_password(password).submit_with_enter()

    @allure.step("Перейти к регистрации")
    def go_to_register(self):
        self.click(self.register_link)
        from pages.register_page import RegisterPage
        return RegisterPage(self.driver)
