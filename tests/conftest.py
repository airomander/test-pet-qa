import pytest
from playwright.sync_api import Page, sync_playwright

from config.config import config


@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        yield context
        browser.close()


@pytest.fixture
def page(browser_context) -> Page:
    page = browser_context.new_page()
    page.set_default_timeout(config.timeout)
    page.goto(config.base_url)
    yield page
    page.close()
