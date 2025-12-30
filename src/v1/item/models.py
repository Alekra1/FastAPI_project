from uuid import UUID

from v1.pydantic.mixins import BaseModel


class Item(BaseModel):
    id: None | UUID = None
    name: str
