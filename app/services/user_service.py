from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.utils import hash_password, verify_password, create_token

class UserService:

    @staticmethod
    def register_user(user_data: UserCreate, db: Session) -> str:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed = hash_password(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return create_token({"sub": new_user.email})

    @staticmethod
    def authenticate_user(user_data: UserLogin, db: Session) -> str:
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if not db_user or not verify_password(user_data.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return create_token({"sub": db_user.email})
