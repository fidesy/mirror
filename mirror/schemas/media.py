from pydantic import BaseModel


class MediaBase(BaseModel):
    channel_id: int
    post_id: int
    photo_id: str


class MediaCreate(MediaBase):
    ...


class Media(MediaBase):
    id: int

    class Config:
        orm_mode = True