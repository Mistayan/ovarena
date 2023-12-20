"""
States Package
Contains all available States and their connections
"""
from .base import State, BaseState, StateEnum, StateMachine
from .end_game import EndGame
from .in_game import InGame
from .wait_players import WaitPlayers
from .wait_game_start import WaitGameStart
