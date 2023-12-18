"""
Define the BaseState class.

This class is the base class for all server side states.

It defines the methods that can be called by the server's EntityManager.
"""

from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from typing import List

import root_config
from src.server.manager_interface import IManager
from src.server.states.possible_states import StateEnum


class IState(ABC):
    """ An IFace is an empty shell. Its only purpose is to define a standard structure for every children """

    @abstractmethod
    def handle(self):
        """ Abstract method to enforce children implementing this"""
        ...


class State(IState, ABC):
    """
    Base State class.
    defines standard actions for specific children states
    """

    @abstractmethod
    def __init__(self):
        self.__context: StateMachine = None

    @property
    @abstractmethod
    def name(self) -> StateEnum:
        """
        Return the Enum value of the state
        this should be implemented as a property
        """
        raise NotImplementedError

    def set_context(self, context):
        self.__context = context

    def switch_state(self, state: StateEnum):
        self.__context.set_actual_state(state)


class BaseState(State):

    def __init__(self, agent: IManager):
        super().__init__()
        self._agent = agent
        self._logger = logging.getLogger(self.__class__.__name__ + f" : {self._agent.robot.name}")
        self._logger.setLevel(root_config.LOGGING_LEVEL)

    def handle(self):
        self._on_handle()

    @abstractmethod
    def _on_handle(self):
        """
        This method is called by the handle method.
        It must be implemented by the children to reflect the state's behavior.
        - WARNING :
        get the manager's wanted value on entering this method, to avoid calling the property twice and risk
        getting a different value (async issues)
        ie :
        all_connected = self._agent.all_players_connected
        ... do stuff with all_connected
        """
        ...


class StateMachine:

    def __init__(self):
        self.__actual_state: int = 0
        self.__states: List[BaseState] = []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)

    def add_state(self, state: BaseState):
        if not isinstance(state, BaseState):
            raise TypeError(f"state must be of type BaseState, got {type(state)}")
        self._logger.debug(f"Adding state {state} at {len(self.__states)} : {state.name}")
        state.set_context(self)
        self.__states.append(state)

    def set_actual_state(self, state: StateEnum):
        self._logger.debug(f"Setting actual state to {state}")
        self.__actual_state = state.value

    def handle(self):
        """Execute the actual state handle method"""
        self._logger.debug(f'Handling state : {self.__actual_state}')
        self.__states[self.__actual_state].handle()
