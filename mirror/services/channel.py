from datetime import datetime, date, timedelta
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.types import Channel, MessageMediaPhoto
from sqlalchemy.orm import Session


from .. import crud
from ..schemas.channel import ChannelCreate
from ..schemas.post import PostCreate
from ..schemas.media import MediaCreate
from ..client import client


async def add_channel(db: Session, channel_username: str) -> None:
    async with client:
        entity = await client.get_entity(channel_username)

        await __join_channel(client, entity)

        channel_info = await __get_channel_info(client, entity)

        raw_posts = await __get_posts(client, entity, (date.today()+timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
        posts, media = await parse_posts(client, raw_posts[::-1])

    crud.add_channel(db, ChannelCreate(**channel_info))

    for post in posts:
        crud.add_post(db, PostCreate(**post))

    for m in media:
        crud.add_media(db, MediaCreate(**m))


async def __join_channel(client: TelegramClient, entity: Channel) -> None:
    await client(JoinChannelRequest(entity))


async def __get_channel_info(client: TelegramClient, entity: Channel) -> dict:
    full_info = await client(GetFullChannelRequest(entity))

    await client.download_profile_photo(entity, f"./photos/{entity.id}.png")

    return {
        "id": entity.id, 
        "username": entity.username, 
        "title": entity.title, 
        "description": full_info.full_chat.about,
    }


async def __get_posts(client: TelegramClient, entity: Channel, offset_date: str) -> list[dict]:
    raw_posts = await client(GetHistoryRequest(
        peer=entity,
        limit=50,
        offset_date=datetime.fromisoformat(offset_date),
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0,
    ))
    
    return raw_posts.messages


async def parse_posts(client: TelegramClient, raw_posts: list[dict]):
    latest_post_id = 0
    posts = []
    media = []
    for post in raw_posts:
        channel_id = post.peer_id.channel_id
        message = post.message
        if not message:
            post.id = latest_post_id

        if post.media:
            if isinstance(post.media, MessageMediaPhoto):
                photo_id = post.media.photo.id
                await client.download_media(post.media, f"./media/{photo_id}.png")

                media.append({
                    "channel_id": channel_id,
                    "post_id": post.id,
                    "photo_id": photo_id
                })

        if message: 
            posts.append({
                "post_id": post.id,
                "channel_id": channel_id,
                "date": post.date,
                "message": message,
            })
            latest_post_id = post.id

    return posts, media


async def delete_channel(db: Session, username: str):
    async with client:
        entity = await client.get_entity(username)
        await __leave_channel(client, entity)

    channel_db = crud.get_channel_by_username(db, username)
    for post in channel_db.posts:
        crud.delete_post(db, post.id)

    crud.delete_channel(db, username)




async def __leave_channel(client: TelegramClient, entity: Channel) -> None:
    await client(LeaveChannelRequest(entity))


