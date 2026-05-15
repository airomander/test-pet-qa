import pytest
from playwright.sync_api import Page, expect

from config.config import config
from pages.inventory_page import InventoryPage


class TestInventory:
    @pytest.mark.smoke
    def test_inventory_page_displays_products(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        expect(inventory_page.title).to_be_visible()
        expect(inventory_page.title).to_have_text("Products")
        assert inventory_page.item_count == 6

    def test_add_item_to_cart_updates_badge(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        assert inventory_page.cart_badge_count == 1

    def test_add_multiple_items(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        inventory_page.add_item_to_cart("Sauce Labs Bike Light")
        inventory_page.add_item_to_cart("Sauce Labs Onesie")
        assert inventory_page.cart_badge_count == 3

    def test_remove_item_from_cart(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        assert inventory_page.cart_badge_count == 1
        auth_page.locator("[data-test*='remove']").click()
        assert not inventory_page.is_cart_badge_visible

    @pytest.mark.parametrize("username", [
        "standard_user",
        "problem_user",
        "performance_glitch_user",
    ])
    def test_all_users_can_see_products(self, browser, username: str) -> None:
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(config.timeout)
        page.goto(config.base_url)
        from pages.login_page import LoginPage
        login_page = LoginPage(page)
        login_page.login(username, config.password)
        inventory_page = InventoryPage(page)
        expect(inventory_page.title).to_be_visible()
        assert inventory_page.item_count == 6
        context.close()
