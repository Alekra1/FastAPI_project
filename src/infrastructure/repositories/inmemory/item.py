from typing import Dict, List, Optional
from uuid import UUID, uuid4

from domain.item.exceptions import ItemNotFoundError
from domain.item.models import Item, ItemCreateDTO, ItemUpdateDTO
from domain.item.repository import AbstractItemRepository


class InMemoryItemRepository(AbstractItemRepository):
    def __init__(self, storage: Optional[Dict[UUID, Item]] = None) -> None:
        if storage is not None:
            self._storage = storage.copy()
        else:
            self._storage = {}

    def get(self, entity_id: UUID) -> Item:
        try:
            return self._storage[entity_id]
        except KeyError:
            raise ItemNotFoundError(entity_id)

    def list(self, *, limit: int = 100, offset: int = 0) -> List[Item]:
        items = list(self._storage.values())
        return items[offset : offset + limit]

    def create(self, dto: ItemCreateDTO) -> Item:
        _id = uuid4()

        item = Item(id=_id, name=dto.name, description=dto.description)

        self._storage[_id] = item

        return item

    def update(self, entity_id: UUID, dto: ItemUpdateDTO) -> Item:
        if entity_id not in self._storage:
            raise ItemNotFoundError(entity_id)

        existing_item = self._storage[entity_id]

        updated_item = Item(
            id=existing_item.id,
            name=dto.name if dto.name is not None else existing_item.name,
            description=dto.description
            if dto.description is not None
            else existing_item.description,
        )

        self._storage[entity_id] = updated_item
        return updated_item

    def delete(self, entity_id: UUID) -> None:
        if entity_id not in self._storage:
            raise ItemNotFoundError(entity_id)

        del self._storage[entity_id]
