from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .entities import ComparisonResult
from .entities import Item

class ItemRepository(ABC):
    @abstractmethod
    def find_by_id(self, item_id: str) -> Item:
        pass

    @abstractmethod
    def find_all(self) -> List[Item]:
        pass

    @abstractmethod
    def add(self, item: Item) -> Item:
        pass

    @abstractmethod
    def update(self, item: Item) -> Item:
        pass

    @abstractmethod
    def delete(self, item_id: str) -> None:
        pass

class FileStoragePort(ABC):
    @abstractmethod
    def save(self, filename: str, data: bytes) -> str:
        pass

class ImageComparisonPort(ABC):
    @abstractmethod
    def compare_images(self, figma_dir: Path, screenshots_dir: Path) -> ComparisonResult:
        pass