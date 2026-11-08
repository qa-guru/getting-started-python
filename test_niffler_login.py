import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage

USERNAME = "stas"
PASSWORD = "12345"


@allure.epic("Niffler")
@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешный логин")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Логин с валидными кредами")
    def test_success_login(self, page):
        main_page = LoginPage(page).open().login(USERNAME, PASSWORD)

        with allure.step("Проверить заголовок истории трат"):
            expect(main_page.spendings_section).to_contain_text("History of Spendings")

    @allure.story("Успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Логин с отправкой формы клавишей Enter")
    def test_success_login_with_press_enter(self, page):
        main_page = LoginPage(page).open().login_with_enter(USERNAME, PASSWORD)

        with allure.step("Проверить заголовок истории трат"):
            expect(main_page.spendings_section).to_contain_text("History of Spendings")

    @allure.story("Невалидные креды")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Логин с неверным паролем показывает ошибку")
    def test_wrong_credentials(self, page):
        login_page = LoginPage(page).open()
        login_page.fill_username(USERNAME).fill_password("12345sgsrgwr").submit_with_enter()

        with allure.step("Проверить текст ошибки"):
            expect(login_page.error_message).to_have_text("Bad credentials")
