from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Query, Response
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse

from v1.pydantic.models import Pagination

from .models import Item

router = APIRouter(prefix="/items")


_db: dict[UUID, Item] = {}


@router.get("", response_model=list[Item])
async def get_items(pagination: Annotated[Pagination, Query()]):
    return Item.paginate(pagination, _db)


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: UUID):
    if item_id in _db:
        return _db[item_id]
    else:
        return JSONResponse({"message": "Item not found!"}, status_code=404)


@router.post("", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.id is None:
        item.id = uuid4()
    if item.id in _db:
        return JSONResponse({"message": "Item already exists"}, status_code=409)
    _db[item.id] = item
    return item


@router.put("/{item_id}", response_model=Item, status_code=200)
async def update_item(item_id: UUID, item: Item, response: Response):
    item.id = item_id
    if item.id not in _db:
        response.status_code = 201
    _db[item.id] = item
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: UUID):
    if item_id not in _db:
        return JSONResponse({"message": "Item not found"}, status_code=404)
    else:
        del _db[item_id]
        return
