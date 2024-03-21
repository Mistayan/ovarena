"""
Synchronisation class
"""
import logging
import time
from typing import Any

from src.api.j2l.pytactx.agent import Agent


class SyncAgent(Agent):
    """
    Handles event from agent and copy callbacks to Manager
    """

    def __init__(self, user, arena, login, password, server, port):
        self.__logger = logging.getLogger("ArenaAgent")
        self.__context = None
        super().__init__(user, arena, login, password, server, port)

    def set_context(self, context):
        from .arena_manager import ArenaManager
        if not isinstance(context, ArenaManager):
            raise TypeError("Context must be an ArenaManager")
        self.__logger.info("Setting context")
        self.__context = context

    # def update(self, enableSleep=True) -> None:
    #     """
    #     Update the agent.
    #     :param enableSleep: enable sleep after update
    #     """
    #     self.__logger.info("Updating agent")
    #     super().update(enableSleep)
    #     self.__logger.info("Agent updated")

    def _onArenaChanged(self, eventSrc: Any, eventName: str, arenaState: dict[str, Any]):
        self.__logger.info(f"{eventName} : {arenaState}")
        super()._onArenaChanged(eventSrc, eventName, arenaState)
        if self.__context:
            self.__context._on_update(eventSrc, eventName, arenaState)

    # def _onUpdated(self, eventSrc: Any, eventName: str, gameState: dict[str, Any]):
    #     self.__logger.info(f"{eventName} : {gameState}")
    #     super()._onUpdated(eventSrc, eventName, gameState)
    #     if self.__context:
    #         self.__context._on_update(eventSrc, eventName, gameState)
    #
    # def _onPlayerNumberChanged(self, valueBefore: list[str], valueAfter: list[str]):
    #     self.__logger.info("Player number changed")
    #     super()._onPlayerNumberChanged(valueBefore, valueAfter)
    #     if self.__context:
    #         self.__context._on_update("players count changed", valueBefore, valueAfter)
    #
    def _onGamePauseChanged(self, valueBefore: bool, valueAfter: bool):
        self.__logger.info("Game pause changed: %s -> %s", valueBefore, valueAfter)
        super()._onGamePauseChanged(valueBefore, valueAfter)
        if self.__context:
            self.__context._on_update("game pause changed", valueBefore, valueAfter)

    # def _onRobotNumberChanged(self, valueBefore: list[str], valueAfter: list[str]):
    #     self.__logger.info("Robot number changed : %s -> %s", valueBefore, valueAfter)
    #     super()._onRobotNumberChanged(valueBefore, valueAfter)
    #     if self.__context:
    #         self.__context._on_update("robots count changed", valueBefore, valueAfter)

    def __enter__(self):
        """
        Connect to the server.
        """
        self.__logger.info("Connecting to server")
        while not self.isConnectedToArena():
            self.connect()
            print(".", end=".")
            time.sleep(1.5)

        self.__logger.info("Connected to server")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Disconnect from the server.
        """
        self.__logger.info("Disconnecting from server")
        while self.isConnectedToArena():
            self.disconnect()
            print(".", end=".")
            time.sleep(1.5)
        self.__logger.info("Disconnected from server")
        return True
