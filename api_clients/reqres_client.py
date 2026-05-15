from api_clients.base_client import BaseAPIClient
from config.config import config
from schemas.user import (
    CreateUserRequest,
    LoginRequest,
    RegisterRequest,
    UpdateUserRequest,
)


class ReqResClient(BaseAPIClient):
    def __init__(self, base_url: str = "https://reqres.in/api", api_key: str = config.reqres_api_key) -> None:
        super().__init__(base_url, api_key=api_key)

    def list_users(self, page: int = 1) -> "Response":
        return self.get(f"/users?page={page}")

    def get_user(self, user_id: int) -> "Response":
        return self.get(f"/users/{user_id}")

    def create_user(self, name: str, job: str) -> "Response":
        payload = CreateUserRequest(name=name, job=job).model_dump()
        return self.post("/users", json=payload)

    def update_user(self, user_id: int, name: str, job: str) -> "Response":
        payload = UpdateUserRequest(name=name, job=job).model_dump()
        return self.put(f"/users/{user_id}", json=payload)

    def delete_user(self, user_id: int) -> "Response":
        return self.delete(f"/users/{user_id}")

    def login(self, email: str, password: str) -> "Response":
        payload = LoginRequest(email=email, password=password).model_dump()
        return self.post("/login", json=payload)

    def register(self, email: str, password: str) -> "Response":
        payload = RegisterRequest(email=email, password=password).model_dump()
        return self.post("/register", json=payload)
