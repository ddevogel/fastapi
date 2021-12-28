from data.database import Database


class BaseService:
    db: Database

    def __init__(self):
        self.db = Database()
