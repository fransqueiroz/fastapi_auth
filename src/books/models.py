import datetime
import uuid
from sqlalchemy import Column, DateTime, Integer, String

from src.database.database import Base

class Book_Model(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(
        String,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
        unique=True,
    )
    title=  Column(String, nullable=False)
    author=  Column(String, nullable=False)
    publisher=  Column(String, nullable=False)
    published_date=  Column(String, nullable=False)
    page_count= Column(Integer, nullable=False)
    language= Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    update_at = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
        onupdate=datetime.datetime.now,
    )