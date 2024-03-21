import os

import dotenv

from src.api.j2l.pytactx.agent import Agent

dotenv.load_dotenv()

agent = Agent(
    os.getenv("USER"),
    os.getenv("ARENA"),
    os.getenv("LOGIN"),
    os.getenv("PASSWORD"),
    os.getenv("SERVER"),
    int(os.getenv("PORT"))
)

print(agent.game)

print(agent.game["maxPlayers"])
rules = {"gridColumns": 3,
         "gridRows": 4,
         "map": [
             [0, 2, 0],
             [3, 2, 3],
             [3, 2, 3],
             [0, 2, 0]],

            "maxPlayers": 5,
            "maxRobots": 4,
         }

for key, value in rules.items():
    agent.ruleArena(key, value)
agent.update()

ok = False
for key, value in agent.game.items():
    if key == "maxPlayers" and value == 5:
        ok = True
    print(key, value)

assert ok
