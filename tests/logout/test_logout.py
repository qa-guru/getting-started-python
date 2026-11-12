import allure

from pages.login_page import LoginPage


@allure.epic("Niffler")
@allure.feature("Выход из аккаунта")
class TestLogout:

    @allure.story("Логаут")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Выход возвращает на форму логина")
    def test_logout(self, driver, settings, existing_user):
        with allure.step("Логаут из существующего пользователя"):
            login_page = LoginPage(driver, settings).open()
            main_page = login_page.login(existing_user.username, existing_user.password)
            login_page = main_page.logout()

        with allure.step("Проверить, что отображается форма логина"):
            login_page.wait_until_open()
