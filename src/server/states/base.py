"""
Define the BaseState class.

This class is the base class for all server side states.

It defines the methods that can be called by the server's EntityManager.
"""

import logging
from abc import abstractmethod, ABC

import root_config
from src.api.j2l.pyrobotx.robot import IRobot
from src.api.j2l.pytactx.agent import Agent


class State(ABC):
    """
    Base class for all server side states.
    """

    @abstractmethod
    def __init__(self, agent: Agent):
        self.agent: Agent = agent
        self.robot: IRobot = agent.robot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(root_config.LOGGING_LEVEL)
        self.logger.addHandler(logging.StreamHandler())

    @abstractmethod
    def __enter__(self):
        """
        Called when the state is entered.
        """

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when the state is exited.
        """

    @abstractmethod
    def on_player_event(self, event, value):
        """
        Called when an event is received.
        """

    @abstractmethod
    def on_arena_event(self, source, event, value):
        """
        Called when an arena event is received.
        """

    @abstractmethod
    def on_image(self, image):
        """
        Called when an image is received.
        """
