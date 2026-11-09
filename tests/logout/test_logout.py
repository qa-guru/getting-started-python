import allure
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage


@allure.epic("Niffler")
@allure.feature("Выход из аккаунта")
class TestLogout:

    @allure.story("Логаут")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Выход возвращает на форму логина")
    def test_logout(self, driver, wait):
        main_page = LoginPage(driver).open().login("stas", "12345")
        login_page = main_page.logout()

        with allure.step("Проверить, что отображается форма логина"):
            wait.until(EC.visibility_of_element_located(login_page.login_button))
