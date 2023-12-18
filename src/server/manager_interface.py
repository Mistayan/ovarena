"""
Interface for the Manager.
This class defines the actions a Manager can do on the game.
"""

from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, Any, List

import root_config
from src.api.j2l.pytactx.agent import Agent
from src.server.models import Player


class IManager(Agent, ABC):
    """
    Define the interface for managing the arena.

    Every method must be implemented by the Manager.
    """

    @abstractmethod
    def __init__(self, nom, arene, username, password, server="mqtt.jusdeliens.com"):
        print("IManager super init")
        super().__init__(nom, arene, username, password, server=server, verbosity=root_config.LOGGING_LEVEL)
        print("IManager done init")

    @abstractmethod
    def game_loop(self):
        """
        This method is the main loop of the game.
        it should only be called once
        before running a game loop, ensure that all callbacks are set
        """
        while True:
            sleep(0.1)
            self.update()

    ############################
    # CONNECTIVITY MANAGEMENT  #
    ############################
    @abstractmethod
    def on_update(self) -> None:
        """
        Define what must be done on each update.
        """
        pass

    ##########################
    # ARENA RULES MANAGEMENT #
    ##########################

    @abstractmethod
    def set_rules(self, rules: Dict[str, Any]) -> None:
        """
        Set the rules of the arena.
        """
        pass

    @abstractmethod
    def get_rules(self) -> Dict[str, Any]:
        """
        Get the rules applied to the arena.
        """
        pass

    @abstractmethod
    def all_players_connected(self) -> bool:
        """ return True if all players are connected """
        pass

    @abstractmethod
    def set_pause(self, pause: bool) -> bool:
        """
        un/pause the game
        this method waits for the game response and return it
        :param pause: True to pause the game, False to resume
        :return: the new pause state applied to the game
        """
        pass

    @abstractmethod
    def set_map(self, map: List[List[int]]) -> bool:
        pass

    ############################
    # ARENA PLAYERS MANAGEMENT #
    ############################
    @abstractmethod
    def kill_player(self, player_id: int) -> Player:
        """
        Kill a player.
        :param player_id: the id of the player to kill
        :return: the killed player's reference
        """
        pass

    @abstractmethod
    def register_player(self, player: Player) -> Player:
        """
        Spawn a player.
        :param player: the player to register to the arena and spawn
        :return: the registered player's reference
        """
        pass

    @abstractmethod
    def unregister_player(self, player_id: int) -> None:
        """
        Unregister a player. (cannot be undone)
        :param player_id: the id of the player to unregister
        """
        pass

    @abstractmethod
    def update_players(self, *args, **kwargs):
        """
        This method is called when a player connects or disconnects.
        """
        pass

    @abstractmethod
    def update_player_stats(self, player: Player) -> Player:
        """
        Update a player.
        :param player: the player to update
        :return: the updated player's reference
        """
        pass

    @abstractmethod
    def get_player(self, player_id: int) -> Player:
        """
        Get a player.
        :param player_id: the id of the player to get
        :return: the player reference if found, None otherwise
        """
        pass

    # @abstractmethod
    # def wait_all_players(self, *args, **kwargs):
    #     """
    #     This method is called when a player connects or disconnects.
    #     """
    #     pass

    def __enter__(self):
        """
        called when entering a with statement
        """
        if not self.isConnectedToRobot():
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        called when exiting a with statement
        """
        self.disconnect()
        return False
