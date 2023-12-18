"""
State class for the state machine
Handles the game operations
"""

from __future__ import annotations

from src.server.states.base import BaseState
from src.server.states.possible_states import StateEnum


class InGame(BaseState):
    """
    Game just started and is running
    """

    @property
    def name(self) -> StateEnum:
        return StateEnum.IN_GAME

    def _on_handle(self):
        """
        If a player disconnects, switch to the WaitPlayers state
        If the game is paused, unpause it
        If the game is over, switch to the EndGame state
        Handle the game operations
        """
        if not self._agent.all_players_connected:
            return self.switch_state(StateEnum.WAIT_PLAYERS)
        if not self._agent.game_running:
            return self.switch_state(StateEnum.END_GAME)
        if self._agent.game["pause"]:
            return self.__unpause()
        self.__update()

    def __unpause(self):
        self._agent.set_pause(False)
        self._agent.display("🟢 Reprise de la partie !")
        # self._agent.update()

    def __handle_players_events(self):
        """
        If a player hits a wall, walks on a trap, gets hit, etc...
        """
        ...  # TODO: handle players events

    def __handle_game_events(self):
        """
        If the game time is elapsed, a player is dead, etc...
        """
        ...  # TODO: handle game events after updating players

    def __update(self):
        """
        Update the game state
        """
        self.__loop_start_time = self._agent.game["timeElapsed"]
        if self.__loop_start_time % 6000 == 0:
            self._agent.display(f"🟢 {self.__loop_start_time // 6000} minutes écoulées")
        self.__handle_players_events()
        self.__handle_game_events()
        self._agent.update()
