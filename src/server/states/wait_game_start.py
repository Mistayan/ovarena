"""
State class for the state machine
Handles waiting for players to connect to the arena
"""

from __future__ import annotations

from src.server.states import WaitPlayers
from src.server.states.possible_states import StateEnum


class WaitGameStart(WaitPlayers):
    """
    Wait for all players to connect to the arena
    therefor, the game is paused if not all players are connected
    when all players are connected, the game starts
    """

    @property
    def name(self) -> StateEnum:
        return StateEnum.WAIT_GAME_START

    def _on_handle(self):
        """
        If all players are connected, switch to the InGame state
        If not, wait for players to connect
        """
        if self._agent.game_loop_running:
            self.switch_state(StateEnum.IN_GAME)
        if self._agent.all_players_connected:
            self.switch_state(StateEnum.WAIT_PLAYERS_CONNEXION)
