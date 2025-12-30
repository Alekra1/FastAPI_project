from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from v1.pydantic.models import Pagination

from .models import Book, BookList, Genre

router = APIRouter(prefix="/books")

_db: dict[UUID, BookList] = {}


@router.get("", response_model=list[BookList])
async def get_paginated_book_list(
    pagination: Annotated[Pagination, Depends()],
    genre: Annotated[Genre | None, Query()] = None,
):
    return BookList.paginate(pagination, _db, genre=genre)


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID):
    if book_id not in _db:
        raise HTTPException(status_code=404, detail="Book not found")
    return _db[book_id]


@router.post("", response_model=BookList, status_code=201)
async def create_book(book: BookList):
    if book.id is None:
        book.id = uuid4()
    if book.id in _db:
        raise HTTPException(status_code=409, detail="Item already exists")
    _db[book.id] = book
    return _db[book.id]


@router.put("", response_model=Book, status_code=200)
async def update_book(book: Book, response: Response):
    if book.id is None:
        book.id = uuid4()
    if book.id not in _db:
        response.status_code = 201
    _db[book.id] = book
    return _db[book.id]


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: UUID):
    if book_id not in _db:
        raise HTTPException(status_code=404, detail="Item not found")
    del _db[book_id]
    return
