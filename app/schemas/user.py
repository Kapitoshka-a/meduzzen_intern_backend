from typing import List

from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str
    registered_at: datetime
    role: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdateRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_active: bool


class UsersListResponse(BaseModel):
    users: List[User]


class UserDetailResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    registered_at: datetime
    role: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
