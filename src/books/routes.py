from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.books.books_data import books
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.books.service import BookService
from src.database.dependencies import get_db

book_router = APIRouter()
book_service = BookService(db=next(get_db()))
acccess_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    token_details=Depends(acccess_token_bearer)
):
    print(token_details)
    books = await book_service.get_all_books()
    return books

@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[role_checker])
async def get_user_book_submissions(
    user_uid:str,
    token_details: dict = Depends(acccess_token_bearer),
):
    books = await book_service.get_user_books(user_uid)
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker]
)
async def create_a_book(
    book_data: BookCreateModel,
    token_details=Depends(acccess_token_bearer),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_id)
    return new_book



@book_router.get("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    token_details=Depends(acccess_token_bearer),
) -> dict:
    book = await book_service.get_book(book_uid)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    token_details=Depends(acccess_token_bearer),
) -> dict:

    updated_book = await book_service.update_book(book_uid, book_update_data)

    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    else:
        return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
    book_uid: str,
    token_details=Depends(acccess_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:

        return {}