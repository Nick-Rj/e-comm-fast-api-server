from pydantic import BaseModel
from typing import List

# --- Review Schemas ---
class ReviewBase(BaseModel):
    text: str
    ratings: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    reviews: List[Review] = []

    class Config:
        from_attributes = True
        