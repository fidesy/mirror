from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import Database

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mirror.fidesy.xyz"]
)

db = Database(os.getenv("DBURL"))


@app.get("/api/posts")
def get_posts(skip: int = 0, limit: int = 100, like: str = ""):
    return db.get_posts(skip, limit, like)


@app.get("/api/photos/{photo_id}")
def get_photo(photo_id: int):
    img = ""
    with open(f"mirror/data/photos/{photo_id}.png", "rb") as f:
        img = f.read()

    return Response(img, media_type="image/png")