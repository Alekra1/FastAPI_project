from uuid import UUID

from pydantic import BaseModel, Field


class ItemListSchema(BaseModel):
    id: UUID | None = None
    name: str = "Item Name"


class ItemSchema(ItemListSchema):
    description: str = "Item Description"


class ItemCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    description: str = Field(min_length=1)


class ItemUpdateSchema(ItemCreateSchema): ...
