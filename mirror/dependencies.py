from fastapi import Header, HTTPException
import os


async def get_token_header(x_token: str = Header()):
    if x_token != os.getenv("X_TOKEN"):
        raise HTTPException(400, detail="X-Token header invalid")

    