import allure
from pytest_bdd import when, parsers
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@when(parsers.parse('I add "{item_name}" to cart'))
def _(page: Page, item_name: str):
    with allure.step(f"BDD: add {item_name} to cart"):
        InventoryPage(page).add_item_to_cart(item_name)


@when(parsers.parse("I proceed to checkout"))
def _(page: Page):
    with allure.step("BDD: proceed to checkout"):
        page.locator("[data-test='shopping-cart-link']").click()
        CartPage(page).go_to_checkout()


@when(parsers.parse('I cancel checkout at step one'))
def _(page: Page):
    from pages.checkout_page import CheckoutStepOnePage
    with allure.step("BDD: cancel checkout"):
        page.locator("[data-test='shopping-cart-link']").click()
        CartPage(page).go_to_checkout()
        CheckoutStepOnePage(page).cancel()
