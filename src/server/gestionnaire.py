"""
Game manager of the arena.
Watch the arena state machine and the arena events.
Apply the rules of the arena.
"""
import json
from copy import deepcopy
from time import sleep
from typing import List, Dict, Any, Union

from src.api.j2l.pyrobotx.client import DefaultClientSettings
from src.api.j2l.pyrobotx.robot import RobotEvent
from src.server.manager_interface import IManager
from src.server.models import Player
from src.server.states.base import StateMachine
from src.server.states.end_game import EndGame
from src.server.states.in_game import InGame
from src.server.states.possible_states import StateEnum
from src.server.states.wait_players import WaitPlayers


class Gestionnaire(IManager):
    """
    This class is the manager of the arena. It handles the arena state machine and the arena events.
    Subclass of Agent that handles the connection to the server,
     and allows basic communication and control of the robot.
    """

    def __init__(self, nom, arene, username, password):
        """
        Constructor of the class Gestionnaire, subclass of Agent.
        :param nom: name of the robot : should be registered in a .dotenv file
        :param arene: name of the arena : should be registered in a .dotenv file
        :param username: username of the robot : should be registered in a .dotenv file
        :param password: password of the robot : should be registered in a .dotenv file
        """
        self.__TIME_LIMIT = 1000 * 60 * 3 + 1000 * 20  # 3minutes 20 seconds
        self.__start_time = 0
        self.__paused_time = 0
        self.__loop_start_time = 0
        self.__loop_end_time = 0

        print("Gestionnaire init")
        self.players: List[str] = []
        self._robot = super().__init__(nom, arene, username, password, server="mqtt.jusdeliens.com")
        print("Gestionnaire done super init")
        # define variables to retain information about the game
        self.__map: List[List[int]] = []
        self.__rules: Dict[str, Any] = {}
        self.__game_state = StateEnum.WAIT_PLAYERS  # initial state

        # define the state machine
        self.__state_machine = StateMachine()
        self.__state_machine.add_state(WaitPlayers(self))
        self.__state_machine.add_state(InGame(self))
        self.__state_machine.add_state(EndGame(self))
        self.__state_machine.set_actual_state(StateEnum.WAIT_PLAYERS)  # optional, since stateMachine starts at index 0
        print("Gestionnaire done init")

        # define the rules of the arena
        self.ruleArena("info", "🔴 Arène en cours de construction ")
        self.update()
        with open("rules.json", "r", encoding="utf-8") as json_file:
            self.__rules = json.load(json_file)
            self.set_rules(self.__rules)
        self.ruleArena("pause", True)
        self.ruleArena("reset", True)
        print("BEFORE", self.game)
        # change manager's State to wait for players
        self.ruleArena("info", "En attente des joueurs...")
        self.update()
        print("AFTER", self.game)
        self.robot.addEventListener(RobotEvent.robotConnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.robotDisconnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.updated, self.on_update)

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
        for player in self.__players:
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
        return len(self.__players) == self.__rules.get("nPlayers")

    @property
    def get_rules(self) -> Dict[str, Any]:
        return deepcopy(self.__rules)

    @property
    def __players(self) -> List[Player]:
        players_names: List[str] = self.players
        players: List[Player] = []
        p = None
        for player_name in players_names:
            try:
                p = self.get_player(player_name)
            except ValueError:
                p = Player(player_name)
            if p is not None:
                players.append(p)
        return players

    def game_loop(self):
        """
        This method is the main loop of the game.
        """
        print("Game loop started")
        self.__start_time = self.game['t']
        while self.game_running:
            self.__loop_start_time = self.game['t']
            self.update()
            self.__loop_end_time = self.game['t']
            sleep(1)

    def set_rules(self, rules: Dict[str, Any]) -> None:
        self.__rules = rules
        print(self)

    def set_pause(self, pause: bool) -> bool:
        self.ruleArena("pause", pause)
        self.update()
        return pause

    def set_map(self, game_map: List[List[int]]) -> bool:
        self.ruleArena("map", game_map)
        self.update()
        if self.get_rules["map"] == game_map:
            return True
        return False

    def get_player(self, player_id: Union[int | str]) -> Player:
        for player in self.players:
            if isinstance(player_id, int) and player.id == player_id \
                    or isinstance(player_id, str) and player == player_id:
                return player
        raise ValueError(f"Player {player_id} not found")

    def kill_player(self, player_id: int) -> Player:
        p = self.get_player(player_id)
        p.health = 0
        return p

    def register_player(self, player: Player) -> Player:
        p = self.get_player(player.id)
        if p is not None:
            return p
        self.__players.append(player)
        return player

    def unregister_player(self, player_id: int) -> None:
        p = self.get_player(player_id)
        self.__players.remove(p)

    def update_player_stats(self, player: Union[int | str]) -> Player:
        pass

    def update_players(self, *args, **kwargs) -> None:
        """
        This method on each update, gathers players from arena and update them internally.
        It also handles the players' events.
        """
        # get players from arena
        arena_players = self.players
        if arena_players is None:
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


if __name__ == '__main__':
    DefaultClientSettings.dtSleepUpdate = 100
    DefaultClientSettings.dtPing = 1000
    with Gestionnaire("...", "...", "...", "...") as gest:
        gest.game_loop()
