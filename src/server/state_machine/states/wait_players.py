"""
State class for the state machine
Handles waiting for players to connect to the arena
"""
import time

from .base import GameState
from .possible_states import StateEnum


class WaitPlayers(GameState):
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
        all_connected = self._manager.all_players_connected

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
        time.sleep(1)
        self._manager._robot.ruleArena("pause", True)
        self._manager.display("En attente de reconnection des joueurs...")
        # self._agent.update()

    def __start_game(self):
        """
        switch to the InGame state
        """
        self.switch_state(StateEnum.WAIT_GAME_START)
