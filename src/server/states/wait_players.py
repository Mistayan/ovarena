"""
State class for the state machine
Handles waiting for players to connect to the arena
"""

from __future__ import annotations

from src.server.states.base import BaseState
from src.server.states.possible_states import StateEnum


class WaitPlayers(BaseState):
    """
    Wait for all players to connect to the arena
    therefor, the game is paused if not all players are connected
    when all players are connected, the game starts
    """

    @property
    def name(self) -> StateEnum:
        return StateEnum.WAIT_PLAYERS

    def _on_handle(self):
        """
        If all players are connected, switch to the InGame state
        If not, wait for players to connect
        """
        all_connected = self._agent.all_players_connected
        self._logger.info(f"Waiting for players to connect : {all_connected}")

        # Handle events
        if not all_connected:
            self.__wait_all_players()
        else:
            self.__start_game()

    def __wait_all_players(self):
        """
        Wait for all players to connect
        pause the game and display "waiting for players"
        """
        self._agent.ruleArena("pause", True)
        self._agent.ruleArena("info", "En attente des joueurs...")
        self._agent.update()

    def __start_game(self):
        """
        switch to the InGame state
        """
        self.switch_state(StateEnum.IN_GAME)
