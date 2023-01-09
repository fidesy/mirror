import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.types import PeerChannel

from database import Database

load_dotenv()


client = TelegramClient(os.getenv("TITLE"), os.getenv("API_ID"), os.getenv("API_HASH"))

db = Database(os.getenv("DBURL"))

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

    db.create_post((message.id, message.peer_id.channel_id, message.date, message.message, media_url))


if __name__ == "__main__":
    client.start()    
    client.run_until_disconnected()