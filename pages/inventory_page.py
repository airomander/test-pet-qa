import allure
from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.inventory_items = page.locator("[data-test='inventory-item']")
        self.shopping_cart_badge = page.locator("[data-test='shopping-cart-badge']")

    @property
    def is_open(self) -> bool:
        return self.title.is_visible()

    @property
    def item_count(self) -> int:
        return self.inventory_items.count()

    @property
    def cart_badge_count(self) -> int:
        return int(self.shopping_cart_badge.text_content())

    @property
    def is_cart_badge_visible(self) -> bool:
        return self.shopping_cart_badge.is_visible()

    def add_item_to_cart(self, item_name: str) -> None:
        with allure.step(f"Add '{item_name}' to cart"):
            item = self.page.locator("[data-test='inventory-item']", has_text=item_name)
            item.locator("[data-test*='add-to-cart']").click()

    def go_to_cart(self) -> None:
        with allure.step("Go to cart"):
            self.page.locator("[data-test='shopping-cart-link']").click()
