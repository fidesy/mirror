import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from utils import load_txt


load_dotenv()


async def join_channels(client: TelegramClient, resources: list[str], delay: int = 5) -> None:
    for resource in resources:
        entity = await client.get_entity(resource)
        await client(JoinChannelRequest(entity))
        await asyncio.sleep(delay)


async def main():
    async with TelegramClient(os.getenv("TITLE"), os.getenv("API_ID"), os.getenv("API_HASH")) as client:
        channels = load_txt("mirror/data/channels.txt")
        await join_channels(client, channels)


if __name__ == "__main__":
    asyncio.run(main())