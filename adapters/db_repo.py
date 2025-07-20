from domain.entities import Item
from domain.ports import ItemRepository

class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self.items = {}

    def find_by_id(self, item_id: str) -> Item:
        return self.items.get(item_id)

    def find_all(self) -> list:
        return list(self.items.values())

    def add(self, item: Item) -> Item:
        self.items[item.id] = item
        return item

    def update(self, item: Item) -> Item:
        self.items[item.id] = item
        return item

    def delete(self, item_id: str) -> None:
        if item_id in self.items:
            del self.items[item_id]
