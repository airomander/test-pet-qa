import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from config.config import config
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage, CheckoutStepOnePage, CheckoutStepTwoPage
from pages.header_component import HeaderComponent
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

DATA_DIR = Path(__file__).parent


def load_checkout_data():
    with open(DATA_DIR / "checkout_data.json") as f:
        return json.load(f)


def load_users():
    import csv
    with open(DATA_DIR / "users.csv") as f:
        return list(csv.DictReader(f))


class TestDataDriven:
    @pytest.mark.parametrize("data", load_checkout_data())
    def test_checkout_with_various_data(self, auth_page: Page, data: dict) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")

        header = HeaderComponent(auth_page)
        header.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.go_to_checkout()

        checkout_step_one = CheckoutStepOnePage(auth_page)
        checkout_step_one.fill_details(
            data["first_name"], data["last_name"], data["postal_code"]
        )
        checkout_step_one.continue_checkout()

        if data["valid"]:
            checkout_step_two = CheckoutStepTwoPage(auth_page)
            checkout_step_two.finish()
            CheckoutCompletePage(auth_page).should_have_success_message()
        else:
            error = checkout_step_one.get_error_text()
            assert data["error"] in error

    @pytest.mark.parametrize("user", load_users())
    def test_login_from_csv(self, page: Page, user: dict) -> None:
        login_page = LoginPage(page)
        login_page.login(user["username"], user["password"])

        if user["expected_success"] == "true":
            inventory_page = InventoryPage(page)
            expect(inventory_page.title).to_be_visible()
        else:
            error = login_page.get_error_text()
            assert "locked" in error.lower()
