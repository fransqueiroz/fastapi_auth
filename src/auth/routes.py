from datetime import timedelta
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker, get_current_user
from src.auth.models import User_Model
from src.auth.schema import UserBooksModel, UserCreateModel, UserLoginModel
from src.auth.service import UserService
from src.auth.utils import create_access_token, verify_password
from src.database.dependencies import get_db
from src.database.redis import add_jti_to_blocklist


auth_router = APIRouter()
user_service = UserService(db=next(get_db()))
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY=2

@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )

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

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user