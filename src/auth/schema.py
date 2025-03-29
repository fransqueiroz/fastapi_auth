import datetime
from typing import List
from pydantic import BaseModel, Field

from src.books.schemas import Book


class UserCreateModel(BaseModel):
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }

class UserResponseModel(BaseModel):
    uid: str
    first_name: str
    last_name: str
    username: str
    email: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)

class UserBooksModel(UserResponseModel):
    books: List[Book]