from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
