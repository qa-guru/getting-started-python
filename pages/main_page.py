import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class MainPage(BasePage):
    path = "/main"

    spendings_section = (By.CSS_SELECTOR, "#spendings")
    history_header = (By.CSS_SELECTOR, "#spendings h2")
    menu_button = (By.CSS_SELECTOR, "button[aria-label='Menu']")
    sign_out_button = (By.CSS_SELECTOR, "[data-testid='sign-out-btn']")
    confirm_logout_button = (By.XPATH, "//button[@data-testid='dialog-submit-btn' or normalize-space()='Log out']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Выйти из аккаунта")
    def logout(self):
        # нативный клик chromedriver не открывает MUI-меню в headless — кликаем через JS
        self.js_click(self.menu_button)
        self.js_click(self.sign_out_button)
        self.js_click(self.confirm_logout_button)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)
