from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str


_db: dict[int, Item] = {}


@app.get("/items", response_model=list[Item])
async def get_items():
    return list(_db.values())

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id in _db:
        return _db[item_id]
    else:
        raise HTTPException(status_code=404, detail="item not found")

@app.post("/items/{item_id}", status_code=status.HTTP_201_CREATED, response_model=Item)
async def create_item(item_id: int, item: Item):
    if item_id not in _db:
        _db.update({item_id : item})
        return item
    else:
        raise HTTPException(status_code=409, detail="item with this id already exists")

@app.put("/items", response_model=Item, status_code=200)
async def update_item(item: Item, response: Response):
    if item.id not in _db:
        response.status_code = status.HTTP_201_CREATED

    _db[item.id] = item
    
    return _db[item.id]

