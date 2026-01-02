from uuid import UUID


class ItemNotFoundError(Exception):
    def __init__(self, item_id: UUID) -> None:
        super().__init__(f"Item with id={item_id} not found!")
        self.item_id = item_id
