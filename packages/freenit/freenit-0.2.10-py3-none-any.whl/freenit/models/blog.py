import ormar

from freenit.config import getConfig

from ..models.base import BaseModel
from ..models.metaclass import AllOptional

config = getConfig()


class Blog(BaseModel):
    class Meta(config.meta):
        pass

    id: int = ormar.Integer(primary_key=True)


class BlogOptional(Blog, metaclass=AllOptional):
    pass
