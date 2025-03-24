from fastapi import APIRouter, HTTPException, status

from src.auth.models import User_Model
from src.auth.schema import UserCreateModel
from src.auth.service import UserService
from src.database.dependencies import get_db


auth_router = APIRouter()
user_service = UserService(db=next(get_db()))

@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel
):
    email = user_data.email

    user_exists = await user_service.user_exists(email)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data)

    return new_user