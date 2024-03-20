"""
State machine class.
It defines the states and the links between them.
When requesting to change state, it checks if the state is allowed
 to switch to the new state.
This is the main class of the state machine.
It uses the StateMachineConfig class to load the configuration from
 state_machine_config.json file.
"""
from __future__ import annotations

import json
import logging
import os
from importlib import import_module
from typing import List, Tuple, Dict

import root_config
from src.server.manager_interface import IManager
from src.server.state_machine.states import StateEnum, GameState


def dynamic_imp(package_name, class_name):
    """
    # find_module() method is used
    # to find the module and return
    # its description and path
    if found, otherwise
    # raise ImportError and return (None, None)
    """
    try:
        package = import_module(package_name)
        myclass = getattr(package, class_name)
        return package, myclass
    except ImportError as e:
        logging.error(e)
        raise ImportError(f"Error while importing {class_name} from {package_name}")


class StateMachine:
    """
    State machine class.
    It defines the states and the links between them.
    When requesting to change state, it checks if the state is allowed to switch to the new state.
    """

    def __init__(self, controller: IManager):
        """
        Initialize the state machine
        """
        if not isinstance(controller, IManager):
            raise TypeError(f"Controller must be a subclass of IManager, got {type(controller)}")
        self.__agent = controller
        self.__actual_state: StateEnum = None
        self.__states: Dict[str, GameState] = {}
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(root_config.LOGGING_LEVEL)
        self.__allowed_switches: Tuple[Tuple[StateEnum, StateEnum]] = tuple()
        self.__lock = False

    @property
    def state(self) -> str:
        """ return the actual state name """
        return self.__actual_state.name

    def __add_state(self, state: GameState.__class__):
        """
        Add a state to the state machine
        """

        state_object = state
        state_object.set_context(state_machine=self)
        if not isinstance(state_object, GameState):
            raise TypeError(f"State {state_object} is not a subclass of BaseState")
        self._logger.debug(f"Adding state {state.name} to states dict")
        self.__states.setdefault(state_object.name.name, state_object)

    def __define_states_links(self, connexions: List[Tuple[StateEnum, StateEnum]]):
        """
        Define the links between states.
        The tuple must be of the form :
        ( (state_from, state_to), (...) )
        """
        for connexion in connexions:
            self._logger.debug(connexion)
            if not isinstance(connexion, tuple):
                raise TypeError(f"Connexion {connexion} is not a tuple")
            if len(connexion) != 2:
                raise ValueError(f"Connexion {connexion} must be a tuple of size 2")
            if not isinstance(connexion[0], StateEnum):
                raise TypeError(f"Connexion {connexion} must be a tuple of StateEnum")
            if not isinstance(connexion[1], StateEnum):
                raise TypeError(f"Connexion {connexion} must be a tuple of StateEnum")
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

    def handle(self, *args):
        """Execute the actual state handle method
        Warning, once called it locks the state machine, thus preventing any change to the states
        """
        self.__lock = True
        self._logger.debug(f'Handling state : {self.__actual_state} with args {args}')
        self.__states[self.__actual_state.name].handle()

    def __is_allowed(self, new_state: StateEnum) -> bool:
        """
        returns True if the state is allowed to switch to the new state
        """
        if self.__actual_state is None:
            return True
        for state_from, state_to in self.__allowed_switches:
            if (self.__actual_state and
                    state_from.name == self.__actual_state.name and
                    state_to.name == new_state.name):
                return True
        return False

    def define_states(self, config: StateMachineConfig) -> StateMachine:
        """
        Initiate the state machine
        Set context to the agent
        Add states to the state machine
        Define the links between states
        """
        if self.__lock:
            raise RuntimeError("State machine is locked, cannot define states")
        if not isinstance(config, StateMachineConfig):
            raise TypeError("Config must be an instance of StateMachineConfig")

        for s in config.states:
            if not issubclass(s, GameState):
                raise ValueError(f"State {s} is not a subclass of GameState")
            self.__add_state(s(self.__agent))

        self.__define_states_links(config.links)
        init_state = config.initial_state
        if init_state and not isinstance(init_state, StateEnum):
            raise TypeError("Initial state must be an instance of StateEnum")

        self.set_actual_state(StateEnum(init_state))
        return self


class StateMachineConfig:
    """
    Define the configuration of the state machine
    """

    def __init__(self, path=None):
        """
        Load the configuration from the config.json file
        """
        if path is None or not isinstance(path, str):
            path = "state_machine_config.json"
        self.__states = []
        self.__links = []
        self.__initial_state = ""
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__logger.setLevel(root_config.LOGGING_LEVEL)
        self.__logger.debug("Loading state machine configuration")
        file_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(file_dir, path), "r", encoding="utf-8") as f:
            config = json.load(f)

        self.__set_states(config["states"])
        self.__set_links(config["links"])
        self.__set_initial_state(config["initial_state"])

    @property
    def states(self):
        """
        Return the states as a tuple
        """
        return tuple(self.__states)

    @states.setter
    def states(self, states: list):
        """
        Set the states
        """
        for s in states:
            if not isinstance(GameState.__class__, s):
                raise TypeError(f"State {s} is not a subclass of GameState")
        self.__set_states(states)

    @property
    def links(self):
        """
        Return the links between states as a list of tuples
        """
        return list(self.__links)

    @links.setter
    def links(self, links: list):
        """
        Set the links between states
        """
        for lnk1, lnk2 in links:
            if (not isinstance(StateEnum[lnk1], StateEnum)
                    or not isinstance(StateEnum[lnk2], StateEnum)):
                raise TypeError(f"Link {lnk1} -> {lnk2} is not a valid tuple of StateEnum")
        self.__set_links(links)

    @property
    def initial_state(self):
        """
        Return the initial state as a string
        """
        return self.__initial_state

    @initial_state.setter
    def initial_state(self, initial_state: str):
        """
        Set the initial state
        """
        if not isinstance(initial_state, str):
            raise TypeError("Initial state must be a string")
        self.__set_initial_state(initial_state)

    def __set_states(self, states: list) -> list:
        """
        import all desired states as class references and let the state machine instantiate them
        """
        self.__logger.debug("Setting states from src.server.state_machine.states ...")
        for enum_name in states:
            # import class from src.server.state_machine.states
            class_name = "".join([x.capitalize() for x in enum_name.split("_")])
            self.__logger.debug(f"Importing {class_name}")
            mod, state_class = dynamic_imp("src.server.state_machine.states", class_name)
            if not state_class or not mod or not issubclass(state_class, GameState):
                raise ValueError(f"State {class_name} not found")
            self.__states.append(state_class)
        self.__logger.info(f"Imported {self.__states}")
        return states

    def __set_links(self, links: list) -> None:
        """
        Set the links between states
        """
        # import enum, then load the enum value from the string

        self.__logger.debug("Setting links")
        for lnk1, lnk2 in links:
            self.__links.append((StateEnum[lnk1], StateEnum[lnk2]))
        self.__logger.info(f"allowing transitions for {self.__links}")

    def __set_initial_state(self, initial_state: str):
        """
        Set the initial state
        """
        # import enum, then load the enum value from the string
        self.__logger.debug(f"Setting initial state to {initial_state}")
        self.__initial_state = StateEnum[initial_state]
