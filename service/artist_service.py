from data.view_models import ArtistView
from service.base_service import BaseService
from type.mapper import Mapper


class ArtistService(BaseService):

    def __init__(self):
        super().__init__()

    def get_artist_view(self, id: int) -> ArtistView:
        artist = self.db.get_artist(id)
        return Mapper.artist_to_view(artist)
