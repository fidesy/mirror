from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_token_header
from ..services import channel


router = APIRouter(tags=["channel"])


@router.post("/channel", dependencies=[Depends(get_token_header)])
async def create_channel(username: str, db: Session = Depends(get_db)):
    await channel.add_channel(db, username)


@router.delete("/channel", dependencies=[Depends(get_token_header)])
async def delete_channel(username: str, db: Session = Depends(get_db)):
    await channel.delete_channel(db, username)