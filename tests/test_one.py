import json
from io import StringIO
from logging import error
from operator import is_not
from typing import BinaryIO
import pytest
from uuid import UUID, uuid1

from sqlalchemy import null

# import asyncio
from app.config import Config
# from data.database import Database
# from data.models import *
# from data.view_models import *
from unittest import mock
from unittest.mock import Mock, MagicMock
from app.main import db_session_middleware
# def test_orm():
#     albums = Database().get_albums()
#     for album in albums:
#         print(album)
#     raise SystemExit(1)
from fastapi import Request


class bob:
    def x():
        return "x"


async def noop(r: Request) -> Request:
    return r


@pytest.mark.asyncio
async def test_middleware():
    r = Request({"type": "http", "method": "GET", "path": "/abc/", "url": "url"})

    x = await db_session_middleware(r, noop)
    assert r.state is not None
    i = UUID(str(r.state.id))
    assert r.state.db is not None

 



    assert(len(x.state.id)==36)
    # s = r


def test_env():
    s = bob()
    s.x = Mock(return_value="y")
    print(s.x())

    # m = Mock(Config)

    c = Config(".env")
    v = c("DATABASE_URI")
    assert v == 3


def test_map():
    # d = Database().get_one_album()
    # print(AlbumView(d).Title)
    # d = Database().get_artist()
    # print(Mapper.ArtistView(d))
    p = [{'name': 'dave', 'pwd': 'password'}]
    io = StringIO()
    map(lambda x: json.dump(delattr(x, 'name'), io), p)
    print(io.getvalue())
    assert True
