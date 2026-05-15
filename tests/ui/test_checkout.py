import pytest
from playwright.sync_api import Page

from config.config import config
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage, CheckoutStepOnePage, CheckoutStepTwoPage
from pages.header_component import HeaderComponent
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestCheckout:
    @pytest.mark.smoke
    def test_full_checkout_flow(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        inventory_page.add_item_to_cart("Sauce Labs Bike Light")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.fill_details("Roman", "Savchenko", "400001")
        checkout_step_one.continue_checkout()

        checkout_step_two = CheckoutStepTwoPage(auth_page)
        checkout_step_two.should_have_item_count(2)
        checkout_step_two.finish()

        checkout_complete = CheckoutCompletePage(auth_page)
        checkout_complete.should_have_success_message()

    def test_checkout_without_items(self, auth_page: Page) -> None:
        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.fill_details("Roman", "Savchenko", "400001")
        checkout_step_one.continue_checkout()

        checkout_step_two = CheckoutStepTwoPage(auth_page)
        checkout_step_two.should_have_item_count(0)
        checkout_step_two.finish()

        checkout_complete = CheckoutCompletePage(auth_page)
        checkout_complete.should_have_success_message()

    def test_checkout_required_fields(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.continue_checkout()

        error_text = checkout_step_one.get_error_text()
        assert "First Name is required" in error_text

    def test_checkout_cancel_from_step_one(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.cancel()

        cart_page.should_have_count(1)

    def test_checkout_cancel_from_overview(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.fill_details("Roman", "Savchenko", "400001")
        checkout_step_one.continue_checkout()

        checkout_step_two = CheckoutStepTwoPage(auth_page)
        checkout_step_two.cancel()

        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_open

    def test_logout_after_checkout(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.fill_details("Roman", "Savchenko", "400001")
        checkout_step_one.continue_checkout()

        checkout_step_two = CheckoutStepTwoPage(auth_page)
        checkout_step_two.finish()

        checkout_complete = CheckoutCompletePage(auth_page)
        checkout_complete.should_have_success_message()

        header.logout()

        login_page = LoginPage(auth_page)
        assert login_page.login_button.is_visible()

    @pytest.mark.parametrize("username", [
        "standard_user",
        pytest.param("problem_user", marks=pytest.mark.xfail(reason="problem_user has broken UI — expected")),
    ])
    def test_checkout_for_multiple_users(self, browser, username: str) -> None:
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(config.timeout)
        page.goto(config.base_url)

        login_page = LoginPage(page)
        login_page.login(username, config.password)

        inventory_page = InventoryPage(page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(page)
        header.go_to_cart()

        cart_page = CartPage(page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(page)
        checkout_step_one.fill_details("Roman", "Savchenko", "400001")
        checkout_step_one.continue_checkout()

        checkout_step_two = CheckoutStepTwoPage(page)
        checkout_step_two.finish()

        checkout_complete = CheckoutCompletePage(page)
        checkout_complete.should_have_success_message()

        context.close()
