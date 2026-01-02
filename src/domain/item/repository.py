from abc import ABC
from uuid import UUID

from domain.repositories.abstract import AbstractRepository

from .models import Item, ItemCreateDTO, ItemUpdateDTO


class AbstractItemRepository(
    AbstractRepository[Item, UUID, ItemCreateDTO, ItemUpdateDTO], ABC
):
    """No specific Item logic for now"""
