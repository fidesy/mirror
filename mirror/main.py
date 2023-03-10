from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from .dependencies import get_token_header
from .service import Service


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mirror.fidesy.xyz"]
)

service = Service(os.getenv("DB_URL"), os.getenv("TITLE"), os.getenv("API_ID"), os.getenv("API_HASH"))


@app.get("/api/posts")
def get_posts(skip: int = 0, limit: int = 100, like: str = ""):
    return service.get_posts(skip, limit, like)


@app.get("/api/photos/{photo_id}")
def get_photo(photo_id: int):
    img = ""
    with open(f"mirror/data/photos/{photo_id}.png", "rb") as f:
        img = f.read()

    return Response(img, media_type="image/png")


@app.get("/api/channels")
def get_channels(skip: int = 0, limit: int = 100):
    return service.get_channels(skip, limit)


@app.post("/api/channel", dependencies=[Depends(get_token_header)])
async def create_channel(username: str):
    await service.add_channel(username)
    return 200


@app.delete("/api/channel", dependencies=[Depends(get_token_header)])
async def delete_channel(username: str):
    try:
        await service.delete_channel(username)
        return 200
    except Exception as e:
        raise HTTPException(500, detail=e)