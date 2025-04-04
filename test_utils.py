import pytest
from sqlalchemy.orm import Session
from app.utils import hash_password, verify_password, create_token, verify_token
from app.models.user import User
from app.database.database import SessionLocal


test_email = "test@example.com"
test_password = "secure_password_123"


def test_hash_and_verify_password():
    hashed = hash_password(test_password)
    assert hashed != test_password, "Hash şifreyle aynı olmamalı"
    assert verify_password(test_password, hashed) is True
    assert verify_password("wrong_password", hashed) is False
def test_create_and_verify_token():
    token = create_token({"sub": test_email})
    assert isinstance(token, str)
    

    db: Session = SessionLocal()


    user = db.query(User).filter(User.email == test_email).first()
    if not user:
        user = User(email=test_email, hashed_password=hash_password(test_password))
        db.add(user)
        db.commit()
        db.refresh(user)

    verified_user = verify_token(token, db)
    assert verified_user.email == test_email
