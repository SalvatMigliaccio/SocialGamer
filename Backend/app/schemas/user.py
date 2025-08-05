from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john_doe@example.com")
    bio: Optional[str] = Field(None, example="Avid gamer and tech enthusiast.")
    age: Optional[int] = Field(None, ge=0)
    avatar_url: Optional[str] = Field(None, example="http://example.com/avatar.jpg")
    is_active: bool = Field(default=True, example=True)
    name: Optional[str] = Field(..., example="John")
    surname: Optional[str] = Field(..., example="Doe")

class UserCreate(UserBase):
        password: str = Field(..., min_length=8, example="securepassword123")
        confirm_password: str = Field(..., min_length=8, example="securepassword123")
        
class UserOut(UserBase):
    id: int
    
    class Config:
        orm_mode = True
