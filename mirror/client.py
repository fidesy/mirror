from telethon import TelegramClient

from .config import config


client = TelegramClient(config["title"], config["api_id"], config["api_hash"])


