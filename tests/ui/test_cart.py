import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.header_component import HeaderComponent
from pages.inventory_page import InventoryPage


class TestCart:
    @pytest.mark.smoke
    def test_empty_cart_has_no_items(self, auth_page: Page) -> None:
        header = HeaderComponent(auth_page)
        header.go_to_cart()
        cart_page = CartPage(auth_page)
        cart_page.should_have_count(0)

    def test_cart_shows_added_item(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        item_names = cart_page.get_item_names()
        assert "Sauce Labs Backpack" in item_names

    def test_cart_shows_multiple_items(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        inventory_page.add_item_to_cart("Sauce Labs Bike Light")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.should_have_count(2)

    def test_remove_item_from_cart(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        inventory_page.add_item_to_cart("Sauce Labs Bike Light")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.remove_item("Sauce Labs Backpack")
        cart_page.should_have_count(1)

        item_names = cart_page.get_item_names()
        assert "Sauce Labs Backpack" not in item_names

    def test_continue_shopping_returns_to_inventory(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.continue_shopping()

        expect(inventory_page.title).to_be_visible()
        expect(inventory_page.title).to_have_text("Products")
