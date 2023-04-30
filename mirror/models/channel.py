from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    title = Column(String(100))
    description = Column(String)

    posts = relationship("Post")

