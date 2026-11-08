import allure
from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class MainPage(BasePage):
    path = "/main"

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def spendings_section(self) -> Locator:
        return self.page.locator("#spendings")

    @property
    def history_header(self) -> Locator:
        return self.spendings_section.locator("h2")

    @property
    def menu_button(self) -> Locator:
        return self.page.locator("button[aria-label='Menu']")

    @property
    def sign_out_button(self) -> Locator:
        return self.page.locator("[data-testid='sign-out-btn']")

    @property
    def confirm_logout_button(self) -> Locator:
        return self.page.get_by_role("button", name="Log out")

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.menu_button.click()
        self.sign_out_button.click()
        self.confirm_logout_button.click()
        from pages.login_page import LoginPage
        return LoginPage(self.page)
