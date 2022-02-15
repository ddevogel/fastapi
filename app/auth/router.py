from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import create_access_token
from .service import authenticate_user
from .views import Login, Token

auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@auth.post("/token", response_model=Token)
async def login_for_access_token_form(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_for_access_token_noform(form_data.username, form_data.password)


@auth.post("/login", response_model=Token)
async def login_for_access_token(login: Login):
    return await login_for_access_token_noform(login.username, login.password)


async def login_for_access_token_noform(username: str, password: str) -> Token:
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_access_token(user)
    #  Move this to dependencies
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={
    #         "sub": user.id,
    #         "nickname": user.username,
    #         "scopes": user.scopes,
    #         "iss": ACCESS_TOKEN_ISSUER,
    #     },
    #     expires_delta=access_token_expires,
    # )
    # return {"access_token": access_token, "token_type": "bearer"}
