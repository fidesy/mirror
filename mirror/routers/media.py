from fastapi import APIRouter, Response, HTTPException


router = APIRouter(tags=["media"])


@router.get("/photos/{photo_id}")
async def get_photo(photo_id: int):
    img = ""
    try:
        with open(f"photos/{photo_id}.png", "rb") as f:
            img = f.read()
    except FileNotFoundError:
        raise HTTPException(404, "not found")

    return Response(img, media_type="image/png")


@router.get("/media/{media_id}")
async def get_media(media_id: int):
    img = ""
    try:
        with open(f"media/{media_id}.png", "rb") as f:
            img = f.read()
    except FileNotFoundError:
        raise HTTPException(404, "not found")

    return Response(img, media_type="image/png")