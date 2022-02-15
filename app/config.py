import logging

from pydantic import BaseModel
from starlette.config import Config

log = logging.getLogger(__name__)


config = Config(".env")


LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")
DATABASE_URI = config("DATABASE_URI", default=None)
