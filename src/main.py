import logging
from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

from fastapi import Depends, FastAPI, Header, Request
from sqlalchemy.orm import scoped_session
from starlette.middleware.cors import CORSMiddleware

from dependencies import get_state, verify_token, check_404
from artist.views import ArtistView
from src.artist.service import get_artist_view
from src.database.service import SessionLocal
from src.employee.service import get_employee_view
from src.employee.views import EmployeeView
from src.genre.service import get_genre_view, merge_genre
from src.genre.views import GenreView

# uvicorn main:app --app_dir src --reload --port 8001
api = FastAPI()

# artist_service = ArtistService()
# employee_service = EmployeeService()
# genre_service = GenreService()


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


origins = [
    "http://bob"
]


api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["PUT"],
    allow_headers=["*"],
)


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())

    # we create a per-request id such that we can ensure that our session is scoped for a particular request.
    # see: https://github.com/tiangolo/fastapi/issues/726
    ctx_token = _request_id_ctx_var.set(request_id)
    # path_params = get_path_params_from_request(request)

    try:
        session = scoped_session(SessionLocal, scopefunc=get_request_id)
        request.state.db = session()
        request.state.id = request_id
        logging.error(
            f'Pre-processed request with id: {request_id} and uri: {request.url}'
        )
        # logging.error(request.headers["origin"])
        response = await call_next(request)
    finally:
        request.state.db.close()

    _request_id_ctx_var.reset(ctx_token)
    return response


# def check_404(value):
#     if(value is None):
#         raise HTTPException(status_code=404, detail="Item not found")
#     else:
#         return value


# def get_state(request: Request) -> State:
#     return request.state


# async def verify_token(xy_token: str = Header(...)):
#     if xy_token != "secret":
#         raise HTTPException(status_code=401, detail="X-Token header invalid")


@api.get("/employee/{id}", response_model=EmployeeView)
async def employee(id: int, state=Depends(get_state)):
    response = get_employee_view(db_session=state.db, id=id)
    return check_404(response)


# https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
@api.get("/artist/{id}", response_model=ArtistView)
async def artist(id: int, state=Depends(get_state)):
    response = get_artist_view(db_session=state.db, id=id)
    return check_404(response)


@api.get("/genre/{id}", response_model=GenreView)
async def genre(id: int, state=Depends(get_state)):
    response = get_genre_view(db_session=state.db, id=id)
    return check_404(response)


@api.put("/genre")
async def update_genre(genre: GenreView, state=Depends(get_state)):
    return merge_genre(db_session=state.db, genre=genre)
