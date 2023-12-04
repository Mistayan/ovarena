"""
Player's instance in the maze
keep records of:
    positions (x, y) 
    direction (N, E, S, W)
    health
    inventory

on each updates (timebased)
"""""
import datetime.datetime as dt

from sqlalchemy import Column, Integer, String, Enum, DateTime


from . import Base, Direction

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    name = Column(String)
    health = Column(Integer, default=100)
    inventory = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    direction = Column(Enum(Direction))
    score = Column(Integer, default=0)

    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.x = 0
        self.y = 0
        self.direction = Direction.NORTH
        self.score = 0

    def __repr__(self):
        return f"<Player(name='{self.name}', health={self.health}," \
        f"inventory={self.inventory}, x={self.x}, y={self.y}, direction={self.direction})>"
