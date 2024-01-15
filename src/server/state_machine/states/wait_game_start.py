"""
State class for the state machine
Handles waiting for players to connect to the arena
"""

from __future__ import annotations

import time

from .possible_states import StateEnum
from .wait_players import WaitPlayers


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
        time.sleep(1)
        if self._manager.game_loop_running:
            return self.switch_state(StateEnum.IN_GAME)
