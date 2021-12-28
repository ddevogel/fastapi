from typing import List
from sqlalchemy import create_engine
# from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
from sqlalchemy.ext.automap import automap_base
from .models import Album, Artist, Employee, Genre


class Database:
    def __init__(self):
        self.Base = automap_base()
        self.__engine = create_engine(
            'sqlite:////home/david/dev/python/fastapi/data/chinook.db'
        )
        self.Base.prepare(self.__engine, reflect=True)
        # self.__session = sessionmaker(bind=self.__engine)()
        self.__session = Session(self.__engine)

    @property
    def __session__(self):
        session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine
        )
        try:
            yield session
            session.commit()
        finally:
            session.close()

    def get_albums(self) -> List[Album]:
        query = self.__db__().query(Album)
        return query.all()

    def get_one_album(self) -> Album:
        return self.get_albums()[0]

    def get_artist(self, id) -> Artist:
        return self.__session.query(Artist).get(id)

    def get_employee(self, id: int) -> Employee:
        return (
            self.__session
            .query(Employee)
            .options(joinedload(Employee.parent))
            .get(id)
        )

    def get_genre(self, id: int) -> Genre:
        return self.__session.query(Genre).get(id)

    def update_genre(self, genre: Genre):
        merged = self.__session.merge(genre)
        self.__session.commit()
        self.__session.refresh(merged)
        return merged
