"""
Define the BaseState class.

This class is the base class for all server side states.

It defines the methods that can be called by the server's EntityManager.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import root_config
from src.server.manager_interface import IManager
from .possible_states import StateEnum


class IState(ABC):
    """
    An IFace is an empty shell.
     Its only purpose is to define a standard structure for every children
      """

    @property
    @abstractmethod
    def name(self) -> StateEnum:
        """
        Return the Enum value of the state
        this should be implemented as a property
        """

    @abstractmethod
    def handle(self):
        """ Abstract method to enforce children implementing this"""


class State(IState, ABC):
    """
    Base State class.
    defines standard actions for specific children states
    """

    def __init__(self):
        """
        Initialize the state
        """
        super().__init__()
        self.__context = None

    def set_context(self, state_machine):
        """
        define the context of the state, that is the state machine
        """
        self.__context = state_machine

    def switch_state(self, state: StateEnum):
        """
        Asks the context to switch to the given state,
        if the switch is allowed
        """
        self.__context.set_actual_state(state)


class GameState(State, ABC):
    """
    Base State class.
    """

    def __init__(self, manager: IManager):
        super().__init__()
        self._manager = manager
        self._logger = logging.getLogger(self.__class__.__name__ + f" : {self.name.name}")
        self._logger.setLevel(root_config.LOGGING_LEVEL)

    def handle(self):
        self._logger.debug(f"(Child) handled : {self.name.name}")
        self._on_handle()

    @abstractmethod
    def _on_handle(self):
        """
        This method is called by the handle method.
        It must be implemented by the children to reflect the state's behavior.
        - WARNING :
        get the manager's wanted value on entering this method,
         to avoid calling the property twice and risk
         getting a different value (async issues)
        ie :
        all_connected = self._agent.all_players_connected
        ... do stuff with all_connected
        """
