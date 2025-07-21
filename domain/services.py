from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .entities import Item
from .entities import ImagePair, ComparisonResult
from .ports import ItemRepository
from domain.ports import FileStoragePort
from domain.ports import ImageComparisonPort


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


class FileService:
    def __init__(self, storage: FileStoragePort):
        self.storage = storage

    def save_zip(self, filename: str, data: bytes) -> str:
        if not filename.endswith('.zip'):
            raise ValueError("Arquivo deve ser .zip")
        return self.storage.save(filename, data)
    
class ImageComparisonService:
    def __init__(self, comparison_port: ImageComparisonPort = None):
        self.comparison_port = comparison_port        
    def compare_images(self, figma_dir: Path = None, screenshots_dir: Path = None) -> ComparisonResult:
        """Compara imagens usando o adaptador fornecido."""
        return self.comparison_port.compare_images(figma_dir, screenshots_dir)
