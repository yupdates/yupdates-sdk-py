from dataclasses import dataclass
from typing import List  # maintains older Python version compatibility


@dataclass
class AssociatedFile:
    """A file associated with a feed item. See the API documentation for field details."""
    url: str
    length: int
    type_str: str


@dataclass
class FeedItem:
    """One item from a feed. See the API documentation for field details."""
    feed_id: str
    item_id: str
    input_id: str
    title: str
    content: str
    canonical_url: str
    item_time: str
    item_time_ms: int
    deleted: bool
    associated_files: List[AssociatedFile] = None


@dataclass
class InputItem:
    """One item to add to a feed. See the API documentation for field details."""
    title: str
    content: str
    canonical_url: str
    associated_files: List[AssociatedFile] = None
