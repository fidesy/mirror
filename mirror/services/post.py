from sqlalchemy.orm import Session
from telethon.types import MessageMediaPhoto
from telethon.tl.types import PeerChannel

from ..schemas import PostCreate, MediaCreate
from ..client import client
from .. import crud


async def add_post(db: Session, post: PostCreate):
    async with client:
        channel = await client.get_entity(PeerChannel(post.channel_id))

        messages = await client.get_messages(channel)
        message = messages[0]

        if message.id == post.post_id and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                photo_id = message.media.photo.id
                await client.download_media(message.media, f"./media/{photo_id}.png")
            
                crud.add_media(db, MediaCreate(
                    channel_id=post.channel_id,
                    post_id=post.post_id,
                    photo_id=message.media.photo.id,
                ))

        if post.message:
           crud.add_post(db, PostCreate(
                post_id=post.post_id,
                channel_id=post.channel_id,
                date=post.date,
                message=post.message,
           ))