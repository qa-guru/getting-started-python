import allure

from pages.login_page import LoginPage
from test_data.consts.auth import BAD_CREDENTIALS_ERRORS, WRONG_PASSWORD
from test_data.consts.main_page import HISTORY_HEADER_TEXT


@allure.epic("Niffler")
@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешный логин")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Логин с валидными кредами")
    def test_success_login(self, driver, settings, existing_user):
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver, settings).open()

        with allure.step("Войти под существующим пользователем"):
            main_page = login_page.login(
                existing_user.username, existing_user.password
            )

        with allure.step("Проверить заголовок истории трат"):
            header = main_page.history_header_text()
            assert header == HISTORY_HEADER_TEXT, \
                f"Ожидался заголовок {HISTORY_HEADER_TEXT!r}, получен {header!r}"

    @allure.story("Успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Логин с отправкой формы клавишей Enter")
    def test_success_login_with_press_enter(self, driver, settings, existing_user):
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver, settings).open()

        with allure.step("Войти под существующим пользователем через Enter"):
            main_page = login_page.login_with_enter(
                existing_user.username, existing_user.password
            )

        with allure.step("Проверить заголовок истории трат"):
            header = main_page.history_header_text()
            assert header == HISTORY_HEADER_TEXT, \
                f"Ожидался заголовок {HISTORY_HEADER_TEXT!r}, получен {header!r}"

    @allure.story("Невалидные креды")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Логин с неверным паролем показывает ошибку")
    def test_wrong_credentials(self, driver, settings, existing_user):
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(driver, settings).open()

        with allure.step("Отправить форму с неверным паролем"):
            login_page.fill_username(existing_user.username) \
                .fill_password(WRONG_PASSWORD) \
                .submit_with_enter()

        with allure.step("Проверить текст ошибки"):
            error = login_page.error_text()
            assert error in BAD_CREDENTIALS_ERRORS, \
                f"Ожидался один из текстов {BAD_CREDENTIALS_ERRORS!r}, получен {error!r}"
