"""
Define an Enum for the direction of the player
"""
from sqlalchemy import Enum

class Direction(Enum):
    """
    Enum for the direction of the player
    Decomposed in 12 directions
    """
    NORTH = 0
    NORTHNORTHEAST = 1
    NORTHEAST = 2
    EAST = 3
    EASTSOUTHEAST = 4
    SOUTHEAST = 5
    SOUTHSOUTHEAST = 6
    SOUTH = 7
    SOUTHSOUTHWEST = 8
    SOUTWEST = 9
    WEST = 10
    NORTHWEST = 11
    NORTHNORTHWEST = 12

    @staticmethod
    def from_rotation(angle: int):
        """
        Convert an angle to a direction
        """
        if angle < 0:
            angle += 360
        angle = int(angle) // 30
        return Direction(angle)
