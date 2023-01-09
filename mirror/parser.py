import asyncio
from dotenv import load_dotenv
import os
from telethon import TelegramClient

from database import Database
from scripts.get_channels_info import get_channels_info
from scripts.get_channels_posts import get_channels_posts
from scripts.utils import load_txt


async def main():
    load_dotenv()

    db = Database(os.getenv("DBURL"))

    channels_txt = load_txt("mirror/data/channels.txt")

    async with TelegramClient(os.getenv("TITLE"), os.getenv("API_ID"), os.getenv("API_HASH")) as client:
        channels = await get_channels_info(client, channels_txt)
        for channel in channels:
            db.create_channel(channel)

        channels_posts = await get_channels_posts(client, channels_txt, delay=1)


    for channel_posts in channels_posts:
        for post in channel_posts:
            db.create_post(post)


if __name__ == "__main__":
    asyncio.run(main())