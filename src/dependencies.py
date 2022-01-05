from typing import Optional, Final
from contextvars import ContextVar
from fastapi import Request, HTTPException, Header
from starlette.datastructures import State


# REQUEST_ID_CTX_KEY: Final[str] = "request_id"
# _request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
#     REQUEST_ID_CTX_KEY, default=None)


# def get_request_id() -> Optional[str]:
#     return _request_id_ctx_var.get()


# def set_request_id(value):
#     return _request_id_ctx_var.set(value)


def get_state(request: Request) -> State:
    return request.state


async def verify_token(xy_token: str = Header(...)):
    pass
    # if xy_token != "secret":
    #     raise HTTPException(status_code=401, detail="X-Token header invalid")


def check_404(value):
    if(value is None):
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return value    