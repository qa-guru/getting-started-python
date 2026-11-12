import allure

from pages.register_page import RegisterPage
from test_data.consts.registration import (
    MISMATCHED_PASSWORD_SUFFIX,
    PASSWORDS_MISMATCH_ERROR,
    REGISTRATION_SUCCESS_MESSAGE,
    USERNAME_TAKEN_ERROR_TEMPLATE,
)


@allure.epic("Niffler")
@allure.feature("Регистрация")
class TestRegistration:

    @allure.story("Успешная регистрация")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Регистрация нового пользователя")
    def test_successful_registration(self, driver, settings, new_user):
        with allure.step("Открыть страницу регистрации"):
            register_page = RegisterPage(driver, settings).open()

        with allure.step("Зарегистрировать нового пользователя"):
            register_page.register(new_user.username, new_user.password)

        with allure.step("Проверить сообщение об успешной регистрации"):
            message = register_page.success_message_text()
            assert message == REGISTRATION_SUCCESS_MESSAGE, \
                f"Ожидалось сообщение {REGISTRATION_SUCCESS_MESSAGE!r}, получено {message!r}"

    @allure.story("Валидация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Несовпадающие пароли показывают ошибку")
    def test_registration_with_mismatched_passwords(self, driver, settings, new_user):
        with allure.step("Открыть страницу регистрации"):
            register_page = RegisterPage(driver, settings).open()

        with allure.step("Отправить форму с несовпадающими паролями"):
            register_page.register(
                new_user.username,
                new_user.password,
                password_submit=new_user.password + MISMATCHED_PASSWORD_SUFFIX,
            )

        with allure.step("Проверить текст ошибки"):
            error = register_page.error_text()
            assert error == PASSWORDS_MISMATCH_ERROR, \
                f"Ожидалась ошибка {PASSWORDS_MISMATCH_ERROR!r}, получена {error!r}"

    @allure.story("Валидация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Занятое имя пользователя показывает ошибку")
    def test_registration_with_existing_username(self, driver, settings, existing_user, new_user):
        with allure.step("Открыть страницу регистрации"):
            register_page = RegisterPage(driver, settings).open()

        with allure.step("Отправить форму с занятым именем пользователя"):
            register_page.register(existing_user.username, new_user.password)

        with allure.step("Проверить текст ошибки"):
            error = register_page.error_text()
            expected = USERNAME_TAKEN_ERROR_TEMPLATE.format(existing_user.username)
            assert error == expected, \
                f"Ожидалась ошибка {expected!r}, получена {error!r}"
