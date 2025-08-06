# app/main.py

from fastapi import FastAPI
from app.routes import games, user, auth, review
from app.database import Base, engine

# Crea le tabelle al primo avvio (solo se non esistono già)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SocialGamer API")
app.include_router(games.router, tags=["Games"])
app.include_router(user.router, tags=["Users"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(review.router, tags=["Reviews"])