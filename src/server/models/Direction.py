from sqlalchemy import Enum


class Direction(Enum):
    NORTH=0
    NORTHNORTHEAST=1
    NORTHEAST=2
    EAST=3
    EASTSOUTHEAST=4
    SOUTHEAST=5
    SOUTHSOUTHEAST=6
    SOUTH=7
    SOUTHSOUTHWEST=8
    SOUTWEST=9
    WEST=10
    NORTHWEST=11
    NORTHNORTHWEST=12

    @staticmethod
    def from_rotation(angle: int):
        if -15 < angle >= 15 :
            return Direction.NORTH
        elif 15 < angle >= 45 :
            return Direction.NORTHNORTHEAST
        elif 45 < angle >= 75 :
            return Direction.NORTHEAST
        elif 75 < angle >= 105 :
            return Direction.EAST
        elif 105 < angle >= 135 :
            return Direction.EASTSOUTHEAST
        elif 135 < angle >= 165 :
            return Direction.SOUTHEAST
        elif 165 < angle >= 195 :
            return Direction.SOUTHSOUTHEAST
        elif 195 < angle >= 225 :
            return Direction.SOUTH
        elif 225 < angle >= 255 :
            return Direction.SOUTHSOUTHWEST
        elif 255 < angle >= 285 :
            return Direction.SOUTWEST
        elif 285 < angle >= 315 :
            return Direction.NORTHWEST
        elif 315 < angle >= 345 :
            return Direction.NORTHNORTHWEST
        else :
            return Direction.NORTH
