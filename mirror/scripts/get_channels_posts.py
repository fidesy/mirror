import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest


async def get_channels_posts(client: TelegramClient, usernames: list[str], delay: int = 1) -> list[any]:
    posts = []
    for username in usernames:
        print(username)
        posts_ = await get_posts(client, username)
        posts.append(posts_)
        await asyncio.sleep(delay)


    return posts


async def get_posts(client: TelegramClient, username: str) -> list[any]:
    entity = await client.get_entity(username)

    raw_posts = await client(GetHistoryRequest(
        peer=entity,
        limit=50,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    posts = []

    for post in raw_posts.messages:
        media_url = ""
        try:
            media_url = post.media.webpage.url
        except AttributeError:
            ...

        posts.append((post.id, post.peer_id.channel_id, post.date, post.message, media_url))
    
    return posts