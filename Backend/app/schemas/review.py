# Review schemas

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    game_id: int = Field(..., description="ID of the game being reviewed")
    user_id: int = Field(..., description="ID of the user who wrote the review")
    comment: str = Field(..., description="Content of the review")
    user_rating: Optional[int] = Field(None, description="Rating given by the user, from 1 to 10")
   
    
class ReviewCreate(ReviewBase):
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the review was created")
    
class ReviewUpdate(ReviewBase):
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the review was last updated")
    
class ReviewOut(ReviewBase):
    id: int = Field(..., description="Unique ID of the review")
    created_at: datetime = Field(..., description="Timestamp when the review was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the review was last updated")
    
    class Config:
        orm_mode = True