from fastapi import Header, HTTPException

from .config import config
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


async def get_token_header(x_token: str = Header()):
    if x_token != config["x_token"]:
        raise HTTPException(400, detail="X-Token header invalid")