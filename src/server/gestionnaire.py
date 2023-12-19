"""
Game manager of the arena.
Watch the arena state machine and the arena events.
Apply the rules of the arena.
"""
import json
import logging
from copy import deepcopy, copy
from time import sleep
from typing import List, Dict, Any, Union, Tuple

import root_config
from src import WaitPlayers, InGame, EndGame
from src.api.j2l.pyrobotx.client import DefaultClientSettings
from src.api.j2l.pyrobotx.robot import RobotEvent
from src.server.manager_interface import IManager
from src.server.models import Player
from src.server.states.base import StateMachine
from src.server.states.possible_states import StateEnum
from src.server.states.wait_players_to_connect import WaitPlayersConnexion


class Gestionnaire(IManager):
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
        self.__loop_start_time = 0
        self.__loop_end_time = 0
        self.__game_running = False
        self.__registered_players: List[Player] = []

        print("Gestionnaire init")
        self.players: List[str] = []
        self._robot = super().__init__(nom, arene, username, password, server="mqtt.jusdeliens.com")
        print("Gestionnaire done super init")
        # define variables to retain information about the game
        self.__map: List[List[int]] = []
        self.__rules: Dict[str, Any] = {}
        self.__game_state = StateEnum.WAIT_PLAYERS  # initial state

        self.initiate_state_machine(StateMachine(self),
                                    (WaitPlayersConnexion, WaitPlayers, InGame, EndGame),
                                    [
                                        (StateEnum.WAIT_PLAYERS_CONNEXION, StateEnum.IN_GAME),
                                        (StateEnum.WAIT_PLAYERS_CONNEXION, StateEnum.WAIT_PLAYERS_CONNEXION),
                                        (StateEnum.WAIT_PLAYERS, StateEnum.IN_GAME),
                                        (StateEnum.IN_GAME, StateEnum.WAIT_PLAYERS),
                                        (StateEnum.IN_GAME, StateEnum.END_GAME),
                                        (StateEnum.END_GAME, StateEnum.WAIT_PLAYERS_CONNEXION)]
                                    )
        print("Gestionnaire done init")

        # define the rules of the arena
        self.ruleArena("info", "🔴 Arène en cours de construction ")
        self.update()
        with open("rules.json", "r", encoding="utf-8") as json_file:
            self.__rules = json.load(json_file)
            self.set_rules(self.__rules)
        self.__TIME_LIMIT = self.__rules.get("timeLimit")
        self.ruleArena("pause", True)
        self.ruleArena("reset", True)
        print("BEFORE", self.game)
        # change manager's State to wait for players
        self.ruleArena("info", "En attente des joueurs...")
        self.update()
        self.robot.addEventListener(RobotEvent.robotConnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.robotDisconnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.updated, self.on_update)
        print("AFTER", self.game)

    def on_update(self, other, event, value) -> None:
        """
        On each update, the manager checks the arena state machine and the arena events.
        For each player, it updates the player's state machine and the player's events.
        """
        # Let curent state handle the update and
        print(f"on_update : {self.__game_state.name} => {other.__class__.__name__} Received : {event} : {value}")
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
    def game_running(self) -> bool:
        """
        Return False if the game time is elapsed or all players are dead.
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
        while self.game_running:
            self.__loop_start_time = self.game['t']
            sleep(1)
            self.update()
            self.__loop_end_time = self.game['t']

    def set_rules(self, rules: Dict[str, Any]) -> None:
        self._logger.debug("Updating rumes to : " % self.__rules)
        self.__rules = rules

    def set_pause(self, pause: bool) -> bool:
        self.ruleArena("pause", pause)
        # self.update()
        return pause

    def set_map(self, game_map: List[List[int]]) -> bool:
        self.ruleArena("map", game_map)
        # self.update()
        if self.get_rules["map"] == game_map:
            return True
        return False

    def get_player(self, player_id: Union[int | str]) -> Player:
        for player in self.registered_players:
            if isinstance(player_id, int) and player.id == player_id \
                    or isinstance(player_id, str) and player.name == player_id:
                self._logger.debug(f"Found player {player.name} in registered players")
                return player
        return None

    def kill_player(self, player_id: int) -> Player:
        self._logger.info(f"Killing player {player_id}")
        p = self.get_player(player_id)
        p.health = 0
        return p

    def register_player(self, player: Player) -> Player:
        p = self.get_player(player.name)
        if p is not None:
            self._logger.debug(f"Found player {player}")
            player = p
        else:
            self._logger.info(f"Registering player {player}")
            self.__registered_players.append(player)
        return player

    def unregister_player(self, player_id: int) -> None:
        p = self.get_player(player_id)
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
        return "Gestionnaire"

    def display(self, message: str) -> None:
        """
        Display a message on the arena.
        :param message: the message to display
        """
        self.ruleArena("info", message)

    def get_state(self):
        return self.__game_state.name

    def __update_timers(self):
        """
        Depending on the current state, time passes differently.
        """
        if self.__game_state == StateEnum.WAIT_PLAYERS:
            self.__paused_time += self.game['t'] - (self.__loop_end_time - self.__loop_start_time)
        self._logger.debug(f"Timers : start={self.__start_time}, paused={self.__paused_time}, elapsed={self.game['t']}")

    def initiate_state_machine(self, machine: StateMachine, states: tuple, links: List[Tuple[StateEnum, StateEnum]],
                               initial_state: StateEnum = StateEnum.WAIT_PLAYERS_CONNEXION):
        self.__state_machine = StateMachine(self) if machine is None else machine

        [self.__state_machine.add_state(s) for s in states]
        self.__state_machine.define_states_links(links)
        self.__state_machine.set_actual_state(initial_state)  # optional, since stateMachine starts at index 0


if __name__ == '__main__':
    DefaultClientSettings.dtSleepUpdate = 100
    DefaultClientSettings.dtPing = 1000
    with Gestionnaire("...", "...", "...", "...") as gest:
        gest.game_loop()
