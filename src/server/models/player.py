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
    """
        Base du joueur, à utiliser pour instancier un robot dans l'arène
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    name = Column(String)
    score = Column(Integer, default=0)

    def __init__(self, name):
        self.name = name
        self.score = 0

    def __repr__(self):
        return f"<Player(name='{self.name}', score='{self.score}')>"


class RobotPlayer(Player):
    """
        Représentation du joueur dans l'arène (ayant un robot)
    """
    health = Column(Integer)
    inventory = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    direction = Column(Enum)
    
    def __init__():
        self.health = 100
        self.inventory = []
        self.x = 0
        self.y = 0
        self.direction = Direction.NORTH
