from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from cachetools import TTLCache
import uvicorn
from app.schemas.user import UserCreate, UserLogin
from app.schemas.post import PostCreate, PostResponse
from app.models.user import User
from app.models.post import Post
from app.utils.utils import hash_password, verify_password, create_token, verify_token
from app.database.database import Base, engine, SessionLocal
from app.services import user_service


Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

cache = TTLCache(maxsize=100, ttl=300)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    token = user_service.register_user(user, db)
    return {"token": token}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = user_service.authenticate_user(user, db)
    return {"token": token}

@app.post("/addpost")
def add_post(post: PostCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    if len(post.text.encode("utf-8")) > 1024 * 1024: 
        raise HTTPException(status_code=400, detail="Payload exceeds 1MB")
    new_post = Post(text=post.text, owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"postID": new_post.id}

@app.get("/getposts", response_model=List[PostResponse])
def get_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)  
    if user.id in cache: 
        return cache[user.id]
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    cache[user.id] = posts  
    return posts

@app.delete("/deletepost/{post_id}")
def delete_post(post_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(token, db)
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
