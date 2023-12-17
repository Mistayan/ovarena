"""
This file contains the StateEnum class
"""

from enum import Enum


class StateEnum(Enum):
    """
    An Enum is a classy way to put a name on a value
    Define the names of the states
    """
    WAIT_PLAYERS = 0  # "WaitPlayersState / PauseState"
    IN_GAME = 1  # "InGameState"
    END_GAME = 2  # "EndGameState"
