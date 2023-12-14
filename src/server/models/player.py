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

from sqlalchemy import Column, Integer, String, Enum, DateTime

from . import Base, Direction


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String)
    health = Column(Integer, default=100)
    inventory = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    direction = Column(Enum(Direction))
    score = Column(Integer, default=0)
    known_map = Column(String)

    @property
    def serialize(self):
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
        super().__init__(**kw)
        self.name = name
        self.health: int = 100
        self.inventory: List[Dict] = []
        self.x: int = 0
        self.y: int = 0
        self.direction: Direction = Direction.NORTH
        self.score: float = 0.0

    def __repr__(self):
        return f"<Player(name='{self.name}', health={self.health}," \
               f"inventory={self.inventory}, x={self.x}, y={self.y}, direction={self.direction})>"

    def __str__(self):
        return f"<Player(name='{self.name}', health={self.health}," \
               f"inventory={self.inventory}, x={self.x}, y={self.y}, direction={self.direction})>"

    def add_score(self, score: float):
        self.score = score
        return self.score

    def sub_score(self, score: float):
        self.score -= score
        return self.score

    def add_health(self, health: int):
        self.health += health
        return self.health

    def sub_health(self, health: int):
        self.health -= health
        return self.health

    def add_item(self, item: Dict):
        self.inventory.append(item)
        return self.inventory

    def remove_item(self, item: Dict):
        self.inventory.remove(item)
        return self.inventory

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
        return self.x, self.y
