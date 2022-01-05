import logging
# import os
# from typing import List
from pydantic import BaseModel
from starlette.config import Config
# from starlette.datastructures import CommaSeparatedStrings

log = logging.getLogger(__name__)


class BaseConfigurationModel(BaseModel):
    """Base configuration model used by all config options."""
    pass


# def get_env_tags(tag_list: List[str]) -> dict:
#     """Create dictionary of available env tags."""
#     tags = {}
#     for t in tag_list:
#         tag_key, env_key = t.split(":")

#         env_value = os.environ.get(env_key)

#         if env_value:
#             tags.update({tag_key: env_value})

#     return tags


config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

# ENV_TAG_LIST = config("ENV_TAGS", cast=CommaSeparatedStrings, default="")
# ENV_TAGS = get_env_tags(ENV_TAG_LIST)
DATABASE_URI = config("DATABASE_URI", default=None)
