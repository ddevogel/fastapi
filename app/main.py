import logging
from uuid import uuid1

from fastapi import Depends, FastAPI, Header, Request, Response
from passlib.hash import pbkdf2_sha512
from sqlalchemy.orm import scoped_session
from starlette.middleware.cors import CORSMiddleware

from app.artist.router import artists
from app.auth.router import auth
from app.database.service import SessionLocal
from app.dependencies import RequestIdContext
from app.employee.router import employees
from app.genre.router import genres

hash = pbkdf2_sha512.using(rounds=1000000, salt_size=10).hash("password")
print(hash)

# uvicorn main:app --app_dir app --reload --port 8001
api = FastAPI()


origins = ["http://bob"]


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
            SessionLocal, scopefunc=request_id_context.get_request_id
        )
        request.state.db = session()
        request.state.id = request_id
        # logging.error(
        #     f'Pre-processed request with id: {request_id} and uri: {request.url}'
        # )
        # logging.error(request.headers["origin"])
        response = await call_next(request)
    finally:
        request.state.db.close()

    request_id_context.reset()
    return response


api.include_router(auth)
api.include_router(artists)
api.include_router(employees)
api.include_router(genres)
