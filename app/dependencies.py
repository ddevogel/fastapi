from typing import Optional, Final
from contextvars import ContextVar
from fastapi import Request, HTTPException, Header
from starlette.datastructures import State


class RequestIdContext:
    __REQUEST_ID_CTX_KEY: Final[str] = "request_id"

    def __init__(self):
        self.__request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
            self.__REQUEST_ID_CTX_KEY, default=None)
        self.__token = None

    def get_request_id(self) -> Optional[str]:
        return self.__request_id_ctx_var.get()

    def set_request_id(self, value):
        self.__token = self.__request_id_ctx_var.set(value)

    def reset(self):
        self.__request_id_ctx_var.reset(self.__token)


def get_state(request: Request) -> State:
    return request.state


async def verify_token(auth_token: str = Header(...)):
    # pass
    if auth_token != "secret":
        raise HTTPException(status_code=401, detail="auth_token header invalid")


def check_404(value):
    if(value is None):
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return value
