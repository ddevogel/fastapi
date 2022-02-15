from contextvars import ContextVar
from datetime import timedelta
from typing import Final, Optional

from fastapi import Header, HTTPException, Request
from starlette.datastructures import State

from app.auth.service import build_access_token
from app.auth.views import UserInDB


class RequestIdContext:
    __REQUEST_ID_CTX_KEY: Final[str] = "request_id"

    def __init__(self):
        self.__request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
            self.__REQUEST_ID_CTX_KEY, default=None
        )
        self.__token = None

    def get_request_id(self) -> Optional[str]:
        return self.__request_id_ctx_var.get()

    def set_request_id(self, value):
        self.__token = self.__request_id_ctx_var.set(value)

    def reset(self):
        self.__request_id_ctx_var.reset(self.__token)


def get_state(request: Request) -> State:
    return request.state


def create_access_token(user: UserInDB):
    return build_access_token(user)


def check_404(value):
    if value is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return value
