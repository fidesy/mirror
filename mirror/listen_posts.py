import asyncio
from telethon import TelegramClient, events
from telethon.types import PeerChannel, MessageMediaPhoto

from .config import config
from .dependencies import get_db
from .crud import add_post, add_media
from .schemas import PostCreate, MediaCreate


client = TelegramClient(config["title"], config["api_id"], config["api_hash"])

mirror = None 


# New message handler
@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    
    # Check if the message is from a channel or from a chat
    if type(event.peer_id) != PeerChannel or not event.post:
        return

    try:
        await client.forward_messages(mirror, event.message)
    except Exception as e:
        print(e)

    db = get_db()
    add_post(db, PostCreate(
        post_id=message.id,
        channel_id=message.peer_id.channel_id,
        date=message.date,
        message=message.message,
    ))

    if message.media and isinstance(message.media, MessageMediaPhoto):
        add_media(db, MediaCreate(
            channel_id=message.peer_id.channel_id,
            post_id=message.id,
            photo_id=message.media.photo.id
        ))


if __name__ == "__main__":
    client.start()    

    loop = asyncio.get_event_loop()
    mirror = loop.run_until_complete(client.get_entity(config["channel_username"]))

    client.run_until_disconnected()