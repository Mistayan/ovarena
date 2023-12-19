"""
This file contains the StateEnum class
"""

from enum import Enum


class StateEnum(Enum):
    """
    An Enum is a classy way to put a name on a value
    Define the names of the states
    """
    WAIT_PLAYERS_CONNEXION = 0  # "WaitPlayersConnexionState"
    WAIT_PLAYERS = 1  # "WaitPlayersState / PauseState"
    IN_GAME = 2  # "InGameState"
    END_GAME = 3  # "EndGameState"
