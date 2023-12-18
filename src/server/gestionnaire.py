"""
Game manager of the arena.
Watch the arena state machine and the arena events.
Apply the rules of the arena.
"""
import json
from copy import deepcopy
from time import sleep
from typing import List, Dict, Any

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
        print("Gestionnaire init")
        self.players: List[Player] = []
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
        print(self.get_rules)
        # change manager's State to wait for players
        self.ruleArena("info", "En attente des joueurs...")
        self.update()
        self.robot.addEventListener(RobotEvent.robotConnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.robotDisconnected, self.__state_machine.handle)
        self.robot.addEventListener(RobotEvent.updated, self.on_update)

    def on_update(self) -> None:
        """
        On each update, the manager checks the arena state machine and the arena events.
        For each player, it updates the player's state machine and the player's events.
        """
        # Let curent state handle the update and
        self.__game_state.handle()

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
        return self.game["timeElapsed"] <= self.game["timeLimit"]

    @property
    def game_running(self) -> bool:
        """
        Return False if the game time is elapsed or all players are dead.
        """
        return self.__timer_running or self.__all_players_dead

    @property
    def all_players_connected(self) -> bool:
        """ return True if all players are connected """
        return len(self.__players) == self.__rules["nbJoueurs"]

    @property
    def get_rules(self) -> Dict[str, Any]:
        return deepcopy(self.__rules)

    @property
    def __players(self) -> List[Player]:
        return self.__players

    def game_loop(self):
        """
        This method is the main loop of the game.
        """
        print("Game loop started")
        while True:
            sleep(0.1)
            self.update()

    def set_rules(self, rules: Dict[str, Any]) -> None:
        self.__rules = rules
        self.robot.game("game", self.__rules)

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

    def get_player(self, player_id: int) -> Player:
        for player in self.__players:
            if player.id == player_id:
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

    def update_player_stats(self, player: Player) -> Player:
        p = self.get_player(player.id)
        p.health = player.health
        p.inventory = player.inventory
        p.x = player.x
        p.y = player.y
        p.direction = player.direction
        p.score = player.score
        p.known_map = player.known_map
        return p

    def update_players(self, *args, **kwargs) -> None:
        """
        This method on each update, gathers players from arena and update them internally.
        It also handles the players' events.
        """
        # get players from arena
        arena_players = self.robot.game("players", None)
        if arena_players is None:
            raise ValueError("No players found in arena")
        # update players
        for arena_player in arena_players:
            player = self.get_player(arena_player["id"])
            self.update_player_stats(player)
            # handle player events
            if player.health <= 0:
                player.set_position(0, 0)
            # TODO : HANDLE OTHER EVENTS

    def __str__(self):
        return "Gestionnaire"

    def display(self, message: str) -> None:
        """
        Display a message on the arena.
        :param message: the message to display
        """
        self.ruleArena("info", message)


if __name__ == '__main__':
    DefaultClientSettings.dtSleepUpdate = 100
    DefaultClientSettings.dtPing = 1000
    with Gestionnaire("...", "...", "...", "...") as gest:
        gest.game_loop()
