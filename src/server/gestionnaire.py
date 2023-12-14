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
        super().__init__(nom, arene, username, password, server="mqtt.jusdeliens.com")

        self.__players: List[Player] = []
        self.__map: List[List[int]] = []
        self.__rules: Dict[str, Any] = {}
        self.__game_state = "wait"
        self.__game_states = {
            "wait": self.wait_all_players,
            "start": self.start_game,
            "end": self.end_game
        }
        self.ruleArena("info", "🔴 Arène en cours de construction ")
        with open("rules.json", "r", encoding="utf-8") as json_file:
            self.__rules = json.load(json_file)
            self.set_rules(self.__rules)
        self.ruleArena("pause", True)
        self.ruleArena("reset", True)
        print(self.get_rules)
        # change manager's State to wait for players
        self.ruleArena("info", "En attente des joueurs...")
        self.update()
        self.robot.addEventListener(RobotEvent.robotConnected, self.wait_all_players)
        self.robot.addEventListener(RobotEvent.robotDisconnected, self.wait_all_players)
        # TODO : ADD THIS LINE TO EACH MANAGER_STATES !
        # self.robot.addEventListener(RobotEvent.updated, self.__game_states[self.__game_state])

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

    @property
    def get_rules(self) -> Dict[str, Any]:
        return deepcopy(self.__rules)

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

    def update_player(self, player: Player) -> Player:
        p = self.get_player(player.id)
        p.health = player.health
        p.inventory = player.inventory
        p.x = player.x
        p.y = player.y
        p.direction = player.direction
        p.score = player.score
        p.known_map = player.known_map
        return p

    @property
    def all_players_connected(self) -> bool:
        """ return True if all players are connected """
        return len(self.players) == self.__rules["nbJoueurs"]

    def wait_all_players(self, *args, **kwargs) -> None:
        """
        This method is called when a player connects or disconnects.
        """

        # Handle events
        if not self.all_players_connected:
            self.ruleArena("pause", True)
            self.ruleArena("info", "En attente des joueurs...")
            self.update()
        else:
            self.ruleArena("pause", False)
            self.ruleArena("info", "🟢 C'est parti !")

    def start_game(self, *args, **kwargs) -> bool:
        """
        This method is called when the game starts.
        """
        self.ruleArena("info", "🟢 Que le meilleur gagne !")
        self.ruleArena("pause", False)
        self.update()
        if self.get_rules["info"] == "🟢 Que le meilleur gagne !":
            return True
        return False

    def end_game(self, *args, **kwargs):
        """
        This method is called when the game ends.
        """
        self.ruleArena("info", "🔴 Fin de la partie !")
        self.ruleArena("pause", True)
        self.update()
        if self.get_rules["info"] == "🔴 Fin de la partie !":
            return True
        return False

    def update_players(self, *args, **kwargs) -> None:
        """
        This method is called when a player updates.
        """
        pass  # TODO : implement game logic

    def __str__(self):
        return "Gestionnaire"


if __name__ == '__main__':
    DefaultClientSettings.dtSleepUpdate = 100
    DefaultClientSettings.dtPing = 1000
    pass
