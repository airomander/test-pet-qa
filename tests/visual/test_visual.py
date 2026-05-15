import allure
import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage


class TestVisualRegression:
    @pytest.mark.skip(reason="Enable to generate baseline screenshots")
    def test_capture_inventory_snapshot(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_open
        screenshot = auth_page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name="inventory_page.png",
            attachment_type=allure.attachment_type.PNG,
        )

    @pytest.mark.skip(reason="Enable to generate baseline screenshots")
    def test_capture_login_snapshot(self, page: Page) -> None:
        assert page.locator("[data-test='login-container']").is_visible()
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name="login_page.png",
            attachment_type=allure.attachment_type.PNG,
        )

    def test_screenshot_with_cart_badge(self, auth_page: Page) -> None:
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        screenshot = auth_page.screenshot(full_page=True)
        assert len(screenshot) > 0
        allure.attach(
            screenshot,
            name="cart_with_badge.png",
            attachment_type=allure.attachment_type.PNG,
        )
