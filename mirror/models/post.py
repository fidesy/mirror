from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    channel_id = Column(Integer, ForeignKey("channels.id"))
    date = Column(DateTime)
    message = Column(String)

    channel = relationship("Channel", backref="post")
    media = relationship("Media", backref="post")