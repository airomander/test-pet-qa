import allure
from playwright.sync_api import Page, expect


class CheckoutStepOnePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.cancel_button = page.locator("[data-test='cancel']")
        self.error_message = page.locator("[data-test='error']")

    def fill_details(self, first_name: str, last_name: str, postal_code: str) -> None:
        with allure.step(f"Fill checkout form: {first_name} {last_name}, {postal_code}"):
            self.first_name_input.fill(first_name)
            self.last_name_input.fill(last_name)
            self.postal_code_input.fill(postal_code)

    def continue_checkout(self) -> None:
        with allure.step("Continue checkout"):
            self.continue_button.click()

    def cancel(self) -> None:
        with allure.step("Cancel checkout"):
            self.cancel_button.click()

    def get_error_text(self) -> str:
        with allure.step("Get checkout error"):
            return self.error_message.text_content()


class CheckoutStepTwoPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.summary_items = page.locator("[data-test='inventory-item']")
        self.subtotal_label = page.locator("[data-test='subtotal-label']")
        self.tax_label = page.locator("[data-test='tax-label']")
        self.total_label = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")
        self.cancel_button = page.locator("[data-test='cancel']")

    def finish(self) -> None:
        with allure.step("Finish order"):
            self.finish_button.click()

    def cancel(self) -> None:
        with allure.step("Cancel from overview"):
            self.cancel_button.click()

    def get_item_names(self) -> list[str]:
        with allure.step("Get order summary item names"):
            return self.summary_items.locator("[data-test='inventory-item-name']").all_text_contents()

    def should_have_item_count(self, count: int) -> None:
        with allure.step(f"Check order has {count} item(s)"):
            expect(self.summary_items).to_have_count(count)


class CheckoutCompletePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.complete_header = page.locator("[data-test='complete-header']")
        self.complete_text = page.locator("[data-test='complete-text']")
        self.back_home_button = page.locator("[data-test='back-to-products']")

    def back_home(self) -> None:
        with allure.step("Back to products"):
            self.back_home_button.click()

    def should_have_success_message(self) -> None:
        with allure.step("Check order success message"):
            expect(self.complete_header).to_have_text("Thank you for your order!")
