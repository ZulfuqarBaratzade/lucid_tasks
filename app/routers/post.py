from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.post import PostCreate, PostResponse
from app.models.post import Post
from app.utils.utils import verify_token
from app.database.database import get_db
from cachetools import TTLCache
from fastapi.security import OAuth2PasswordBearer
from typing import List
router = APIRouter()
cache = TTLCache(maxsize=100, ttl=300)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router.post("/addpost")
def add_post(post: PostCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    if len(post.text.encode("utf-8")) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload exceeds 1MB")
    new_post = Post(text=post.text, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"postID": new_post.id}

@router.get("/getposts", response_model=List[PostResponse])
def get_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    if user.id in cache:
        return cache[user.id]
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    cache[user.id] = posts
    return posts

@router.delete("/deletepost/{post_id}")
def delete_post(post_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
