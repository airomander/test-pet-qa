from pytest_bdd import given, parsers

from config.config import config
from pages.login_page import LoginPage


@given("I am on the login page")
def _() -> None:
    pass


@given(parsers.parse("I am logged in as {username}"))
def _(page, username) -> None:
    login_page = LoginPage(page)
    login_page.login(username, config.password)
