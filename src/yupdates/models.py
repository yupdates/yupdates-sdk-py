from dataclasses import dataclass


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


@dataclass
class InputItem:
    """One item to add to a feed. See the API documentation for field details."""
    title: str
    content: str
    canonical_url: str
