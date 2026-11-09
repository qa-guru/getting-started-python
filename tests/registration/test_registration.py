import uuid

import allure
from selenium.webdriver.support import expected_conditions as EC

from pages.register_page import RegisterPage


def _unique_username() -> str:
    return f"user_{uuid.uuid4().hex[:10]}"


@allure.epic("Niffler")
@allure.feature("Регистрация")
class TestRegistration:

    @allure.story("Успешная регистрация")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Регистрация нового пользователя")
    def test_successful_registration(self, driver, wait):
        register_page = RegisterPage(driver).open()
        register_page.register(_unique_username(), "12345")

        with allure.step("Проверить сообщение об успешной регистрации"):
            wait.until(EC.text_to_be_present_in_element(
                register_page.success_message,
                "Congratulations! You've registered!",
            ))

    @allure.story("Валидация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Несовпадающие пароли показывают ошибку")
    def test_registration_with_mismatched_passwords(self, driver, wait):
        register_page = RegisterPage(driver).open()
        register_page.register(_unique_username(), "12345", password_submit="54321")

        with allure.step("Проверить текст ошибки"):
            wait.until(EC.text_to_be_present_in_element(
                register_page.error_message, "Passwords should be equal"
            ))

    @allure.story("Валидация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Занятое имя пользователя показывает ошибку")
    def test_registration_with_existing_username(self, driver, wait):
        register_page = RegisterPage(driver).open()
        register_page.register("stas", "12345")

        with allure.step("Проверить текст ошибки"):
            wait.until(EC.text_to_be_present_in_element(
                register_page.error_message, "Username `stas` already exists"
            ))
