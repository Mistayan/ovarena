"""
Test Manager Unit Tests
"""
import unittest
from copy import copy
from unittest.mock import Mock

# from j2L, Mock Agent library
from src.api.j2l.pytactx.agent import Agent
from src.server.arena_manager import ArenaManager

Agent = Mock(Agent)


class TestManager(unittest.TestCase):
    """
    Test the manager without connecting to the server
    """

    def __new_test_agent(self, init_dict):
        """
        Create a mock Agent, with predefined behavior for the test
        """
        # Create a mock Agent, with predefined behavior for the test
        fake_agent = Mock(Agent.__class__)
        fake_agent.game = copy(init_dict)
        fake_agent.players = ["p1"]
        # when agent.ruleArena is called, update the game dict
        fake_agent.ruleArena = lambda k, v: fake_agent.game.update({k: v})
        return fake_agent

    def test_init_manager_ko(self):
        """
        Test that the manager cannot be initialized with a non Agent object
        """
        with self.assertRaises(TypeError):
            ArenaManager("not an agent")

    def test_str_manager(self):
        """
        Test that the manager can be printed as a string
        """
        init_game = {'t': 0}
        fake_agent = self.__new_test_agent(init_game)

        # Create an instance of ArenaManager with the mock Agent
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        assert str(arena_manager) == "Manager"

    def test_game_init_ok(self):
        """
        Test that the game is correctly initialized
        """
        init_game = {'t': 0}
        fake_agent = self.__new_test_agent(init_game)

        # Create an instance of ArenaManager with the mock Agent
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        assert arena_manager._robot == fake_agent
        assert arena_manager._robot.game != init_game
        assert arena_manager._robot.game['pause'] is True
        assert arena_manager._robot.game['t'] == 0
        assert arena_manager.state == 'WAIT_PLAYERS_CONNEXION'

    def test_player_just_logged_in_arena_open(self):
        """
        Test that a player that just logged in is registered
        """
        init_game = {'t': 0}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        # simulate a player just logged in
        fake_agent.players = ["p1"]
        # simulate server sent response event
        arena_manager.on_update(None, "event", "p1")

        assert arena_manager.state == 'WAIT_PLAYERS_CONNEXION'
        assert len(arena_manager.registered_players) == 1
        fake_agent.players = ["p1", "p2"]
        arena_manager.on_update(None, "event", "p2")
        assert arena_manager.state == 'WAIT_GAME_START'
        assert len(arena_manager.registered_players) == 2
        print(arena_manager.registered_players)

    def test_player_just_logged_in_arena_closed(self):
        """ Not implemented yet """
        pass

    def test_player_just_logged_out(self):
        """
        Test that a player that just logged out is still registered
        and the game is waiting for him to reconnect
        """
        init_game = {'t': 0, 'pause': True}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        # simulate a player just logged in
        assert arena_manager.all_players_connected is False

        fake_agent.players = ["p1", "p2"]
        # simulate server sent response event
        arena_manager.on_update(None, "event", "p1, p2")
        assert arena_manager.all_players_connected is True
        assert arena_manager.state == 'WAIT_GAME_START'
        assert len(arena_manager.registered_players) == 2

        arena_manager.on_update(None, "event", None)
        assert arena_manager.state == 'IN_GAME'
        fake_agent.players = ["p1"]
        arena_manager.on_update(None, "event", "p1")
        assert arena_manager.all_players_connected is False

        # player is still registered, and game is waiting for him to reconnect
        assert len(arena_manager.registered_players) == 2
        assert arena_manager.state == 'WAIT_PLAYERS'
        print(arena_manager.registered_players)

    def test_kill_players_should_end_game_loop(self):
        """
        Test that a player can be killed by the manager
        """
        init_game = {'t': -1, 'pause': True}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        fake_agent.players = ["p1", "p2"]
        # simulate players just logged in
        arena_manager.on_update(None, "event", "p1, p2")
        assert len(arena_manager.registered_players) == 2
        assert arena_manager.game_loop_running is True
        print(arena_manager.registered_players)
        arena_manager.kill_player("p1")
        arena_manager.kill_player("p2")
        print(arena_manager.registered_players)
        assert arena_manager.game_loop_running is False

    def test_unregister_player(self):
        init_game = {'t': -1, 'pause': True}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        fake_agent.players = ["p1", "p2"]
        arena_manager.on_update(None, "event", "p1, p2")
        # player p1 has been caught cheating, unregister him
        arena_manager.unregister_player("p1")
        assert len(arena_manager.registered_players) == 1
        assert arena_manager.state == 'WAIT_GAME_START'
        print(arena_manager.registered_players)

    # disable this test for now, as it is not implemented yet
    @unittest.skip
    def test_set_map(self):
        """
        Test that the map can be set
        """
        init_game = {'t': -1, 'pause': True, 'map': [[0, 1, 0], [0, 1, 0], [0, 0, 1]]}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        fake_agent.players = ["p1", "p2"]
        arena_manager.on_update(None, "event", "p1, p2")
        arena_manager.set_map([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        assert arena_manager.state == 'WAIT_PLAYERS'
        assert arena_manager._robot.game['map'] == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def test_set_pause_during_game_unpause(self):
        """
        Test that the game can be paused
        """
        init_game = {'t': -1, 'pause': True}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        fake_agent.players = ["p1", "p2"]
        arena_manager.on_update(None, "event", "p1, p2")

    def test_set_rules(self):
        """
        Test that the rules can be set
        """
        init_game = {'t': -1, 'pause': True}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        fake_agent.players = ["p1", "p2"]
        arena_manager.on_update(None, "event", "p1, p2")
        arena_manager.mod_game('t', 0)
        assert arena_manager.state == 'WAIT_GAME_START'
        assert arena_manager._robot.game['t'] == 0

    # Skiped, because of while loop
    @unittest.skip
    def test_game_loop(self):
        """
        Test that the game loop is functional
        """
        init_game = {'t': -1, 'pause': True}
        fake_agent = self.__new_test_agent(init_game)
        arena_manager = ArenaManager(fake_agent)
        arena_manager._robot = fake_agent
        fake_agent.players = ["p1", "p2"]
        arena_manager.on_update(None, "event", "p1, p2")
        # start the game loop, with predefined game duration
        arena_manager.game_loop()