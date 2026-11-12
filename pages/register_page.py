import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    path = "/register"

    username_input = (By.CSS_SELECTOR, "#username")
    password_input = (By.CSS_SELECTOR, "#password")
    password_submit_input = (By.CSS_SELECTOR, "#passwordSubmit")
    register_button = (By.CSS_SELECTOR, "#register-button")
    error_message = (By.CSS_SELECTOR, ".form__error")
    success_message = (By.CSS_SELECTOR, ".form__paragraph_success")
    login_link = (By.CSS_SELECTOR, "a.form__link[href='/login']")

    @allure.step("Открыть страницу регистрации")
    def open(self) -> "RegisterPage":
        self.driver.get(f"{self.settings.auth_url}{self.path}")
        return self

    @allure.step("Зарегистрировать пользователя {username}")
    def register(self, username: str, password: str, password_submit: str | None = None) -> "RegisterPage":
        self.type_text(self.username_input, username)
        self.type_text(self.password_input, password)
        self.type_text(
            self.password_submit_input,
            password_submit if password_submit is not None else password,
        )
        self.click(self.register_button)
        return self

    @allure.step("Получить текст ошибки")
    def error_text(self) -> str:
        error = self.find(self.error_message)
        self.wait.until(lambda _: error.text.strip() != "")
        return error.text.strip()

    @allure.step("Получить сообщение об успешной регистрации")
    def success_message_text(self) -> str:
        return self.find(self.success_message).text.strip()
