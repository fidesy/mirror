from telethon import TelegramClient

from .config import config


def main():
    client = TelegramClient(config["title"], config["api_id"], config["api_hash"])
    client.start()    


if __name__ == "__main__":
    main()