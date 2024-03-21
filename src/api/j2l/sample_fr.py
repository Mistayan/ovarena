from getpass import getpass

import pytactx.agent as pytactx

agent = pytactx.AgentFr(nom=input("👾 id: "),
                        arene=input("🎲 arena: "),
                        username="demo",
                        password=getpass("🔑 password: "),
                        url="mqtt.jusdeliens.com",
                        verbosite=3)

while True:
    agent.orienter((agent.orientation + 1) % 4)
    agent.actualiser()
