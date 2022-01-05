from ..database.service import SessionLocal
from ..models import Genre
from .views import GenreView


def genre_to_view(genre: Genre) -> GenreView:
    return None if genre is None else GenreView.from_orm(genre)


def view_to_genre(genre: GenreView) -> Genre:
    return Genre(Id=genre.GenreId, Name=genre.Name)


def get_genre_view(db_session: SessionLocal, id: int) -> GenreView:
    genre = db_session.query(Genre).get(id)
    return genre_to_view(genre)


def merge_genre(db_session: SessionLocal, genre: GenreView) -> Genre:
    update = view_to_genre(genre)
    merged = db_session.merge(update)
    db_session.commit()
    db_session.refresh(merged)
    return merged
