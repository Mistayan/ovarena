from src.server.arena_agent import SyncAgent
from src.server.arena_manager import ArenaManager
import dotenv
import os

if __name__ == '__main__':
    dotenv.load_dotenv()

    with SyncAgent(
        os.getenv("USER"),
        os.getenv("ARENA"),
        os.getenv("LOGIN"),
        os.getenv("PASSWORD"),
        os.getenv("SERVER"),
        int(os.getenv("PORT"))
    ) as agent:
        with ArenaManager(agent) as arena_manager:
            agent.set_context(arena_manager)
            arena_manager.game_loop()
            print("End of game loop")
            agent.disconnect()
