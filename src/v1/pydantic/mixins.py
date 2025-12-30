from typing import Any
from uuid import UUID

from pydantic import BaseModel as _BaseModel

from .models import Pagination


class BaseModel(_BaseModel):
    @classmethod
    def paginate(
        cls, pagination: Pagination, db: dict[UUID, Any], **kwargs
    ) -> list["BaseModel"]:
        length = len(db)

        if pagination.offset >= length:
            return []

        _list = list(db.values())
        _list = cls.filter(_list, **kwargs)

        paginated_list: list[BaseModel] = _list[
            pagination.offset : pagination.offset + pagination.limit
        ]

        return paginated_list

    @staticmethod
    def filter(_list, **kwargs):
        return _list
