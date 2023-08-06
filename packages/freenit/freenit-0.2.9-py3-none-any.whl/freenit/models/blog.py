import ormar

from ..config import getConfig
from ..models.base import BaseModel
from ..models.metaclass import AllOptional

config = getConfig()


class Blog(BaseModel):
    class Meta(config.meta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=1024)
    content: str = ormar.Text()


class BlogOptional(Blog, metaclass=AllOptional):
    pass
