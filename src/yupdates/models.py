from dataclasses import dataclass


@dataclass
class InputItem:
    """One item to add to a feed. See the API documentation for field details."""
    title: str
    content: str
    canonical_url: str
