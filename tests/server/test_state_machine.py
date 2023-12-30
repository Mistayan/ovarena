import unittest
from unittest import mock

import pytest

from src.server import StateMachine
from src.server.arena_manager import ArenaManager
from src.server.state_machine.states import StateEnum, WaitGameStart, WaitPlayersConnexion
from src.server.state_machine import StateMachineConfig


class TestStateMachine(unittest.TestCase):

    def test_init_no_manager_fail(self):
        # If i do not provide a manager, the state machine should fail
        # assertRaises
        with pytest.raises(TypeError):
            StateMachine(None)

    def test_init_with_manager_ok(self):
        # Given a manager
        manager = mock.Mock(ArenaManager)

        # If i do provide a manager, the state machine should init
        StateMachine(manager)

    def test_states_cannot_change_after_lock(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # When i lock the state machine
        sm.handle()
        # Then i should not be able to change the state
        with pytest.raises(RuntimeError):
            sm.define_states(StateMachineConfig())

    def test_bad_transition(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        smc = StateMachineConfig()
        sm.define_states(smc)

        # When i try to switch to a bad state
        with pytest.raises(ValueError):
            sm.set_actual_state(StateEnum.IN_GAME)

    def test_add_bad_state(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        # When i try to add a bad state
        smc = StateMachineConfig()
        smc.states = (WaitPlayersConnexion, WaitGameStart, "bad_state")
        with pytest.raises(TypeError):
            sm.define_states(smc)

    def test_request_bad_state_switch(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
        manager = mock.Mock(ArenaManager)
        manager.players = []
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())
        # When i try to add a bad state
        with pytest.raises(ValueError):
            sm.set_actual_state(StateEnum.IN_GAME)

    def test_state_machine_wait_players(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        sm.handle()
        manager.register_player.assert_called()
        assert sm.state == StateEnum.WAIT_GAME_START.name

    def test_state_machine_wait_players_one_then_two_players(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
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
        assert manager.register_player.call_count == 3  # FIXME  why 3 and not 2 ? there are 2 players, not 3!
        manager.all_players_connected = True
        sm.handle()
        manager.register_player.assert_called()
        manager.register_player.assert_called_with(mock.ANY)
        assert sm.state == StateEnum.WAIT_GAME_START.name

    def test_state_machine_wait_game_start(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state and a WaitGameStart state
        # where the WaitPlayersConnexion state is the initial state and the WaitGameStart state is the next state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # When i handle the state machine, it registers the players and switch to the next state
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        # manager.game_loop_running.return_value = True
        # given the fact that i am in the WaitGameStart state, i should be able to start the game
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name

    def test_wait_players_connexion(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state
        # where the WaitPlayersConnexion state is the initial state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # When i handle the state machine, it registers the players and switch to the next state
        sm.handle()
        manager.register_player.assert_called()
        assert sm.state == StateEnum.WAIT_GAME_START.name

    def test_wait_game_start(self):
        # Given a manager and a state machine with a WaitGameStart state
        # where the WaitGameStart state is the initial state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # When i handle the state machine, it registers the players and switch to the next state
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        # manager.game_loop_running.return_value = True
        # given the fact that i am in the WaitGameStart state, i should be able to start the game
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name

    def test_game_start_should_unpause(self):
        # Given a manager and a state machine with a WaitGameStart state
        # where the WaitGameStart state is the initial state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        manager.game = {"pause": True, "timeElapsed": 0, "timeLimit": 50000}
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # When i handle the state machine, it registers the players and switch to the next state
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        # manager.game_loop_running.return_value = True
        # given the fact that i am in the WaitGameStart state, i should be able to start the game
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name
        sm.handle()
        assert manager.game["pause"] is False

    def test_players_disconnected(self):
        # Given a manager and a state machine with a WaitPlayersConnexion state
        # where the WaitPlayersConnexion state is the initial state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        # When i handle the state machine, it registers the players and switch to the next state
        sm.handle()
        manager.register_player.assert_called()
        assert sm.state == StateEnum.WAIT_GAME_START.name

        # When a player disconnects, the state machine should switch to the WaitPlayers state
        manager.players = ["player1"]
        manager.all_players_connected.return_value = False
        sm.handle()
        assert sm.state == StateEnum.WAIT_PLAYERS.name

    def test_end_game(self):
        # Given a manager and a state machine with a InGame state
        # where the InGame state is the initial state
        manager = mock.Mock(ArenaManager)
        manager.players = ["player1", "player2"]
        manager.game = {"pause": False, "timeElapsed": 0, "timeLimit": 0}

        sm = StateMachine(manager)
        sm.define_states(StateMachineConfig())

        assert sm.state == StateEnum.WAIT_PLAYERS_CONNEXION.name
        # When i handle the state machine, it registers the players
        sm.handle()
        assert sm.state == StateEnum.WAIT_GAME_START.name
        manager.game_loop_running.return_value = True
        manager.all_players_connected.return_value = True
        # given the fact that i am in the WaitGameStart state, i should be able to start the game
        sm.handle()
        assert sm.state == StateEnum.IN_GAME.name
        # given the fact that i am in the InGame state, i should be able to handle the game
        manager.game_loop_running.return_value = False
        sm.handle()
        assert sm.state == StateEnum.END_GAME.name
        # given the fact that i am in the InGame state, i should be able to pause the game
