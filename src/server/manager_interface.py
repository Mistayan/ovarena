"""
Interface for the Manager.
This class defines the actions a Manager can do on the game.
"""

from abc import ABC, abstractmethod
from time import sleep, perf_counter
from typing import Dict, Any, List

import root_config
from src.api.j2l.pytactx.agent import Agent
from .models import Player


class IManager(ABC):
    """
    Define the interface for managing the arena.

    Every method must be implemented by the Manager.
    """
    _robot: Agent

    @abstractmethod
    def __init__(self, agent: Agent):
        """
        Initialize the manager.
        use super().__init__() to initialize the Agent
        """
        self.__last_loop_time = 0
        print("IManager super init")
        if not isinstance(agent, Agent):
            raise TypeError(f"Agent must be a subclass of Agent, got {type(agent)}")
        self._robot = agent
        print("IManager done init")

    @property
    def last_loop_time(self) -> int:
        """
        Return the time of the last loop in milliseconds
        """
        return int(self.__last_loop_time)

    @abstractmethod
    def game_loop(self):
        """
        This method is the main loop of the game.
        it should only be called once
        before running a game loop, ensure that all callbacks are set
        """
        while self.game_loop_running:
            sleep(1.501)
            loop_start_time = perf_counter()
            self._robot.update()
            self.__last_loop_time = (perf_counter() - loop_start_time) * 1000

    ############################
    # CONNECTIVITY MANAGEMENT  #
    ############################
    @abstractmethod
    def on_update(self, other, event, value) -> None:
        """
        Define what must be done on each update.
        """

    ##########################
    # ARENA RULES MANAGEMENT #
    ##########################

    @property
    @abstractmethod
    def get_rules(self) -> Dict[str, Any]:
        """
        Get the rules applied to the arena.
        """

    @property
    @abstractmethod
    def all_players_connected(self) -> bool:
        """ return True if all players are connected """

    @abstractmethod
    def set_pause(self, pause: bool) -> bool:
        """
        un/pause the game
        this method waits for the game response and return it
        :param pause: True to pause the game, False to resume
        :return: the new pause state applied to the game
        """

    @abstractmethod
    def set_map(self, _map: List[List[int]]) -> bool:
        """
        Set the map of the arena.
        """

    ############################
    # ARENA PLAYERS MANAGEMENT #
    ############################
    @abstractmethod
    def kill_player(self, player: str) -> Player:
        """
        Kill a player.
        :param player: player to kill
        :return: the killed player's reference
        """

    @abstractmethod
    def register_player(self, player: Player) -> Player:
        """
        Spawn a player.
        :param player: the player to register to the arena and spawn
        :return: the registered player's reference
        """

    @abstractmethod
    def unregister_player(self, player_id: int) -> None:
        """
        Unregister a player. (cannot be undone)
        :param player_id: the id of the player to unregister
        """

    @abstractmethod
    def update_players(self, a1, event, before, after) -> None:
        """
        This method is called when a player connects or disconnects.
        """

    @abstractmethod
    def update_player_stats(self, player: Player) -> Player:
        """
        Update a player.
        :param player: the player to update
        :return: the updated player's reference
        """

    @property
    @abstractmethod
    def state(self) -> str:
        """
        Return the actual state name of the arena.
        """

    @abstractmethod
    def display(self, message):
        """
        Display a message on the arena.
        """

    @property
    @abstractmethod
    def game_loop_running(self) -> bool:
        """
        return True if the game is running
        """

    def __del__(self):
        self._robot.disconnect()
        print("Manager deleted")

    def __enter__(self):
        """
        called when entering a with statement
        """
        while not self._robot.isConnectedToArena():
            self._robot.connect()
            sleep(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        called when exiting a with statement
        """
        self._robot.disconnect()
        return False
