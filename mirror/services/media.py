from sqlalchemy.orm import Session

from ..client import client
from ..schemas import MediaCreate
from ..crud import add_media


async def add_media(db: Session, media: MediaCreate):
    async with client:
        post = await client.get_entity(media.post_id)
        await client.download_media(post.media, f"./media/{media.photo_id}.png")

    add_media(db, media)
    