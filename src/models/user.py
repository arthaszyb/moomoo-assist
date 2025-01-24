from dataclasses import dataclass
from typing import List

@dataclass
class User:
    """
    Represents a user of the MooMoo Investment Assistant Tool.
    """
    user_id: str
    api_key: str
    preferences: dict
    portfolio: List[str] 