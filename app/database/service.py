from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import DATABASE_URI


engine = create_engine(str(DATABASE_URI))
SessionLocal = sessionmaker(bind=engine)
