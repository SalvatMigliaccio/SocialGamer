from fastapi import APIRouter, Depends, HTTPException
from requests import get
from sqlalchemy.orm import Session
from app.utils import auth
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.models.user import User
from app.models.review import Review
from app.models import user 
from app.schemas import *
from app.utils import *

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/create", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #chek if the user alrealdy exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = auth.hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        surname=user.surname,
        age=user.age,
        is_active=user.is_active,
        avatar_url=user.avatar_url,
        bio=user.bio
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/get_all_users", response_model=list[UserOut])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

