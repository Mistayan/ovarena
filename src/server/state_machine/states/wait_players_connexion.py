"""
State class for the state machine
Handles waiting for players to connect to the arena
"""

from __future__ import annotations

from src.server.models.player import Player
from .possible_states import StateEnum
from .wait_players import WaitPlayers


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
        all_connected = self._manager.all_players_connected
        self._logger.info(f"Waiting for players to register : {not all_connected}")
        for player in self._manager._robot.players:
            self._manager.register_player(Player(player))
            self._logger.debug(f"Player {player} is connected")

        super()._on_handle()  # if all players are connected, switch to the InGame state
