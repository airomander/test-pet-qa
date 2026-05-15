import allure
from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_list = page.locator("[data-test='cart-list']")
        self.cart_items = page.locator("[data-test='inventory-item']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def go_to_checkout(self) -> None:
        with allure.step("Proceed to checkout"):
            self.checkout_button.click()

    def continue_shopping(self) -> None:
        with allure.step("Continue shopping"):
            self.continue_shopping_button.click()

    def remove_item(self, item_name: str) -> None:
        with allure.step(f"Remove '{item_name}' from cart"):
            item = self.page.locator("[data-test='inventory-item']", has_text=item_name)
            item.locator("[data-test*='remove']").click()

    def get_item_names(self) -> list[str]:
        with allure.step("Get cart item names"):
            return self.cart_items.locator("[data-test='inventory-item-name']").all_text_contents()

    def should_have_count(self, count: int) -> None:
        with allure.step(f"Check cart has {count} item(s)"):
            expect(self.cart_items).to_have_count(count)
