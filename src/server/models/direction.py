from sqlalchemy import Enum

"""
classe de type Enum pour définir une Range d'orientations (tous les 30°)
"""
class Direction(Enum):
    """
    définit les directions ordinales cardinales
    utiliser la méthode from_rotation(...) pour récupérer la valeur ordinale de l'angle actuel
    """
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
        """
        @params : 
         - angle: int : la valeur de l'orientation renvoyée par la boussole du robot
        """
        if type(angle) != int or 0 < angle > 360:
            raise ValueError("une Orientation est définie par un entier 'angle' compris entre 0 et 360 (°)")
        orientation = Direction.NORTH
        if angle <= 30 :
            orientation = Direction.NORTH
        elif angle <= 60 :
            orientation = Direction.NORTHNORTHEAST
        elif angle <= 90 :
            orientation = Direction.NORTHEAST
        elif angle <= 120 :
            orientation = Direction.EAST
        elif angle <= 150 :
            orientation = Direction.EASTSOUTHEAST
        elif angle <= 180 :
            orientation = Direction.SOUTHEAST
        elif angle <= 210 :
            orientation = Direction.SOUTHSOUTHEAST
        elif angle <= 240 :
            orientation = Direction.SOUTH
        elif angle <= 270 :
            orientation = Direction.SOUTHSOUTHWEST
        elif angle <= 300 :
            orientation = Direction.SOUTWEST
        elif angle <= 330 :
            orientation = Direction.NORTHWEST
        elif angle > 330 && angle < 360 :
            orientation = Direction.NORTHNORTHWEST
        return orientation
