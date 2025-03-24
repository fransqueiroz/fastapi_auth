from datetime import datetime, timedelta, timezone
import datetime
import logging
import uuid
import jwt
from passlib.context import CryptContext

from src.config.constants import JWT_ALGORITHM, JWT_SECRET

passwd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    expiry_time = datetime.datetime.utcnow() + (expiry if expiry is not None else timedelta(minutes=60))

    payload = {
        'user': user_data,
        'exp': expiry_time.replace(tzinfo=timezone.utc),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
