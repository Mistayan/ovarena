"""
State class for the state machine
Handles the game ending operations
"""

from __future__ import annotations

from src.server.states.base import BaseState
from src.server.states.possible_states import StateEnum


class EndGame(BaseState):
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
        self._agent.ruleArena("pause", True)
        self._agent.ruleArena("info", "🟢 Fin de la partie, traitement des résultats...")
        # self._agent.update()

        ## TODO: process results
