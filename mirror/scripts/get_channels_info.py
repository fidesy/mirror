import os
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.types import Channel


parent_dir = os.path.join(os.path.dirname(__file__), os.pardir)


async def get_channels_info(client: TelegramClient, usernames: list[str]) -> list[Channel]:
    # create a folder to store photos
    if not os.path.exists(parent_dir + "/data/photos"):
        os.makedirs(parent_dir + "/data/photos")

    channels = []
    for username in usernames:
        channel_info = await get_channel_info(client, username)
        channels.append(channel_info)

    return channels


async def get_channel_info(client: TelegramClient, channel_username: str):
    entity = await client.get_entity(channel_username)
    full_info = await client(GetFullChannelRequest(entity))

    # download profile image
    await client.download_profile_photo(entity, parent_dir + f"data/photos/{entity.id}.png")

    return (entity.id, entity.username, entity.title, full_info.full_chat.about)