import datetime
from typing import List
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.books.schemas import Book
from src.database.database import Base
import uuid


class User_Model(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String, nullable=False, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=True, default="user")
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    books: Mapped[List["Book"]] = relationship("Book_Model", back_populates="user")