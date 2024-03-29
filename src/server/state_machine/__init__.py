"""
State machine package
"""

__export__ = ["states", "state_machine", "state_machine_config"]

from .state_machine import StateMachine, StateMachineConfig
from .states import (
    StateEnum, GameState, InGame, WaitGameStart,
    WaitPlayers, WaitPlayersConnexion, EndGame
)
