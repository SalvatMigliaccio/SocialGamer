from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.auth import get_current_user
from app.schemas import review
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.database import get_db
from app.utils import *
from app.models import user, game

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# CREATE
@router.post("/create", response_model = ReviewCreate)
async def create_review(review_create: ReviewCreate, db: Session = Depends(get_db), 
                        current_user: user.User = Depends(get_current_user)):
    new_review = Review(
        game_id = review_create.game_id,
        user_id = current_user.id,
        comment = review_create.comment,
        user_rating = review_create.rating if review_create.rating else 0,
        created_at = datetime.now().isoformat(),
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# READ ALL by user_id
@router.get("/user/{user_id}", response_model=list[ReviewOut])
async def get_review_by_user(id_user: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.user_id == id_user).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this user")
    return reviews

# READ ALL by game_id
@router.get("/game/{game_id}", response_model=list[ReviewOut])
async def get_review_by_game(id_game: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.game_id == id_game).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this game")
    return reviews

# READ ALL
@router.get("/", response_model=list[ReviewOut])
async def get_all_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

# UPDATE review
@router.put("/{review_id}", response_model=ReviewOut)
async def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    for var, value in vars(review_update).items():
        setattr(review, var, value) if value else None
    db.commit()
    db.refresh(review)
    return review

# DELETE review
@router.delete("/{review_id}")
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}