from sqlalchemy.orm import Session

from ..schemas.media import MediaCreate
from ..models.media import Media


def add_media(db: Session, media: MediaCreate) -> Media:
    db_media = Media(**media.dict())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media