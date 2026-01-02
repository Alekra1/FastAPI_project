from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class Item:
    id: UUID
    name: str
    description: str


@dataclass(slots=True)
class ItemCreateDTO:
    name: str
    description: str


@dataclass(slots=True)
class ItemUpdateDTO:
    name: Optional[str] = None
    description: Optional[str] = None
