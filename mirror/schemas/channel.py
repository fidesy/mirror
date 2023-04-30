from pydantic import BaseModel

# from .post import Post


class ChannelBase(BaseModel):
    id: int
    username: str
    title: str
    description: str


class ChannelCreate(ChannelBase):
    ...


class Channel(ChannelBase):
    # posts: list[Post] = []

    class Config:
        orm_mode = True