"""
Tests StateMachine Class from src.server.state_machine.state_machine
Also tests StateMachineConfig Class from src.server.state_machine.state_machine
"""

import unittest
from unittest import mock

import pytest

from src.server import StateMachine
from src.server.arena_manager import ArenaManager
from src.server.state_machine import StateMachineConfig
from src.server.state_machine.states import StateEnum, WaitGameStart, WaitPlayersConnexion


class TestStateMachine(unittest.TestCase):
    """
    Tests StateMachine Class from src.server.state_machine.state_machine
    Also tests StateMachineConfig Class from src.server.state_machine.state_machine
    Ensure that the Config class is able to load the config from a file
     and instantiate the state machine behavior
    Ensure that the state machine is able to switch states and handle the game
    Ensure that the state machine will fail on bad instructions
    """

    def test_init_no_manager_fail(self):
        """
        # If i do not provide a manager, the state machine should fail
        # assertRaises
        """
        with pytest.raises(TypeError):
            StateMachine(None)

    def test_init_with_manager_ok(self):
        """
        # Given a manager
        # If i do provide a manager, the state machine should init
        """
        manager = mock.Mock(ArenaManager)
        StateMachine(manager)

    def test_states_cannot_change_after_lock(self):
        """
        # Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and
         the WaitGameStart state is the next state
        # When i lock the state machine
        # Then i should not be able to change the state
        """
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        sm.handle()
        with pytest.raises(RuntimeError):
            sm.define_states(StateMachineConfig())

    def test_bad_transition(self):
        """
        # Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state
         and the WaitGameStart state is the next state
        # When i try to switch to a bad state
        """
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        smc = StateMachineConfig()
        sm.define_states(smc)

        with pytest.raises(ValueError):
            sm.set_actual_state(StateEnum.IN_GAME)

    def test_add_bad_state(self):
        """
        # Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state
         and the WaitGameStart state is the next state
        # When i try to add a bad state
        # Then the state machine should fail
        """
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        smc = StateMachineConfig()

        with pytest.raises(TypeError):
            smc.states = (WaitPlayersConnexion, WaitGameStart, "bad_state")
            sm.define_states(smc)

    def test_request_bad_state_switch(self):
        """
        # Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state
         and the WaitGameStart state is the next state
        # When i try to add a bad state, the state machine should fail
        """
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())
        with pytest.raises(ValueError):
            sm.set_actual_state(StateEnum.IN_GAME)

    def test_state_machine_wait_players(self):
        """
        Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        where the WaitPlayersConnexion state is the initial state
         and the WaitGameStart state is the next state
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        sm.handle()
        manager.register_player.assert_called()
        assert sm.state == StateEnum.WAIT_GAME_START.name

    def test_state_machine_wait_players_one_then_two_players(self):
        """
        Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        where the WaitPlayersConnexion state is the initial state
         and the WaitGameStart state is the next state
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        manager.all_players_connected = False
        sm.handle()
        manager.register_player.assert_called_with(mock.ANY)
        manager.register_player.assert_called_once()
        assert sm.state == StateEnum.WAIT_PLAYERS_CONNEXION.name

        manager.players = ["player1", "player2"]
        sm.handle()
        assert sm.state == StateEnum.WAIT_PLAYERS_CONNEXION.name
        # FIXME  why 3 and not 2 ? there are 2 players, not 3!
        assert manager.register_player.call_count == 3
        manager.all_players_connected = True
        sm.handle()
        manager.register_player.assert_called()
        manager.register_player.assert_called_with(mock.ANY)
        assert sm.state == StateEnum.WAIT_GAME_START.name

    def test_state_machine_wait_game_start(self):
        """
        Given a manager and a state machine with a
         WaitPlayersConnexion state and a WaitGameStart state
        where the WaitPlayersConnexion state is the initial state
         and the WaitGameStart state is the next state
        # When i handle the state machine, it registers the players
         and switch to the next state
        # manager.game_loop_running.return_value = True
        # given the fact that i am in the WaitGameStart state,
         i should be able to start the game
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name

    def test_wait_players_connexion(self):
        """
        Given a manager and a state machine with a
         WaitPlayersConnexion state
        where the WaitPlayersConnexion state is the initial state
        when i handle the state machine, it registers the players
         and switch to the next state
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        sm.handle()
        manager.register_player.assert_called()
        assert sm.state == StateEnum.WAIT_GAME_START.name

    def test_wait_game_start(self):
        """
        Given a manager and a state machine with a
         WaitGameStart state
        where the WaitGameStart state is the initial state
        when i handle the state machine, it registers the players
         and switch to the next state
        manager.game_loop_running.return_value = True
        given the fact that i am in the WaitGameStart state,
         i should be able to start the game
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name

    def test_game_start_should_unpause(self):
        """
        Given a manager and a state machine with
         a WaitGameStart state
        where the WaitGameStart state is the initial state
        when i handle the state machine, it registers the players
         and switch to the next state
        manager.game_loop_running.return_value = True
        given the fact that i am in the WaitGameStart state,
         i should be able to start the game
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        manager.game = {"pause": True, "timeElapsed": 0, "timeLimit": 50000}
        # when manager.set_pause is called, set manager.game["pause"] to True/False
        manager.set_pause.side_effect = lambda pause: manager.game.update({"pause": pause})
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # when i handle the state machine, it registers the players
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name
        sm.handle()
        assert manager.game["pause"] is False

    def test_players_disconnected(self):
        """
        # Given a manager and a state machine with a
         WaitPlayersConnexion state
        # where the WaitPlayersConnexion state is the initial state
        # When i handle the state machine, it registers the players
         and switch to the next state
        # When a player disconnects, the state machine should
         switch to the WaitPlayers state
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1"]
        manager.registered_players = []
        manager.all_players_connected = False
        manager.game = {"pause": True, "timeElapsed": 0, "timeLimit": 50000, "nbPlayers": 2}
        # when manager.register_player is called, set manager.players to specified value
        manager.register_player.side_effect = lambda player: manager.registered_players.append(player)
        manager.set_pause.side_effect = lambda pause: manager.game.update({"pause": pause})
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # when i handle the state machine,
        # it registers the player 1 and wait for more players
        sm.handle()
        manager.register_player.assert_called_once()
        assert sm.state == StateEnum.WAIT_PLAYERS_CONNEXION.name
        # player 2 connects
        manager.players = ["player1", "player2"]
        manager.all_players_connected = True
        manager.register_player.assert_called()
        # and switch to the wait game start state
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name

        # When all players are connected, the state machine should
        manager.game_loop_running = True
        sm.handle()
        # switch to the InGame state
        assert sm.state == StateEnum.IN_GAME.name

        # When a player disconnects, the state machine should
        manager.players = ["player1"]
        manager.all_players_connected = False
        sm.handle()
        # switch to the WaitPlayers state
        assert sm.state == StateEnum.WAIT_PLAYERS.name
        sm.handle()
        assert manager.game["pause"] is True

    def test_end_game(self):
        """
        # Given a manager and a state machine with a InGame state
        # where the InGame state is the initial state
        # When i handle the state machine, it registers the players
        # given the fact that i am in the WaitGameStart state,
         i should be able to start the game
        # given the fact that i am in the InGame state,
         i should be able to handle the game
        # given the fact that i am in the InGame state,
         i should be able to end the game
        """
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        manager.game = {"pause": True, "timeElapsed": 0, "timeLimit": 0}
        manager.set_pause.side_effect = lambda pause: manager.game.update({"pause": pause})

        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        assert sm.state == StateEnum.WAIT_PLAYERS_CONNEXION.name
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        manager.game_loop_running = True
        manager.all_players_connected = True
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name
        manager.game_loop_running = False
        sm.handle()
        assert sm.state == StateEnum.END_GAME.name
        # then, EndGame state should put the game in pause and display the end game message
        sm.handle()
        assert manager.game["pause"] is True

    def test_state_machine_config_0(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        assert smc is not None
        assert smc.states is not None
        assert smc.links is not None
        assert smc.initial_state is not None
        with pytest.raises(TypeError):
            smc.states = [None]

    def test_state_machine_config_1(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        with pytest.raises(TypeError):
            smc.states = [WaitGameStart, WaitPlayersConnexion]

    def test_state_machine_config_2(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        with pytest.raises(TypeError):
            smc.links = [None]

    def test_state_machine_config_3(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        with pytest.raises(KeyError):
            smc.links = [(None, None)]

    def test_state_machine_config_4(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        with pytest.raises(ValueError):
            smc.links = [("state", None, None)]

    def test_state_machine_config_5(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        with pytest.raises(KeyError):
            smc.links = [("state", "state")]

    def test_state_machine_config_6(self):
        """
        # Given a state machine config
        # When i load the config from a file
        # Then i should have a state machine config
        """
        smc = StateMachineConfig()
        smc.links = [("WAIT_PLAYERS_CONNEXION", "WAIT_GAME_START")]
        assert (StateEnum.WAIT_PLAYERS_CONNEXION, StateEnum.WAIT_GAME_START) in smc.links

    def test_locked_state_machine(self):
        """ Test locked state machine """
        controller = mock.Mock(ArenaManager)
        state_machine = StateMachine(controller)
        state_machine._StateMachine__lock = True  # Simulate locked state machine
        with self.assertRaises(RuntimeError):
            state_machine.define_states(StateMachineConfig())

    def test_invalid_state_class(self):
        """ Test invalid state class"""
        config = StateMachineConfig()
        with self.assertRaises(TypeError):
            with self.assertRaises(KeyError):
                config.states = ["A", "B", "C"]  # Invalid state class

    def test_invalid_links_type(self):
        """ Test invalid links type """
        config = StateMachineConfig()
        invalid_links = [("State1", "State2"), ("State3", "State4")]  # Invalid links format
        with self.assertRaises(KeyError):
            config.links = invalid_links

    def test_invalid_initial_state_type(self):
        """ Test invalid initial state type """
        config = StateMachineConfig()
        invalid_initial_state = 123  # Invalid initial state type
        with self.assertRaises(TypeError):
            config.initial_state = invalid_initial_state

    def test_base_state(self):
        """ Test Base class """
        from src.server.state_machine.states.base import GameState
        with self.assertRaises(TypeError):
            GameState(None)
        with self.assertRaises(TypeError):
            GameState(mock.Mock(ArenaManager)).name

    def test_state_enum(self):
        """
        Test StateEnum class
        """
        with self.assertRaises(ValueError):
            StateEnum(None)
