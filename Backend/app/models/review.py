from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    
    
    user = relationship("User", back_populates="reviews")