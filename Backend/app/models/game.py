# app/models/game.py

from sqlalchemy import Column, Integer, String
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    rawg_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    release_year = Column(Integer, nullable=True)
    cover_url = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    metacritic_score = Column(Integer, nullable=True)
