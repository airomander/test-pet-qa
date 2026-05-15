import allure
from pytest_bdd import when, then, parsers
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage, CheckoutStepOnePage, CheckoutStepTwoPage
from pages.inventory_page import InventoryPage


@when(parsers.parse('I fill shipping details with "{first_name}" "{last_name}" "{postal_code}"'))
def _(page: Page, first_name: str, last_name: str, postal_code: str):
    with allure.step(f"BDD: fill shipping details"):
        checkout = CheckoutStepOnePage(page)
        checkout.fill_details(first_name, last_name, postal_code)
        checkout.continue_checkout()


@when("I finish the order")
def _(page: Page):
    with allure.step("BDD: finish order"):
        CheckoutStepTwoPage(page).finish()


@when("I click continue without filling details")
def _(page: Page):
    with allure.step("BDD: click continue with empty form"):
        CheckoutStepOnePage(page).continue_checkout()


@then(parsers.parse('I should see "{message}"'))
def _(page: Page, message: str):
    with allure.step(f"BDD: verify success message"):
        CheckoutCompletePage(page).should_have_success_message()


@then(parsers.parse('I should be on cart page with {count:d} item'))
def _(page: Page, count: int):
    with allure.step(f"BDD: verify cart has {count} items"):
        CartPage(page).should_have_count(count)


@then(parsers.parse('I should see error "{text}"'))
def _(page: Page, text: str):
    with allure.step(f'BDD: verify error "{text}"'):
        error = CheckoutStepOnePage(page).get_error_text()
        assert text in error


@then("I should see 6 products in inventory")
def _(page: Page):
    with allure.step("BDD: verify 6 products"):
        inventory = InventoryPage(page)
        assert inventory.item_count == 6


@then("the cart badge should show 1")
def _(page: Page):
    with allure.step("BDD: verify cart badge"):
        inventory = InventoryPage(page)
        assert inventory.cart_badge_count == 1


@then("I should be on the inventory page")
def _(page: Page):
    with allure.step("BDD: verify on inventory"):
        expect(page.locator("[data-test='title']")).to_have_text("Products")


@when(parsers.parse('I login with "{username}" and "{password}"'))
def _(page: Page, username: str, password: str):
    from pages.login_page import LoginPage
    with allure.step(f"BDD: login as {username}"):
        LoginPage(page).login(username, password)
