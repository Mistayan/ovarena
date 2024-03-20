from abc import ABC, abstractmethod
from typing import List, Dict

from src.shared.direction import Direction


class IPlayer(ABC):
    """
    Player's interface
    """
    name: str
    health: int
    inventory: List[Dict]
    x: int
    y: int
    direction: Direction
    score: float
    known_map: List[List[int]]

    @abstractmethod
    def __init__(self, **kw: Dict):
        """
        connect Player to the arena
        """
        pass

    @abstractmethod
    def move(self, direction: Direction, distance: int = 1):
        """
        Move the player in the given direction
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        string representation of the object
        """
        pass