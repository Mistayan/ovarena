import os

import dotenv

from src.api.j2l.pytactx.agent import Agent
from src.server.arena_manager import ArenaManager

if __name__ == '__main__':
    dotenv.load_dotenv()

    agent = Agent(
        os.getenv("USER"),
        os.getenv("ARENA"),
        os.getenv("LOGIN"),
        os.getenv("PASSWORD"),
        os.getenv("SERVER"),
        int(os.getenv("PORT"))
    )

    with ArenaManager(agent) as arena_manager:
        # agent.set_context(arena_manager)
        arena_manager.game_loop()
        print("End of game loop")
