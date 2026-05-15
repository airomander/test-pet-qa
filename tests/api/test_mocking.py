import pytest
from playwright.sync_api import Browser, Page
from responses import mock as responses_mock

from api_clients.reqres_client import ReqResClient
from config.config import config


class TestMocking:
    def test_route_interception_full_page(self, browser: Browser) -> None:
        context = browser.new_context()
        page = context.new_page()

        def handle(route):
            route.fulfill(
                status=200,
                content_type="text/html",
                body="<html><body><h1>Mocked Page</h1><p>This is a test</p></body></html>"
            )

        page.route("**/*", handle)
        page.goto("https://www.saucedemo.com")

        assert page.locator("h1").text_content() == "Mocked Page"
        assert page.locator("p").text_content() == "This is a test"
        context.close()

    @responses_mock.activate
    def test_mocked_api_error_handling(self) -> None:
        import responses

        responses.get(
            "https://reqres.in/api/users/2",
            status=500,
            json={"error": "Internal Server Error"},
        )

        client = ReqResClient(api_key=config.reqres_api_key)
        response = client.get_user(2)

        assert response.status_code == 500
        assert response.json()["error"] == "Internal Server Error"

    @responses_mock.activate
    def test_mocked_api_response(self) -> None:
        import responses

        responses.get(
            "https://reqres.in/api/users/2",
            status=200,
            json={
                "data": {
                    "id": 2,
                    "email": "mocked@test.com",
                    "first_name": "Mock",
                    "last_name": "User",
                    "avatar": "https://example.com/avatar.jpg",
                },
                "support": {"url": "https://example.com", "text": "Mocked support"},
            },
        )

        client = ReqResClient(api_key=config.reqres_api_key)
        response = client.get_user(2)
        data = response.json()["data"]

        assert data["first_name"] == "Mock"
        assert data["email"] == "mocked@test.com"

    @responses_mock.activate
    def test_mocked_api_network_error(self) -> None:
        import responses
        from requests.exceptions import ConnectionError

        responses.get(
            "https://reqres.in/api/users/2",
            body=ConnectionError("Network is unreachable"),
        )

        client = ReqResClient(api_key=config.reqres_api_key)

        with pytest.raises(ConnectionError):
            client.get_user(2)
