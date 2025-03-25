import datetime
import uuid
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.auth.schema import UserResponseModel
from src.database.database import Base

class Book_Model(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(String, nullable=False, default=lambda: str(uuid.uuid4()), index=True, unique=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    publisher: Mapped[str] = mapped_column(String, nullable=False)
    published_date: Mapped[str] = mapped_column(String, nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    user_uid: Mapped[str | None] = mapped_column(String, ForeignKey("user_accounts.uid"), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False)
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    user: Mapped["UserResponseModel"] = relationship("User_Model", back_populates="books")