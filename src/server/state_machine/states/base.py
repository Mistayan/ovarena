"""
Define the BaseState class.

This class is the base class for all server side states.

It defines the methods that can be called by the server's EntityManager.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import root_config
from .possible_states import StateEnum
from src.server.manager_interface import IManager


class IState(ABC):
    """
    An IFace is an empty shell.
     Its only purpose is to define a standard structure for every children
      """

    @abstractmethod
    def handle(self):
        """ Abstract method to enforce children implementing this"""


class State(IState, ABC):
    """
    Base State class.
    defines standard actions for specific children states
    """
    __context: StateMachine

    @property
    @abstractmethod
    def name(self) -> StateEnum:
        """
        Return the Enum value of the state
        this should be implemented as a property
        """
        raise NotImplementedError

    def set_context(self, context: StateMachine):
        self.__context = context

    def switch_state(self, state: StateEnum):
        self.__context.set_actual_state(state)


class GameState(State, ABC):
    """
    Base State class.
    """

    def __init__(self, agent: IManager):
        super().__init__()
        self._agent = agent
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
