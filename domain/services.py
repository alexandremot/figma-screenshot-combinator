from abc import ABC, abstractmethod
from typing import List
from .entities import Item
from .ports import ItemRepository

class ItemService(ABC):
    @abstractmethod
    def get_item(self, item_id: str) -> Item:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        pass

    @abstractmethod
    def create_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def update_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def delete_item(self, item_id: str) -> None:
        pass

class ItemServiceImpl(ItemService):
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def get_item(self, item_id: str) -> Item:
        item = self.item_repository.find_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        return item

    def get_all_items(self) -> List[Item]:
        return self.item_repository.find_all()

    def create_item(self, item: Item) -> Item:
        return self.item_repository.add(item)

    def update_item(self, item: Item) -> Item:
        return self.item_repository.update(item)

    def delete_item(self, item_id: str) -> None:
        self.item_repository.delete(item_id)
