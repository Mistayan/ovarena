"""
This file contains the StateEnum class
"""

from enum import Enum


class StateEnum(Enum):
    """
    An Enum is a classy way to put a name on a value
    Define the names of the states
    """
    WAIT_PLAYERS_CONNEXION = 0,
    WAIT_PLAYERS = 1,
    IN_GAME = 2,
    END_GAME = 3,
    WAIT_GAME_START = 4,

    def __init__(self, name: str):
        self._name = name
