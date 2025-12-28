from uuid import UUID, uuid4

from fastapi import HTTPException, Response
from fastapi.routing import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

router = APIRouter(prefix="/items")


class Item(BaseModel):
    id: None | UUID = None
    name: str


_db: dict[UUID, Item] = {}


@router.get("", response_model=list[Item])
async def get_items(limit: int = 1, offset: int = 0):
    items = list(_db.values())
    if limit < 0 or limit + offset > len(items):
        raise HTTPException(status_code=400, detail="Requested limit is out of range")
    return items[offset : offset + limit]


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
