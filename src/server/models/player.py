"""
Player's instance in the maze
keep records of:
    positions (x, y) 
    direction (N, E, S, W)
    health
    inventory

on each updates (time-based)
"""""
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy import Column, Integer, String, DateTime

from src.shared.direction import Direction
from src.shared.player import IPlayer


class Player(IPlayer):
    """
    Player's instance in the arena
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String)
    health = Column(Integer, default=100)
    inventory = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    direction = Column(Direction)
    score = Column(Integer, default=0)
    known_map = Column(String)

    @property
    def serialize(self):
        """
        Return object data in easily serializable format
        """
        return {
            'name': self.name,
            'health': self.health,
            'inventory': self.inventory,
            'x': self.x,
            'y': self.y,
            'direction': self.direction,
            'score': self.score
        }

    def __init__(self, name: str, **kw: Any):
        """
        create Player's instance in the arena
        """
        super().__init__(**kw)
        self.name = name
        self.health: int = 100
        self.inventory: List[Dict] = []
        self.x: int = 0
        self.y: int = 0
        self.direction: Direction = Direction.NORTH
        self.score: float = 0.0

    def __repr__(self):
        """ string representation of the object"""
        return f"<Player(name='{self.name}', health={self.health}," \
               f"inventory={self.inventory}, x={self.x}, y={self.y}, direction={self.direction})>"

    def __str__(self):
        """ string representation of the object"""
        return self.__repr__()

    def add_score(self, score: float):
        """
        Add score to the player
        """
        self.score = score
        return self.score

    def sub_score(self, score: float):
        """
        Substract score to the player
        """
        self.score -= score
        return self.score

    def add_health(self, health: int):
        """
        Add health to the player
        """
        self.health += health
        return self.health

    def sub_health(self, health: int):
        """
        Substract health to the player
        """
        self.health -= health
        return self.health

    def add_item(self, item: Dict):
        """
        Add an item to the player's inventory
        """
        self.inventory.append(item)
        return self.inventory

    def remove_item(self, item: Dict):
        """
        Remove an item from the player's inventory, drop it on the ground
        """
        self.inventory.remove(item)
        return self.inventory

    def move(self, direction: Direction, distance: int = 1):
        """
        Move the player in the given direction
        """
        if direction == Direction.NORTH:
            self.y += distance
        elif direction == Direction.EAST:
            self.x += distance
        elif direction == Direction.SOUTH:
            self.y -= distance
        elif direction == Direction.WEST:
            self.x -= distance
        return self.x, self.y
