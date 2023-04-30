from datetime import datetime
from pydantic import BaseModel

from .media import Media
from .channel import Channel

class PostBase(BaseModel):
    post_id: int
    channel_id: int
    date: datetime
    message: str


class PostCreate(PostBase):
    ...


class Post(PostBase):
    id: int
    channel: Channel = None
    media: list[Media] = []

    class Config:
        orm_mode = True