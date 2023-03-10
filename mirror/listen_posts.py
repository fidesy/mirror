import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.types import PeerChannel

from database import Database

load_dotenv()


client = TelegramClient(os.getenv("TITLE"), os.getenv("API_ID"), os.getenv("API_HASH"))

mirror = None 

db = Database(os.getenv("DB_URL"))

# New message handler
@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    
    # Check if the message is from a channel or from a chat
    if type(event.peer_id) != PeerChannel or not event.post:
        return

    media_url = ""
    try:
        media_url = message.media.webpage.url
    except AttributeError:
        ...

    try:
        await client.forward_messages(mirror, event.message)
    except Exception as e:
        print(e)

    db.add_channel((message.id, message.peer_id.channel_id, message.date, message.message, media_url))


if __name__ == "__main__":
    client.start()    
    loop = asyncio.get_event_loop()
    mirror = loop.run_until_complete(client.get_entity(os.getenv("CHANNEL_USERNAME")))

    client.run_until_disconnected()