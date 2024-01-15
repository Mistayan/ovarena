"""
State class for the state machine
Handles the game ending operations
"""

from __future__ import annotations

from .base import GameState
from .possible_states import StateEnum


class EndGame(GameState):
    """
    Game just ended
    Pause game
    Change arena info to "Game ended, processing results"
    """

    @property
    def name(self) -> StateEnum:
        return StateEnum.END_GAME

    def _on_handle(self):
        """
        Pause the game and process the results
        """
        self._manager.set_pause(True)
        self._manager.display("🟢 Fin de la partie, traitement des résultats...")
        # self._agent.update()

        ## TODO: process results
