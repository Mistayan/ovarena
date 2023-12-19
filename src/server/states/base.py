"""
Define the BaseState class.

This class is the base class for all server side states.

It defines the methods that can be called by the server's EntityManager.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import List, Tuple

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

    def set_context(self, context: StateMachine):
        self.__context = context

    def switch_state(self, state: StateEnum):
        self.__context.set_actual_state(state)


class BaseState(State):

    def __init__(self, agent: IManager):
        super().__init__()
        self._agent = agent
        self._logger = logging.getLogger(self.__class__.__name__ + f" : {self.name.name}")
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

    def __init__(self, controller: IManager):
        self.__agent = controller
        self.__actual_state: StateEnum = None
        self.__states: List[BaseState] = []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(root_config.LOGGING_LEVEL)
        self.__allowed_switches: Tuple[Tuple[StateEnum, StateEnum]] = tuple()

    def add_state(self, state: BaseState.__class__):
        self._logger.debug(f"Adding state {state} at {len(self.__states)} : {state.name}")
        state_object = state(self.__agent)
        state_object.set_context(context=self)
        if not isinstance(state_object, BaseState):
            raise TypeError(f"State {state_object} is not a subclass of BaseState")
        self.__states.append(state_object)
        self._logger.debug(f"New state list : {self.__states}")

    def define_states_links(self, connexions: List[Tuple[StateEnum, StateEnum]]):
        """
        Define the links between states.
        The tuple must be of the form :
        ( (state_from, state_to), (...) )
        """
        self.__allowed_switches = connexions

    def set_actual_state(self, requested_state: StateEnum):
        """
        Switch the actual state to the given state
        If the state is not in the list, raise an error (should not happen)
        If the state is already the actual state, do nothing (should not happen)
        If the state we switch to is not in the connexions list, raise an error
        """
        self._logger.debug(f"Requested change state to {requested_state.name}")
        if not self.__is_allowed(requested_state):
            raise ValueError(f"State {self.__actual_state.name} "
                             f"is not allowed to switch to {requested_state.name}")
        self.__actual_state = requested_state

    def handle(self):
        """Execute the actual state handle method"""
        self._logger.debug(f'Handling state : {self.__actual_state}')
        self.__states[self.__actual_state.value].handle()

    def __is_allowed(self, new_state: StateEnum) -> bool:
        """
        returns True if the state is allowed to switch to the new state
        """
        if self.__actual_state is None:
            return True
        for state_from, state_to in self.__allowed_switches:
            self._logger.debug("Checking from state : " + str(state_from.name) + " to " + str(state_to.name))
            if self.__actual_state and state_from.name == self.__actual_state.name and state_to.name == new_state.name:
                return True
        return False
