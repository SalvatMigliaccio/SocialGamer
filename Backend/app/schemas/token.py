from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")
    
class TokenData(BaseModel):
    username: str = Field(..., example="john_doe")
    
    