from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import UserService
from app.database.database import get_db

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    token = UserService.register_user(user, db)
    return {"token": token}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = UserService.authenticate_user(user, db)
    return {"token": token}
