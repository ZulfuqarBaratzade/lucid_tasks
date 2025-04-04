from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
