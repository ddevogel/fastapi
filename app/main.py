import logging
from uuid import uuid1

from fastapi import Depends, FastAPI, Header, Request, Response
from sqlalchemy.orm import scoped_session
from starlette.middleware.cors import CORSMiddleware

from app.dependencies import RequestIdContext
from app.artist.router import artists
from app.database.service import SessionLocal
from app.employee.router import employees
from app.genre.router import genres


# uvicorn main:app --app_dir app --reload --port 8001
api = FastAPI()


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
    # ctx_token = _request_id_ctx_var.set(request_id)
    request_id_context = RequestIdContext()
    request_id_context.set_request_id(request_id)
    # path_params = get_path_params_from_request(request)

    try:
        session = scoped_session(
            SessionLocal, scopefunc=request_id_context.get_request_id)
        request.state.db = session()
        request.state.id = request_id
        # logging.error(
        #     f'Pre-processed request with id: {request_id} and uri: {request.url}'
        # )
        # logging.error(request.headers["origin"])
        response = await call_next(request)
    finally:
        request.state.db.close()

    # _request_id_ctx_var.reset(ctx_token)
    request_id_context.reset()
    return response


# https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
# @api.get("/artist/{id}", response_model=ArtistView)
# async def artist(id: int, state=Depends(get_state)):
#     response = get_artist_view(db_session=state.db, id=id)
#     return check_404(response)


# @api.get("/employee/{id}", response_model=EmployeeView)
# async def employee(id: int, state=Depends(get_state)):
#     response = get_employee_view(db_session=state.db, id=id)
#     return check_404(response)


# @api.get("/genre/{id}", response_model=GenreView)
# async def genre(id: int, response: Response, state=Depends(get_state)):
#     result = get_genre_view(db_session=state.db, id=id)
#     response.headers["request_id"] = state.id
#     return check_404(result)


# @api.put("/genre")
# async def update_genre(genre: GenreView, state=Depends(get_state)):
#     return merge_genre(db_session=state.db, genre=genre)

api.include_router(artists)
api.include_router(employees)
api.include_router(genres)
