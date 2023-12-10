"""
Débutant en ptyhon ?
Vous connaissez python, mais pas OVA ?
visitez ce lien pour apprendre les basiques pour commencer :
https://tutos.jusdeliens.com/index.php/2020/01/14/pytactx-prise-en-main/


"""
import os
from time import sleep

from src.api.j2l.pytactx.agent import AgentFr as Gestionnaire

arbitre = Gestionnaire(nom=os.environ['ARBITRE_NAME'] or input("👾 id: "),
                       arene=os.environ['ARENA_NAME'] or input("🎲 arena: "),
                       username="demo",
                       password=os.environ['ARENA_PLAYER_PASS'] or input("🔑 password: "),
                       url="mqtt.jusdeliens.com",
                       verbosite=2)

# rules = agent.jeu

# Set arena rules
arbitre.changerArene("maxRobot", 5)  # 2 players on each team + 1 monitor
arbitre.changerArene("blind", [True, False, False, False])
arbitre.changerArene("mass", [10, 100, 10, 10])

# setup teams Rules
arbitre.changerArene("teamName", ["redPill", "bluePill"])
arbitre.changerArene("teamColor", [[255, 0, 0], [0, 0, 255]])
arbitre.changerArene("teamSize", [2, 2])
arbitre.changerArene("teamShape", ["circle", "square"])
arbitre.changerArene("teamShapeParam", [0.5, 0.5])

# setup map
arbitre.changerArene("mapRandFreq", 4.0)  # randint(0, x)
arbitre.changerArene("gridColumns", 60)
arbitre.changerArene("gridRows", 40)

# how slow a player will be on a give tile
arbitre.changerArene("mapFriction", [
    1.0,  # wall:0
    0.0,  # floor:1
    0.3,  # swamp:2
    0.5,  # grass:3
    0.1,  # stoneFloor:4
    1.0,  # robot:5
    0.0,  # goal:6
    0.0,  # monitor:7

])
# grid textures
arbitre.changerArene("mapImgs", [
    "https://i.imgur.com/hDLyrOG.jpeg",  # wall
    "",  # floor
    "",  # swamp
    "",  # grass
    "",  # stoneFloor
    "",  # robot
    "",  # goal
    "",  # monitor
])
arbitre.changerArene("reset", True)
# send rules to server
arbitre.actualiser()

# print rules after update
print("After change : ")
for k, v in arbitre.jeu.items():
    print(k, " : ", v)

# source : https://tutos.jusdeliens.com/index.php/2023/04/27/pytactx-creez-vos-propres-regles-du-jeu
arbitre.changerArene("info", "⌛ Initialisation de l'arbitre...")
while len(arbitre.jeu) == 0:
    arbitre.orienter((arbitre.orientation + 1) % 4)
    arbitre.actualiser()
    sleep(0.5)

# Création d'agents actualisés par l'arène elle-même
agentsScores = {
    "Neo": 0,
    "Smith": 0
}
arbitre.changerArene("info", "⌛ Création des agents...")
for agentId, agentScore in agentsScores:
    arbitre.changerJoueur(agentId, "life", 100)

# Affichage dans l'arène du début de la partie par l'arbitre
# arbitre.changerArene("info", "🟢 C'est parti !")
arbitre.changerArene("info", "🔴 Arène en cours de construction ")

# Boucle principale pour actualiser l'arbitre
tableauScores = []
while True:
    # Changement d'orientation de l'arbitre pour montrer qu'il est actif dans l'arène
    arbitre.orienter((arbitre.orientation + 1) % 4)
    arbitre.actualiser()

    # TODO : application des règles du jeu à chaque tick

    # Affichage du score des 2 bots en temps réel
    arbitre.changerArene("info", tableauScores)
