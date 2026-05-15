import pytest
from requests import HTTPError

from api_clients.reqres_client import ReqResClient
from schemas.user import LoginResponse, RegisterResponse


class TestAuth:
    def test_login_successful(self, api_client: ReqResClient) -> None:
        response = api_client.login(email="eve.holt@reqres.in", password="cityslicka")
        assert response.status_code == 200

        body = LoginResponse.model_validate(response.json())
        assert body.token is not None

    def test_login_unsuccessful(self, api_client: ReqResClient) -> None:
        response = api_client.login(email="peter@klaven", password="")
        assert response.status_code == 400

        body = response.json()
        assert "error" in body

    def test_register_successful(self, api_client: ReqResClient) -> None:
        response = api_client.register(
            email="eve.holt@reqres.in", password="pistol"
        )
        assert response.status_code == 200

        body = RegisterResponse.model_validate(response.json())
        assert body.id == 4
        assert body.token is not None
