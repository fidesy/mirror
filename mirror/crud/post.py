from sqlalchemy import func
from sqlalchemy.orm import Session

from ..schemas.post import PostCreate
from ..models.post import Post


def add_post(db: Session, post: PostCreate) -> Post:
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 100, like: str = "") -> list[Post]:
    posts = db.query(Post).filter(func.lower(Post.message).like(f"%{like.lower()}%")).order_by(Post.date.desc()).offset(skip).limit(limit).all()
    return posts


def delete_post(db: Session, id: int) -> int:
    status = db.query(Post).filter(Post.id == id).delete()
    db.commit()
    return status

