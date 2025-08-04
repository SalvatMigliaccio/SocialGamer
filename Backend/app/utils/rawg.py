# app/utils/rawg.py

import os
import requests
from typing import Optional


RAWG_API_KEY = os.getenv("RAWG_API_KEY")
BASE_URL = "https://api.rawg.io/api/games"

def fetch_game_by_slug(slug: str) -> Optional[dict]:
    """
    Fetch detailed game data from RAWG using the slug
    """
    url = f"{BASE_URL}/{slug}"
    params = {
        "key": RAWG_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

def search_games(query: str, page_size: int = 5) -> list[dict]:
    """
    Search games by name
    """
    params = {
        "key": RAWG_API_KEY,
        "search": query,
        "page_size": page_size
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get("results", [])
