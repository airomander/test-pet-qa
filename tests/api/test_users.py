import pytest

from api_clients.reqres_client import ReqResClient
from schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    SingleUserResponse,
    UpdateUserResponse,
    User,
    UserListResponse,
)


@pytest.mark.requires_api_key
class TestUsers:
    def test_list_users(self, api_client: ReqResClient) -> None:
        response = api_client.list_users(page=2)
        assert response.status_code == 200

        body = UserListResponse.model_validate(response.json())
        assert body.page == 2
        assert len(body.data) > 0
        assert all(isinstance(u, User) for u in body.data)

    def test_get_user(self, api_client: ReqResClient) -> None:
        response = api_client.get_user(2)
        assert response.status_code == 200

        body = SingleUserResponse.model_validate(response.json())
        assert body.data.id == 2
        assert body.data.email == "janet.weaver@reqres.in"

    def test_get_user_not_found(self, api_client: ReqResClient) -> None:
        response = api_client.get_user(23)
        assert response.status_code == 404
        assert response.json() == {}

    def test_create_user(self, api_client: ReqResClient) -> None:
        response = api_client.create_user(name="Roman", job="QA Engineer")
        assert response.status_code == 201

        body = CreateUserResponse.model_validate(response.json())
        assert body.name == "Roman"
        assert body.job == "QA Engineer"
        assert body.id is not None

    def test_update_user(self, api_client: ReqResClient) -> None:
        response = api_client.update_user(user_id=2, name="Roman", job="Senior QA")
        assert response.status_code == 200

        body = UpdateUserResponse.model_validate(response.json())
        assert body.name == "Roman"
        assert body.job == "Senior QA"

    def test_delete_user(self, api_client: ReqResClient) -> None:
        response = api_client.delete_user(2)
        assert response.status_code == 204
