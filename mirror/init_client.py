import os
from dotenv import load_dotenv
from telethon import TelegramClient


load_dotenv()


def main():
    client = TelegramClient(os.getenv("TITLE"), os.getenv("API_ID"), os.getenv("API_HASH"))
    client.start()    


if __name__ == "__main__":
    main()