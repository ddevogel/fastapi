from ..database.service import SessionLocal
from ..models import Artist
from .views import ArtistView


def artist_to_view(artist: Artist) -> ArtistView:
    return None if artist is None else ArtistView.from_orm(artist)


def get_artist_view(db_session: SessionLocal, id: int) -> ArtistView:
    artist = db_session.query(Artist).get(id)
    return artist_to_view(artist)
