from typing import Generator

import pytest
from playwright.sync_api import Browser, Page, sync_playwright

from config.config import config


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
