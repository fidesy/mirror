from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_token_header
from ..services import post
from .. import crud, schemas


router = APIRouter(tags=["media"])

@router.get("/posts/", response_model=list[schemas.Post])
async def get_posts(skip: int = 0, limit: int = 100, like: str = "", db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip, limit, like)
    return posts


@router.post("/post", dependencies=[Depends(get_token_header)])
async def create_post(_post: schemas.PostCreate, db: Session = Depends(get_db)):
    await post.add_post(db, _post)