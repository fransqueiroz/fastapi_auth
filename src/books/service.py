from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from src.books.models import Book_Model
from src.books.schemas import BookCreateModel
from src.database.dependencies import get_db

class BookService:
    def __init__(
        self,
        db: Session = Depends(get_db)):
        self.db = db

    async def get_all_books(self):
        return self.db.query(Book_Model).order_by(desc(Book_Model.created_at)).all()

    async def create_book(self, book_data: BookCreateModel):
        new_book = Book_Model(**book_data.model_dump())
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    async def get_book(self, book_id: str):
        return self.db.query(Book_Model).filter(Book_Model.uid == book_id).first()

    async def update_book(self, book_id: str, book_update_data: BookCreateModel):
        book = self.db.query(Book_Model).filter(Book_Model.uid == book_id).first()
        if not book:
            return None
        book.title = book_update_data.title
        book.author = book_update_data.author
        book.publisher = book_update_data.publisher
        book.published_date = book_update_data.published_date
        book.page_count = book_update_data.page_count
        book.language = book_update_data.language
        self.db.commit()
        self.db.refresh(book)
        return book

    async def delete_book(self, book_id: str):
        book = self.db.query(Book_Model).filter(Book_Model.uid == book_id).first()
        if not book:
            return None
        self.db.delete(book)
        self.db.commit()
        return