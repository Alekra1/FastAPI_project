from typing import Annotated, List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import JSONResponse, Response

from domain.item.exceptions import ItemNotFoundError
from domain.item.models import Item, ItemCreateDTO, ItemUpdateDTO
from domain.item.repository import AbstractItemRepository
from infrastructure.repositories.inmemory.item import InMemoryItemRepository
from v1.item.models import (
    ItemCreateSchema,
    ItemListSchema,
    ItemSchema,
    ItemUpdateSchema,
)
from v1.pydantic.models import Pagination

router = APIRouter(prefix="/items")

_item_repo = InMemoryItemRepository()


def get_item_repo():
    return _item_repo


@router.post("", response_model=Item)
def create_item(
    payload: ItemCreateSchema, repo: AbstractItemRepository = Depends(get_item_repo)
):
    dto = ItemCreateDTO(name=payload.name, description=payload.description)
    item = repo.create(dto)

    # item_schema = ItemSchema(
    #     id=item.id,
    #     name=item.name,
    #     description=item.description,
    # )

    return item


@router.get("", response_model=List[Item])
def list_items(
    pagination: Pagination = Depends(),
    repo: AbstractItemRepository = Depends(get_item_repo),
):
    items = repo.list(limit=pagination.limit, offset=pagination.offset)

    return items


@router.patch("/{item_id}")
def update_item(
    item_id: UUID,
    payload: ItemUpdateSchema,
    repo: AbstractItemRepository = Depends(get_item_repo),
):
    dto = ItemUpdateDTO(name=payload.name, description=payload.description)

    try:
        item = repo.update(item_id, dto)
    except ItemNotFoundError as exc:
        print(exc)
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: UUID, repo: AbstractItemRepository = Depends(get_item_repo)):
    try:
        repo.delete(item_id)
    except ItemNotFoundError as exc:
        print(exc)
        raise HTTPException(status_code=404, detail="Item not found")
    return
