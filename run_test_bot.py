import time

from src.api.j2l.pytactx.agent import Agent
import dotenv
import os

if __name__ == '__main__':
    dotenv.load_dotenv()

    agent = Agent(
        "rand'O",
        os.getenv("ARENA"),
        os.getenv("LOGIN"),
        os.getenv("PASSWORD"),
        server="mqtt.jusdeliens.com",
        port=1883,
    )
    while agent.isConnectedToArena() is False:
        time.sleep(1)
        agent.connect()
    print("Connected to arena, waiting for game to start")
    while agent.isGamePaused:
        time.sleep(1)
        agent.lookAt((agent.dir + 1) % 4)
        agent.update()
    print("Game started, waiting for game to end")
    while not agent.isGamePaused:
        time.sleep(1)
    print("Game ended, disconnecting from arena")
    agent.disconnect()
    print("Done !")
