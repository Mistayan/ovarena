"""
Game manager of the arena.
Watch the arena state machine and the arena events.
Apply the rules of the arena.
"""
from __future__ import annotations

import json
import logging
import os
from copy import copy
from typing import List, Dict, Any, Union

import colorama

import root_config
from src.server.manager_interface import IManager
from src.server.models import Player
from src.server.state_machine import StateMachine, StateMachineConfig
from src.server.state_machine.states.possible_states import StateEnum

__current_dir__ = os.path.dirname(os.path.abspath(__file__))


def _init_logger():
    colorama.init()


def on_update(source, event, value_before=None, value_after=None):
    """
    Callback appelée à chaque évènement du robot
    """
    print("Rx event ", event, " from ", source, " : ", value_before, " => ", value_after)


class ArenaManager(IManager):
    """
    This class is the manager of the arena. It handles the arena state machine and the arena events.
    Subclass of Agent that handles the connection to the server,
     and allows basic communication and control of the robot.
    """

    __state_machine: StateMachine

    def __init__(self, agent):
        """
        Constructor of the class Manager, act on Agent.
        :param agent: the agent to act on
        """
        from src.api.j2l.pytactx.agent import Agent
        if not isinstance(agent, Agent):
            raise TypeError("Agent must be a subclass of Agent")
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(root_config.LOGGING_LEVEL)
        self.__start_time = 0
        self.__paused_time = 0
        self.__game_running = False
        self.__registered_players: List[Player] = []
        self.__arena_rules_keys = set(agent.game.keys())
        self.__state_machine = StateMachine(self).define_states(StateMachineConfig())
        super().__init__(agent, self.__state_machine)
        _init_logger()
        agent.set_context(self)
        # define variables to retain information about the game
        # self.__map: List[List[int]] = []
        self.__rules = agent.game
        self._logger.info("Rules on startup :", self.__rules)

        # define the rules of the arena
        self.display("🔴 Arène en cours de construction ")
        with open(os.path.join(__current_dir__, "rules.json"), "r", encoding="utf-8") as json_file:
            rules = json.load(json_file)
            self.__update_rules(rules)
            self.__time_limit = int(rules["timeLimit"])
        self.restart()
        # change manager's State to wait for players
        self.display("En attente des joueurs...")
        self._logger.info("rules after updates", self._robot.game)
        self._logger.debug("Gestionnaire done init")

    def _on_update(self, other, event, value) -> None:
        """
        On each update, the manager checks the arena state machine and the arena events.
        For each player, it updates the player's state machine and the player's events.
        """
        self._logger.debug(f"on_update : {self.state} => {other.__class__.__name__} "
                           f"Received : {event} : {value}")
        # Let curent state handle the update
        self.__update_timers()
        if isinstance(value, dict):
            self.__update_rules(value)
        self.__state_machine.handle()

    @property
    def __all_players_dead(self) -> bool:
        """
        Return True if all players are dead.
        """
        alive = 0
        for player in self.registered_players:
            if player.health > 0:
                alive += 1
        return alive == 0

    @property
    def __timer_running(self) -> bool:
        """
        Return False if the game time is elapsed.
        """
        return (int(self.__rules["t"]) <=
                self.__start_time + self.__paused_time + self.__time_limit)

    @property
    def game_loop_running(self) -> bool:
        """
        Return True if the game time is elapsed or all players are dead.
        """
        return self.__timer_running and not self.__all_players_dead and self.all_players_connected

    @property
    def all_players_connected(self) -> bool:
        """ return True if all players are connected """
        wanted = int(self.__rules['maxPlayers'])
        registered = len(self.__registered_players)
        self._logger.debug(f"registered : {registered}, wanted : {wanted}")
        status = registered == wanted and len(self._robot.players) == wanted
        self._logger.info(f"All players connected : {status}")
        return status

    @property
    def get_rules(self):
        """
        Get the rules applied to the arena.
        """
        return self.__rules

    @property
    def registered_players(self) -> List[Player]:
        """
        Return the copy of the list of registered players.
        """
        return copy(self.__registered_players)

    def game_loop(self):
        """
        This method is the main loop of the game.
        """
        self._logger.info("Game loop started")
        self.__start_time = self._robot.game['t']

        while self.state != "END_GAME":
            super().game_loop()
            self.__state_machine.handle()
            self._logger.debug(f"Game loop running : {self.game_loop_running} => {self.state}")

        self._logger.info(f"Game total time :"
                          f" {(int(self._robot.game['t']) - self.__start_time) // 1000}s")
        self._logger.debug(f"Game infos : {self.__game_infos}")
        self._logger.info("Generating score board...")
        self.__state_machine.handle()
        self._logger.info("Score board generated ! Displaying and ending game...")
        self._logger.debug("leaving game_loop !")

    def __update_rules(self, rules: Dict[str, Any] = None) -> None:
        """
        Set the rules of the arena.
        :param rules: the rules to set
        """
        if not rules:
            return
        self._logger.debug(f"Updating rules to : {rules}")
        for key, value in rules.items():
            self._robot.ruleArena(key, value)
        self._robot.update()

    def set_pause(self, pause: bool) -> bool:
        """
        Set the pause state of the arena.
        :param pause: True to pause the arena, False to unpause
        """
        self._robot.ruleArena("pause", pause)
        self._robot.update()
        return self._robot.game["pause"]

    def set_map(self, _map: List[List[int]]) -> bool:
        """
        Set the map of the arena.
        :param _map: the map to set
        """
        self._robot.ruleArena("map", _map)
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

    def kill_player(self, player: str) -> Player:
        """
        Kill a player.
        :param player: player to kill
        :return: the killed player
        """
        self._logger.info(f"Killing player {player}")
        p = self.__get_player(player)
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
        self._robot.rulePlayer(p.name, "reset", True)
        self.__registered_players.remove(p)

    def update_player_stats(self, player: Union[int | str]) -> Player:
        pass

    def update_players(self, a1, event, before, after) -> None:
        """
        This method on each update, gathers players from arena and update them internally.
        It also handles the players' events.
        """
        # get players from arena
        arena_players = self._robot.players
        if arena_players is None or len(arena_players) == 0:
            raise ValueError("No players found in arena")
            # TODO : HANDLE OTHER EVENTS
        self._logger.debug(f"Players : {arena_players}, from : {a1},"
                           f" event : {event}, before : {before}, after : {after}")

    def __str__(self):
        """
        String representation of the object.
        """
        return "Manager"

    def display(self, message: str) -> None:
        """
        Display a message on the arena.
        :param message: the message to display
        """
        self._logger.debug(f"sending : {message}")
        self._robot.ruleArena("info", message)

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
            self._robot.game['t']: {
                "state": self.state,
                "players": self._robot.players,
                "registered_players": self.registered_players,
                "time_limit": self.__time_limit,
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
            "loop_exec_time": f"{int(self.last_loop_time)}ms",
        }

    @property
    def game_running(self) -> bool:
        """
        Return the game_running attribute.
        """
        return self.__game_running

    def __update_timers(self):
        """
        Depending on the current state, time passes differently.
        """
        self._logger.debug(f"Current game state: {self.state}")
        if "WAIT" in self.state:
            self.__paused_time += (int(self._robot.game['t']) - self.__start_time
                                   - self.last_loop_time - self.__paused_time)
            self._logger.debug(f"Paused time : {self.__paused_time}")
        self._logger.debug(f"Timers : {self.__timers}")

    def restart(self):
        """
        Restart the game.
        """
        self._logger.info("Restarting game...")
        self._robot.ruleArena("pause", True)
        self._robot.ruleArena("reset", True)
        self._robot.ruleArena("open", True)
        for player in self.registered_players:
            self.unregister_player(player.name)
        self.__state_machine.set_actual_state(StateEnum.WAIT_PLAYERS_CONNEXION)
        self.__start_time = self.__rules['t']
        self._robot.update()  # sync rules and game
        self.__state_machine.handle()

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
        self._robot.ruleArena(key, value)
        self._robot.update()


if __name__ == '__main__':
    import dotenv
    from src.server.arena_agent import SyncAgent

    dotenv.load_dotenv()
    print(os.getenv("USER"))
    agent: SyncAgent = SyncAgent(
        os.getenv("USER"),
        os.getenv("ARENA"),
        os.getenv("USERNAME"),
        os.getenv("PASSWORD"),
        os.getenv("SERVER"),
        int(os.getenv("PORT"))
    )
    with ArenaManager(agent) as gest:
        gest.game_loop()
        agent.disconnect()
