from data.view_models import GenreView
from service.base_service import BaseService
from type.mapper import Mapper


class GenreService(BaseService):

    def __init__(self):
        super().__init__()

    def get_genre_view(self, id: int) -> GenreView:
        genre = self.db.get_genre(id)
        return Mapper.genre_to_view(genre)

    def update_genre(self, genre: GenreView):
        self.db.update_genre(Mapper.view_to_genre(genre))
