# app/routes/games.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate, GameOut
from app.database import get_db
from app.utils.rawg import *


router = APIRouter(prefix="/games", tags=["Games"])

# CREATE
@router.post("/", response_model=GameOut)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.rawg_id == game.rawg_id).first()
    if db_game:
        raise HTTPException(status_code=400, detail="Game already exists")

    new_game = Game(**game.dict())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

# READ ALL
@router.get("/", response_model=list[GameOut])
def get_all_games(db: Session = Depends(get_db)):
    return db.query(Game).all()

# READ BY ID
@router.get("/{game_id}", response_model=GameOut)
def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

# UPDATE
@router.put("/{game_id}", response_model=GameOut)
def update_game(game_id: int, game_update: GameUpdate, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    for key, value in game_update.dict(exclude_unset=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game

# DELETE
@router.delete("/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(game)
    db.commit()
    return {"detail": "Game deleted"}

# RAWG SEARCH
@router.post("/import/", response_model=GameOut)
def import_game_from_rawg(name: str, db: Session = Depends(get_db)):
    """
    Cerca un gioco da RAWG e lo importa nel database
    """
    results = search_games(name)
    if not results:
        raise HTTPException(status_code=404, detail="Nessun gioco trovato")

    rawg_game = results[0]  # prendiamo il primo risultato
    slug = rawg_game["slug"]

    detailed = fetch_game_by_slug(slug)
    if not detailed:
        raise HTTPException(status_code=400, detail="Errore nel recupero dati RAWG")

    # Controllo duplicati
    existing = db.query(Game).filter(Game.rawg_id == detailed["id"]).first()
    if existing:
        return existing

    new_game = Game(
        rawg_id=detailed["id"],
        name=detailed["name"],
        release_year=int(detailed["released"].split("-")[0]) if detailed.get("released") else None,
        cover_url=detailed["background_image"],
        summary=detailed.get("description_raw"),
        genre=", ".join([genre["name"] for genre in detailed.get("genres", [])]),
        platform=", ".join([p["platform"]["name"] for p in detailed.get("platforms", [])]),
        metacritic_score=detailed.get("metacritic")
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game