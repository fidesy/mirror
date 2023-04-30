from sqlalchemy import Column, Integer, BigInteger, ForeignKeyConstraint

from ..database import Base
from .post import Post


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    post_id = Column(Integer)
    photo_id = Column(BigInteger)

    __table_args__ = (ForeignKeyConstraint([channel_id, post_id], [Post.channel_id, Post.post_id]), {})




