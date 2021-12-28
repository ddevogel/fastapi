from data.models import Artist, Employee, Genre
from data.view_models import ArtistView, EmployeeView, GenreView


class Mapper:
    @staticmethod
    def artist_to_view(artist: Artist) -> ArtistView:
        if artist is None:
            return None
        view = ArtistView.from_orm(artist)
        return view

    @staticmethod
    def employee_to_view(employee: Employee) -> EmployeeView:
        if employee is None:
            return None
        view = EmployeeView.from_orm(employee)
        view.__setattr__("Manager", view.from_orm(employee.parent))
        return view

    @staticmethod
    def genre_to_view(genre: Genre) -> GenreView:
        if genre is None:
            return None
        view = GenreView.from_orm(genre)
        return view

    @staticmethod
    def view_to_genre(genre: GenreView) -> Genre:
        return Genre(GenreId=genre.Id, Name=genre.Name)
