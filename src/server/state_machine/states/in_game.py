"""
State class for the state machine
Handles the game operations
"""

from __future__ import annotations

from .base import GameState
from .possible_states import StateEnum


class InGame(GameState):
    """
    Game just started and is running
    This state handles the game operations
    It can :
        - pause/unpause the game
        - handle players events
        - handle game events
    """

    def __init__(self, agent):
        super().__init__(agent)
        self.__loop_start_time = 0

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
        if self._agent.game["pause"]:
            self.__unpause()
        if not self._agent.all_players_connected:
            self.switch_state(StateEnum.WAIT_PLAYERS)
        if not self._agent.game_loop_running:
            self.switch_state(StateEnum.END_GAME)
        self.__update()

    def __unpause(self):
        """
        The game is paused, unpause it
        """
        self._agent.set_pause(False)
        self._agent.display("🟢 Reprise de la partie !")
        # self._agent.update()

    def __handle_players_events(self):
        """
        If a player hits a wall, walks on a trap, gets hit, etc...
        """
        # TODO: handle players events

    def __handle_game_events(self):
        """
        If the game time is elapsed, a player is dead, etc...
        """
        # TODO: handle game events after updating players

    def __update(self):
        """
        Update the game state
        """
        self.__loop_start_time = self._agent.game["timeElapsed"]
        if self.__loop_start_time % 6000 == 0:
            self._agent.display(f"🟢 {self.__loop_start_time // 6000} minutes écoulées")
        self.__handle_players_events()
        self.__handle_game_events()
        # self._agent.update()
