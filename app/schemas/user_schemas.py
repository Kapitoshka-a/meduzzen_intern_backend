from typing import List

from pydantic import BaseModel, EmailStr, model_validator
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    password: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True


class SignInRequestSchema(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    password1: str
    password2: str
    city: str
    phone: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password1 != self.password2:
            raise ValueError("Passwords do not match")
        return self


class SignUpRequestSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdateRequestSchema(BaseModel):
    firstname: str
    lastname: str
    password: str
    city: str
    phone: str

    class Config:
        from_attributes = True


class UserDetailResponseSchema(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True


class UserBriefResponseSchema(BaseModel):
    id: int
    email: EmailStr
    firstname: str
    lastname: str

    class Config:
        from_attributes = True


class UsersListResponseSchema(BaseModel):
    users: List[UserBriefResponseSchema]
