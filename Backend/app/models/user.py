from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import Optional
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    age = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    
    reviews = relationship("Review", back_populates="user")

