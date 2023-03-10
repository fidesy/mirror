from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest

from .database import Database

class Service:

    def __init__(self, DB_URL: str, title: str, api_id: int, api_hash: str) -> None:
        self.title = title
        self.api_id = api_id
        self.api_hash = api_hash
        self.db = Database(DB_URL)
    
    def get_posts(self, skip: int = 0, limit: int = 100, like: str = ""):
        return self.db.get_posts(skip, limit, like)

    def get_channels(self, skip: int = 0, limit: int = 100):
        return self.db.get_channels(skip, limit)

    async def join_channel(self, channel_username: str) -> None:
        async with TelegramClient(self.title, self.api_id, self.api_hash) as client:
            entity = await client.get_entity(channel_username)
            await client(JoinChannelRequest(entity))

    async def leave_channel(self, channel_username: str) -> None:
        async with TelegramClient(self.title, self.api_id, self.api_hash) as client:
            entity = await client.get_entity(channel_username)
            await client(LeaveChannelRequest(entity))

    async def delete_channel(self, channel_username: str) -> None:
        await self.leave_channel(channel_username)
        self.db.delete_channel(channel_username)


    async def add_channel(self, channel_username: str) -> None:
        await self.join_channel(channel_username)
        channel_info = await self.get_channel_info(channel_username)
        posts = await self.parse_posts(channel_username)
        self.db.add_channel(channel_info)
        self.db.add_posts(posts)


    async def get_channel_info(self, channel_username: str):
        async with TelegramClient(self.title, self.api_id, self.api_hash) as client:
            entity = await client.get_entity(channel_username)
            full_info = await client(GetFullChannelRequest(entity))

            # download profile image
            await client.download_profile_photo(entity, f"mirror/data/photos/{entity.id}.png")

            return (entity.id, entity.username, entity.title, full_info.full_chat.about)

    async def parse_posts(self, username: str) -> list[any]:
        async with TelegramClient(self.title, self.api_id, self.api_hash) as client:
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