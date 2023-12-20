"""
TK Interface for a Manager.
"""
from __future__ import annotations

import tkinter as tk
from functools import partial
from tkinter.ttk import Button

from src.server.gestionnaire import Gestionnaire as Manager
from .components import TkInputField

_header = []
_body = []


class ControlBoard(tk.Tk):
    def __update_rules(self):
        self.__manager.update_rules({
            "timeLimit": self.__header_fields[0].value,
            "maxPlayers": self.__header_fields[1].value
        })

    def __set_headers(self):
        """
        Display the headers of the control board
        Allows the control game parameters once connected.
        """
        self.__header = tk.Frame(self, bg="grey")
        self.__header.pack(fill=tk.BOTH, expand=True)
        # if not connected, display the connection parameters
        if self.__manager.isConnectedToArena():
            tk.Label(self.__header, text="Game parameters", bg="orange").pack(pady=10)
            self.__header_fields = [
                TkInputField(self.__header, "time limit (ms)", int, input_size=20),
                TkInputField(self.__header, "max players", int)
            ]
            # add button to send infos to manager
            tk.Button(self.__header, text="Update params", command=self.__update_rules
                      ).pack(pady=10)
        # pack the header
        self.__header.pack()

    def __set_body(self):
        self.__body = tk.Frame(self, bg="white")
        # if manager.isConnectedToArena():
        #     self.__login(self.__body, manager)
        # else:
        self.__control_arena()
        # pack the body
        self.__body.pack(fill=tk.BOTH, expand=True)

    # def __login(self, frame):
    #     tk.Label(frame, text="Game parameters", bg="orange").pack(pady=10)
    #     self.__body = [
    #         TkInputField(frame, "name", str, input_size=20),
    #         TkInputField(frame, "arena", str, input_size=15),
    #         TkInputField(frame, "login", str, input_size=15, secured_input=True),
    #         TkInputField(frame, "password", str, input_size=15, secured_input=True)
    #     ]
    #     # add button to send infos to manager
    #     tk.Button(frame, text="Login",
    #               command=partial(self.__manager.update_rules, {
    #                   "timeLimit": _body[0].value,
    #                   "maxPlayers": _body[1].value
    #               })
    #               ).pack(pady=10)

    def __control_arena(self):
        tk.Label(self.__body, text="Control the arena", bg="white").pack(pady=10)
        self.__body.pack()
        self.__body_buttons = [
            Button(self, text="Start", command=self.__manager.game_loop),
            Button(self, text="Stop", command=self.__manager.stop),
            Button(self, text="Unpause" if self.__manager.isGamePaused else "Pause",
                   command=partial(self.__manager.set_pause, not self.__manager.isGamePaused)),
            Button(self, text="Reset", command=self.__manager.restart),
            Button(self, text="Quit", command=self.destroy)
        ]
        for button in self.__body_buttons:
            button.pack(pady=10)

    def __init__(self, manager: Manager = None):
        if manager is None or not isinstance(manager, Manager):
            raise ValueError("control board needs a Manager instance to control")
        super().__init__()
        self.__manager = manager
        self.title("Control Pannel")
        self.geometry("230x600")
        self.resizable(False, False)
        # root.iconbitmap("assets/icon.ico")
        self.config(bg="white")
        self.__set_headers()
        # display the buttons to control the game via the manager
        self.__set_body()
        # if button is pressed, destroy the window, and store the result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()
        return False


if __name__ == '__main__':
    with Manager("kaliopeaHelios", "minova", "demo", "demo") as manager:
        with ControlBoard(manager) as board:
            board.mainloop()
