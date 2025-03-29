from fastapi import Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlmodel import select
from src.database.models import Book_Model, User_Model
from src.auth.schema import UserCreateModel, UserResponseModel
from src.auth.utils import generate_password_hash
from src.database.dependencies import get_db
class UserService:
    def __init__(
        self,
        db: Session = Depends(get_db)):
        self.db = db

    async def get_user_by_email(self, email: str):
        user = self.db.execute(select(User_Model).filter(User_Model.email == email))
        user = user.scalars().first()

        return user

    async def get_user_by_uid(self, uid: str):
        user = self.db.execute(select(User_Model).filter(User_Model.uid == uid))
        user = user.scalars().first()

        return user

    async def user_exists(self, email: str):
        user = await self.get_user_by_email(email)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel):
        password_hash = generate_password_hash(user_data.password)
        new_user = User_Model(**user_data.model_dump(exclude={"password"}), password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        print(f"new_user após refresh: {new_user.__dict__}")
        return UserResponseModel(
            uid=new_user.uid,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            username=new_user.username,
            email=new_user.email,
            is_verified=new_user.is_verified,
            password_hash=new_user.password_hash,
            created_at=new_user.created_at,
            update_at=new_user.update_at,
        )