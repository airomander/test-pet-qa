import pytest
from playwright.sync_api import Page, expect

from config.config import config
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestLogin:
    @pytest.mark.smoke
    def test_successful_login(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.login(config.standard_user, config.password)

        inventory_page = InventoryPage(page)
        expect(inventory_page.title).to_be_visible()
        expect(inventory_page.title).to_have_text("Products")

    def test_locked_out_user(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.login(config.locked_out_user, config.password)

        error_text = login_page.get_error_text()
        assert error_text == "Epic sadface: Sorry, this user has been locked out."

    def test_invalid_login(self, page: Page) -> None:
        login_page = LoginPage(page)
        login_page.login("wrong_user", "wrong_pass")

        error_text = login_page.get_error_text()
        assert "Username and password do not match" in error_text
