from typing import TYPE_CHECKING

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.login_page import LoginPage


class MainPage(BasePage):
    path = "/main"

    spendings_section = (By.CSS_SELECTOR, "#spendings")
    history_header = (By.CSS_SELECTOR, "#spendings h2")
    menu_button = (By.CSS_SELECTOR, "button[aria-label='Menu']")
    sign_out_button = (By.CSS_SELECTOR, "[data-testid='sign-out-btn']")
    confirm_logout_button = (By.XPATH, "//button[@data-testid='dialog-submit-btn' or normalize-space()='Log out']")

    @allure.step("Ожидание открытия главной страницы")
    def wait_until_open(self) -> "MainPage":
        self.wait.url_contains(self.path)
        self.wait.visible(self.spendings_section)
        return self

    @allure.step("Получить заголовок истории трат")
    def history_header_text(self) -> str:
        return self.find(self.history_header).text.strip()

    @allure.step("Выйти из аккаунта")
    def logout(self) -> "LoginPage":
        # нативный клик chromedriver не открывает MUI-меню в headless — кликаем через JS
        self.js_click(self.menu_button)
        self.js_click(self.sign_out_button)
        self.js_click(self.confirm_logout_button)
        from pages.login_page import LoginPage
        return LoginPage(self.driver, self.settings)
