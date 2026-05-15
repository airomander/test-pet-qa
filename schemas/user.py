from datetime import datetime

from pydantic import BaseModel, EmailStr

from schemas.common import Support


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str


class UserListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]
    support: Support


class SingleUserResponse(BaseModel):
    data: User
    support: Support


class CreateUserRequest(BaseModel):
    name: str
    job: str


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: datetime


class UpdateUserRequest(BaseModel):
    name: str
    job: str


class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str


class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    id: int
    token: str
