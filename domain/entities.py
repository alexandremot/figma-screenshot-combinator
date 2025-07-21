from dataclasses import dataclass
from typing import Optional
from typing import List


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

@dataclass
class ImagePair:
    figma_path: str
    screenshot_path: str
    similarity_score: float

@dataclass
class ComparisonResult:
    pairs: List[ImagePair]
    total_comparisons: int
