from fastapi import APIRouter

from . import channel, post, media


router = APIRouter(prefix="/api")

router.include_router(channel.router)
router.include_router(post.router)
router.include_router(media.router)