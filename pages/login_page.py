import allure
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def go_to(self) -> None:
        with allure.step("Open login page"):
            self.page.goto("/")

    def login(self, username: str, password: str) -> None:
        with allure.step(f"Login as '{username}'"):
            self.username_input.fill(username)
            self.password_input.fill(password)
            self.login_button.click()

    def get_error_text(self) -> str:
        with allure.step("Get login error message"):
            return self.error_message.text_content()
