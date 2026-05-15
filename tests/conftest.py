import time
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, Page, sync_playwright

from config.config import config
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def playwright() -> Generator[sync_playwright, None, None]:
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright) -> Generator[Browser, None, None]:
    browser = playwright.chromium.launch(headless=config.headless)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser):
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    yield context
    context.close()


@pytest.fixture
def page(context) -> Page:
    page = context.new_page()
    page.set_default_timeout(config.timeout)
    page.goto(config.base_url)
    yield page
    page.close()


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
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            timestamp = int(time.time())
            page.screenshot(path=str(screenshots_dir / f"{item.name}_{timestamp}.png"))
