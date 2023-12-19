"""
State class for the state machine
Handles waiting for players to connect to the arena
"""

from __future__ import annotations

from src import WaitPlayers, Player
from src.server.states.base import BaseState
from src.server.states.possible_states import StateEnum


class WaitPlayersConnexion(WaitPlayers):
    """
    Wait for all players to connect to the arena
    therefor, the game is paused if not all players are connected
    when all players are connected, the game starts
    """

    @property
    def name(self) -> StateEnum:
        return StateEnum.WAIT_PLAYERS_CONNEXION

    def _on_handle(self):
        """
        If all players are connected, switch to the InGame state
        If not, wait for players to connect
        When a player connects for the first time, it is registered to the arena
        """
        all_connected = self._agent.all_players_connected
        self._logger.info(f"Waiting for players to register : {not all_connected}")
        for player in self._agent.players:
            self._agent.register_player(Player(player))
            self._logger.debug(f"Player {player} is connected")

        super()._on_handle()  # if all players are connected, switch to the InGame state
