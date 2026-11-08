import uuid

import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.register_page import RegisterPage


def _unique_username() -> str:
    return f"user_{uuid.uuid4().hex[:10]}"


@allure.epic("Niffler")
@allure.feature("Регистрация")
class TestRegistration:

    @allure.story("Успешная регистрация")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Регистрация нового пользователя")
    def test_successful_registration(self, page):
        register_page = RegisterPage(page).open()
        register_page.register(_unique_username(), "12345")

        with allure.step("Проверить сообщение об успешной регистрации"):
            expect(register_page.success_message).to_have_text(
                "Congratulations! You've registered!"
            )

    @allure.story("Валидация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Несовпадающие пароли показывают ошибку")
    def test_registration_with_mismatched_passwords(self, page):
        register_page = RegisterPage(page).open()
        register_page.register(_unique_username(), "12345", password_submit="54321")

        with allure.step("Проверить текст ошибки"):
            expect(register_page.error_message).to_have_text("Passwords should be equal")

    @allure.story("Валидация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Занятое имя пользователя показывает ошибку")
    def test_registration_with_existing_username(self, page):
        register_page = RegisterPage(page).open()
        register_page.register("stas", "12345")

        with allure.step("Проверить текст ошибки"):
            expect(register_page.error_message).to_have_text("Username `stas` already exists")


@allure.epic("Niffler")
@allure.feature("Выход из аккаунта")
class TestLogout:

    @allure.story("Логаут")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Выход возвращает на форму логина")
    def test_logout(self, page):
        main_page = LoginPage(page).open().login("stas", "12345")
        login_page = main_page.logout()

        with allure.step("Проверить, что отображается форма логина"):
            expect(login_page.login_button).to_be_visible()
