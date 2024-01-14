import pytactx.agent as pytactx
from getpass import getpass
import event

agent = pytactx.Agent(playerId=input("👾 robotId: "), arena=input("🎲 arena: "), username="demo", password=getpass("🔑 password: "), server="mqtt.jusdeliens.com", verbosity=2)
event.subscribe(agent)

while True:
  agent.update()
  agent.lookAt((agent.dir + 1) % 4)
