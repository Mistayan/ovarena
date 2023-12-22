"""
Game manager of the arena.
Watch the arena state machine and the arena events.
Apply the rules of the arena.
"""
from __future__ import annotations

import json
import logging
import os
from copy import deepcopy, copy
from typing import List, Dict, Any, Union

import root_config
from src.api.j2l.pyrobotx.robot import RobotEvent
from src.server.manager_interface import IManager
from src.server.models import Player
from src.server.states.base import StateMachine
from src.server.states.possible_states import StateEnum

__current_dir__ = os.path.dirname(os.path.abspath(__file__))

from src.server.states import WaitGameStart, WaitPlayers, InGame, EndGame

from src.server.states.wait_players_to_connect import WaitPlayersConnexion


def _init_logger():
    import colorama
    colorama.init()


class ArenaManager(IManager):
    """
    This class is the manager of the arena. It handles the arena state machine and the arena events.
    Subclass of Agent that handles the connection to the server,
     and allows basic communication and control of the robot.
    """

    __state_machine: StateMachine

    def __init__(self, nom, arene, username, password):
        """
        Constructor of the class Gestionnaire, subclass of Agent.
        :param nom: name of the robot : should be registered in a .dotenv file
        :param arene: name of the arena : should be registered in a .dotenv file
        :param username: username of the robot : should be registered in a .dotenv file
        :param password: password of the robot : should be registered in a .dotenv file
        """
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(root_config.LOGGING_LEVEL)
        self.__start_time = 0
        self.__paused_time = 0
        self.__game_running = False
        self.__registered_players: List[Player] = []

        self._robot = super().__init__(nom, arene, username, password)
        _init_logger()
        # define variables to retain information about the game
        self.__map: List[List[int]] = []
        self.__rules: Dict[str, Any] = {}

        self.__state_machine = StateMachine(self).define_states(
            states=(WaitPlayersConnexion, WaitPlayers, InGame, EndGame, WaitGameStart),
            links=[
                (StateEnum.WAIT_PLAYERS_CONNEXION, StateEnum.WAIT_GAME_START),
                (StateEnum.WAIT_GAME_START, StateEnum.WAIT_PLAYERS_CONNEXION),
                (StateEnum.WAIT_GAME_START, StateEnum.IN_GAME),
                (StateEnum.WAIT_PLAYERS, StateEnum.IN_GAME),
                (StateEnum.IN_GAME, StateEnum.WAIT_PLAYERS),
                (StateEnum.IN_GAME, StateEnum.END_GAME),
                (StateEnum.END_GAME, StateEnum.WAIT_PLAYERS_CONNEXION)],
            initial_state=StateEnum.WAIT_PLAYERS_CONNEXION
        )

        # define the rules of the arena
        self.ruleArena("info", "🔴 Arène en cours de construction ")
        self.update()
        with open(os.path.join(__current_dir__, "rules.json"), "r", encoding="utf-8") as json_file:
            self.__rules = json.load(json_file)
            self.__update_rules(self.__rules)
        self.__TIME_LIMIT = self.__rules.get("timeLimit")  # todo: change on game rule update
        self.ruleArena("pause", True)
        self.ruleArena("reset", True)
        print("BEFORE", self.game)
        # change manager's State to wait for players
        self.ruleArena("info", "En attente des joueurs...")
        self.update()
        self.robot.addEventListener(RobotEvent.robotConnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.robotDisconnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.updated, self.on_update)
        self.robot.addEventListener(RobotEvent.playerChanged, self.__state_machine.handle)
        print("AFTER", self.game)
        print("Gestionnaire done init")

    def on_update(self, other, event, value) -> None:
        """
        On each update, the manager checks the arena state machine and the arena events.
        For each player, it updates the player's state machine and the player's events.
        """
        print(f"on_update : {self.state} => {other.__class__.__name__} "
              f"Received : {event} : {value}")
        super()._onUpdated(other, event, value)
        # Let curent state handle the update and
        self.__update_timers()
        self.__state_machine.handle()

        # update players
        self.update_players()

    @property
    def __all_players_dead(self) -> bool:
        """
        Return True if all players are dead.
        """
        for player in self.registered_players:
            if player.health > 0:
                return False
        return True

    @property
    def __timer_running(self) -> bool:
        """
        Return False if the game time is elapsed.
        """
        return self.game["t"] <= self.__start_time + self.__paused_time + self.__TIME_LIMIT

    @property
    def game_loop_running(self) -> bool:
        """
        Return True if the game time is elapsed or all players are dead.
        """
        return self.__timer_running or self.__all_players_dead

    @property
    def all_players_connected(self) -> bool:
        """ return True if all players are connected """
        wanted = self.__rules['maxPlayers']
        registered = len(self.__registered_players)
        self._logger.debug(f"registered : {registered}, wanted : {wanted}")
        status = registered == wanted
        self._logger.info(f"All players connected : {status}")
        return status

    @property
    def get_rules(self) -> Dict[str, Any]:
        return deepcopy(self.__rules)

    @property
    def registered_players(self) -> List[Player]:
        return copy(self.__registered_players)

    def game_loop(self):
        """
        This method is the main loop of the game.
        """
        print("Game loop started")
        self.__start_time = self.game['t']

        while self.state != "END_GAME":
            self._logger.debug(f"Game loop running : {self.game_loop_running} => {self.state}")
            super().game_loop()
            self._logger.debug(f"Game loop ended ! Running : {self.game_loop_running}")
            self.__state_machine.handle()

        self._logger.info(f"Game total time : {(int(self.game['t']) - self.__start_time) // 1000}s")
        self._logger.debug(f"Game infos : {self.__game_infos}")
        self._logger.info("Generating score board...")
        self.__state_machine.handle()
        self._logger.info("Score board generated ! Displaying and ending game...")
        self._logger.debug("leaving game_loop !")

    def __update_rules(self, rules: Dict[str, Any]) -> None:
        """
        Set the rules of the arena.
        :param rules: the rules to set
        """
        self._logger.debug(f"Updating rules to : {self.__rules}")
        self.__rules = rules
        for key, value in rules.items():
            self.ruleArena(key, value)
        self.update()

    def set_pause(self, pause: bool) -> bool:
        """
        Set the pause state of the arena.
        :param pause: True to pause the arena, False to unpause
        """
        self.ruleArena("pause", pause)
        # self.update()
        return pause

    def set_map(self, _map: List[List[int]]) -> bool:
        """
        Set the map of the arena.
        :param _map: the map to set
        """
        self.ruleArena("map", _map)
        # self.update()
        if self.get_rules["map"] == _map:
            return True
        return False

    def __get_player(self, player_id: Union[int | str]) -> Player:
        """
        Get a player from the arena.
        :param player_id: the id of the player to get
        """
        for player in self.registered_players:
            if isinstance(player_id, int) and player.id == player_id \
                    or isinstance(player_id, str) and player.name == player_id:
                self._logger.debug(f"Found player {player.name} in registered players")
                return player

    def kill_player(self, player_id: int) -> Player:
        """
        Kill a player.
        :param player_id: the id of the player to kill
        :return: the killed player
        """
        self._logger.info(f"Killing player {player_id}")
        p = self.__get_player(player_id)
        p.health = 0
        return p

    def register_player(self, player: Player) -> Player:
        """
        Register a player to the arena.
        If the player is already registered, return the registered player.
        :param player: the player to register
        :return: the registered player
        """
        p = self.__get_player(player.name)
        if p is not None:
            self._logger.debug(f"Found player {player}")
            player = p
        else:
            self._logger.info(f"Registering player {player}")
            self.__registered_players.append(player)
        return player

    def unregister_player(self, player_id: str) -> None:
        """
        Unregister a player from the arena.
        :param player_id: the id of the player to unregister
        """
        p = self.__get_player(player_id)
        self.rulePlayer(p.name, "reset", True)
        self.registered_players.remove(p)

    def update_player_stats(self, player: Union[int | str]) -> Player:
        pass

    def update_players(self, *args, **kwargs) -> None:
        """
        This method on each update, gathers players from arena and update them internally.
        It also handles the players' events.
        """
        # get players from arena
        arena_players = self.players
        if arena_players is None or len(arena_players) == 0:
            raise ValueError("No players found in arena")
            # TODO : HANDLE OTHER EVENTS

    def __str__(self):
        """
        String representation of the object.
        """
        return "Gestionnaire"

    def display(self, message: str) -> None:
        """
        Display a message on the arena.
        :param message: the message to display
        """
        self.ruleArena("info", message)

    @property
    def state(self) -> str:
        """
        Return the actual state name of the arena.
        """
        return self.__state_machine.state

    @property
    def __game_infos(self) -> Dict[str, Any]:
        """
        Return the game info dict.
        """
        return {
            self.game['t']: {
                "state": self.state,
                "players": self.players,
                "registered_players": self.registered_players,
                "time_limit": self.get_rules['timeLimit'],
                "timers": self.__timers
            }
        }

    @property
    def __timers(self) -> Dict[str, Any]:
        """
        Return the timers of the game.
        """
        return {
            "start_time": self.__start_time,
            "paused_time": self.__paused_time,
            "loop_execution_time": f"{int(self.last_loop_time)}ms",
            "game_time": self.game['t'],

        }

    @property
    def game_running(self) -> bool:
        """
        Return the game_running attribute.
        """
        return self.__game_running

    @game_running.setter
    def game_running(self, value: bool) -> None:
        """
        Set the game_running attribute.
        """
        if not isinstance(value, bool):
            raise TypeError("game_running must be a boolean")
        if ("WAIT" or "END") in self.state:
            raise ValueError("Cannot start game while waiting for players to connect")
        self.__game_running = value

    def __update_timers(self):
        """
        Depending on the current state, time passes differently.
        """
        self._logger.debug(f"Current game state: {self.state}")
        if "WAIT" in self.state:
            self.__paused_time += (int(self.game['t']) - self.__start_time
                                   - self.last_loop_time - self.__paused_time)
            self._logger.debug(f"Paused time : {self.__paused_time}")
        self._logger.debug(f"Timers : {self.__timers}")

    def restart(self):
        """
        Restart the game.
        """
        self._logger.info("Restarting game...")
        self.set_pause(True)
        self.__game_running = False
        self.__start_time = self.game['t']
        for player in self.registered_players:
            self.unregister_player(player.name)
        self.__state_machine.set_actual_state(StateEnum.WAIT_PLAYERS_CONNEXION)

    def stop(self):
        """
        Stop the game.
        """
        self._logger.info("Stopping game...")
        self.__state_machine.set_actual_state(StateEnum.END_GAME)
        self.__state_machine.handle()

    def mod_game(self, key: str, value: Any) -> None:
        """
        set the game key to the given value
        """
        self.ruleArena(key, value)
        self.update()


if __name__ == '__main__':
    import dotenv

    dotenv.load_dotenv()
    print(os.getenv("USER"))
    with ArenaManager(
            os.getenv("USER"),
            os.getenv("ARENA"),
            os.getenv("LOGIN"),
            os.getenv("PASSWORD")
    ) as gest:
        gest.game_loop()
