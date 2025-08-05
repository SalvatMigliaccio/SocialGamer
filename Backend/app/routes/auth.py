from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.utils import auth
from app.schemas.token import Token
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return current_user


