from fastapi import Depends
from sqlalchemy.orm import Session
from src.auth.models import User_Model
from src.auth.schema import UserCreateModel, UserResponseModel
from src.auth.utils import generate_password_hash
from src.database.dependencies import get_db
class UserService:
    def __init__(
        self,
        db: Session = Depends(get_db)):
        self.db = db

    async def get_user_by_email(self, email: str):
        return self.db.query(User_Model).filter(User_Model.email == email).first()

    async def user_exists(self, email: str):
        user = await self.get_user_by_email(email)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel):
        password_hash = generate_password_hash(user_data.password)
        new_user = User_Model(**user_data.model_dump(exclude={"password"}), password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return UserResponseModel(**new_user.__dict__)