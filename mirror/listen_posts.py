import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import requests

from .config import config
from .schemas import PostCreate
from .client import client

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

    add_post(PostCreate(
        post_id=message.id,
        channel_id=message.peer_id.channel_id,
        date=message.date,
        message=message.message,
    ))


def add_post(post: PostCreate):
    body = post.json()
    resp = requests.post("https://mirror.fidesy.xyz/api/post/", data=body, headers={
        "Content-Type": "application/json",
        "X-Token": config["x_token"],
    })

    print(resp.status_code, resp.text)


if __name__ == "__main__":
    client.start()    

    loop = asyncio.get_event_loop()
    mirror = loop.run_until_complete(client.get_entity(config["channel_username"]))

    client.run_until_disconnected()