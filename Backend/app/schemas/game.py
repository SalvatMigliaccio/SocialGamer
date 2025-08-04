# app/schemas/game.py

from pydantic import BaseModel, Field
from typing import Optional


# ✅ Base comune per tutti gli schemi
class GameBase(BaseModel):
    name: str = Field(..., description="Name of the game")
    release_year: Optional[int] = Field(None, description="Year the game was released")
    cover_url: Optional[str] = Field(None, description="URL of the game's cover image")
    summary: Optional[str] = Field(None, description="Brief summary of the game")
    genre: Optional[str] = Field(None, description="Genre of the game")
    platform: Optional[str] = Field(None, description="Platform(s) the game is available on")
    metacritic_score: Optional[int] = Field(None, description="Metacritic score of the game")

    class Config:
        orm_mode = True


# ✅ Per creare un nuovo gioco (POST)
class GameCreate(GameBase):
    rawg_id: int = Field(..., description="Unique identifier from RAWG API")


# ✅ Per aggiornare un gioco (PUT/PATCH)
class GameUpdate(GameBase):
    rawg_id: Optional[int] = Field(None, description="RAWG ID if updated")


# ✅ Per restituire un gioco nelle API (GET)
class GameOut(GameBase):
    id: int = Field(..., description="Unique ID from database")
