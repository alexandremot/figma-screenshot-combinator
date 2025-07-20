import os
from domain.ports import FileStoragePort

class LocalFileStorage(FileStoragePort):
    def __init__(self, base_dir: str = "uploads"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save(self, filename: str, data: bytes) -> str:
        path = os.path.join(self.base_dir, filename)
        with open(path, "wb") as f:
            f.write(data)
        return path
