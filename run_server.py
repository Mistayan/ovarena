"""
Entry point for the server.
"""
from src.server.control_board import ArenaControlBoard
from src.server.gestionnaire import Gestionnaire as Manager

if __name__ == '__main__':
    with Manager("...", "...", "...", "...") as manager:
        with ArenaControlBoard(manager) as control_board:
            control_board.mainloop()
