import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from src.database.database import Base
import uuid


class User_Model(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(
        String,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
        unique=True,
    )
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=True, default="user")
    is_verified = Column(Boolean, default=False, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    update_at = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
        onupdate=datetime.datetime.now,
    )