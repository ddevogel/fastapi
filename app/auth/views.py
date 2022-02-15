from typing import List

from pydantic import UUID1, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    nickname: str
    scopes: List[str] = []


class Login(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    disabled: bool
    scopes: List[str] = []


class UserInDB(User):
    hashed_password: str
