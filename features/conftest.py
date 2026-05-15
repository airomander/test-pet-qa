pytest_plugins = [
    "features.steps.login_steps",
    "features.steps.cart_steps",
    "features.steps.checkout_steps",
]

from playwright.sync_api import Page

from config.config import config
from pages.login_page import LoginPage
import pytest


@pytest.fixture
def bdd_auth(page: Page) -> Page:
    LoginPage(page).login(config.standard_user, config.password)
    return page
