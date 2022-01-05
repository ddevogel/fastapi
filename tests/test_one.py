import json
from io import StringIO
from config import Config
# from data.database import Database
# from data.models import *
# from data.view_models import *

# def test_orm():
#     albums = Database().get_albums()
#     for album in albums:
#         print(album)
#     raise SystemExit(1)


def test_env():
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
