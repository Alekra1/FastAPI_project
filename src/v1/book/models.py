from enum import Enum
from uuid import UUID

from v1.pydantic.mixins import BaseModel


class Genre(Enum):
    Horror = "horror"
    Science_Fiction = "sci-fi"
    Fantasy = "fantasy"


class BookList(BaseModel):
    id: UUID | None = None
    title: str
    genre: Genre

    @staticmethod
    def filter(_list, **kwargs):
        genre = kwargs.pop("genre", None)

        if not genre:
            return _list

        filtered_list = []

        for book in _list:
            if book.genre == genre:
                filtered_list.append(book)

        return filtered_list


class Book(BookList):
    author: str
    year: int
    rating: float
