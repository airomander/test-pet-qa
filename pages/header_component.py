import allure
from playwright.sync_api import Page


class HeaderComponent:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")

    @property
    def is_cart_badge_visible(self) -> bool:
        return self.cart_badge.is_visible()

    @property
    def cart_badge_count(self) -> int:
        return int(self.cart_badge.text_content())

    def go_to_cart(self) -> None:
        with allure.step("Navigate to cart via header"):
            self.cart_link.click()

    def logout(self) -> None:
        with allure.step("Logout from application"):
            self.menu_button.click()
            self.logout_link.click()
