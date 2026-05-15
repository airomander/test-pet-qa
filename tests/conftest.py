import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from config.config import config
from pages.login_page import LoginPage


@pytest.fixture
def auth_page(page: Page) -> Page:
    login_page = LoginPage(page)
    login_page.login(config.standard_user, config.password)
    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name=f"{item.name}.png",
                attachment_type=allure.attachment_type.PNG,
            )
