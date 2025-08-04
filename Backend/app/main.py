# app/main.py

from fastapi import FastAPI
from app.routes import games
from app.database import Base, engine

# Crea le tabelle al primo avvio (solo se non esistono già)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SocialGamer API")

# Includi le route dei giochi
app.include_router(games.router)
