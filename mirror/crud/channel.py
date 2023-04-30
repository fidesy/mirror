from sqlalchemy.orm import Session

from ..schemas.channel import ChannelCreate
from ..models.channel import Channel


def add_channel(db: Session, channel: ChannelCreate) -> Channel:
    db_channel = Channel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


def get_channel_by_username(db: Session, username: str) -> Channel | None:
    return db.query(Channel).filter(Channel.username == username).first()


def update_channel(db: Session, channel: ChannelCreate) -> Channel:
    db_channel = get_channel_by_username(db, channel.username)
    db_channel = Channel(**channel.dict(), id=db_channel.id)
    db.commit()
    db.refresh(db_channel)
    return db_channel


def delete_channel(db: Session, username: str) -> int:
    status = db.query(Channel).filter(Channel.username == username).delete()
    db.commit()
    return status