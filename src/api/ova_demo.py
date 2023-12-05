"""
Ce ficier python est utilisé pour instancier une connexion 
au __robot OVA__ **ou** un __Agent virtuel__
le robot peut être contrôllé via les différentes méthodes de l'API exposées
"""
import random
import time

import j2l.pyrobotx.client as ova
from j2l.pyrobotx.robot import IRobot, RobotEvent


# Pour piloter une ova via un broker MQTT
robot: IRobot = ova.OvaClientMqtt(server="mqtt.jusdeliens.com",
                                  port=1883,
                                  useProxy=False)  # Agent Virtuel


# Pour piloter une ova sur un LAN ou si vous êtes directement connecté à son point d'accès
# robot:IRobot = OvaClientHttpV2(url="192.168.x.x")  # Robot OVA


# Appel de la callback on_event pour chaque évènements du robot
def on_event(source, event, value):
    """
    Affiche les évennements reçus dans la console,
    pour aider le joueur à comprendre ce qu'il se passe sur son robot
    """
    print("Rx event", event, "from", source, ":", value)


robot.addEventListener(RobotEvent.imageReceived, on_event)
robot.addEventListener(RobotEvent.robotChanged, on_event)
robot.addEventListener(RobotEvent.robotConnected, on_event)
robot.addEventListener(RobotEvent.robotDisconnected, on_event)

print("########################")
while not robot.isConnectedToRobot():
    print("Awaiting robot connection...")
    robot.update()
    time.sleep(1)

print("########################")
print("🟢 BEGIN TEST")
robot.enableCamera(False)
beginMelody = []
for i in range(3, 11, 1):
    beginMelody.append((i, 50))
robot.playMelody(beginMelody)
robot.setMotorSpeed(0, 0)
robot.setLedColor(0, 0, 0)
robot.update()

print("########################")
print("🔦 Test sensors")
print("Change the light above the robot to see how sensors values change")
for i in range(50):
    robot.update()
    time.sleep(0.1)
    print("⬆️ Photo front lum: ", robot.getFrontLuminosity())
    print("⬇️ Photo back lum: ", robot.getBackLuminosity())
    print("🔋 Battery voltage: ", robot.getBatteryVoltage())
    print("⏱️ Timestamp: ", robot.getTimestamp())
    print("📸 Camera img " + str(robot.getImageWidth()) + "x" +
          str(robot.getImageHeight()) + " shot after " +
          str(robot.getImageTimestamp()) + "ms")

print("########################")
print("🔊 Test actuators")
robot.stop()
for i in range(20):
    robot.update()
    robot.setLedColor(random.randint(0, 255), random.randint(0, 255),
                      random.randint(0, 255))
    robot.playMelody([[random.randint(0, 12), 200]])
    robot.setMotorSpeed(random.randint(0, 50), random.randint(0, 50))
robot.stop()

print("########################")
print("📸 Test camera")
robot.enableCamera(True)
for i in range(50):
    robot.update()
    red, green, blue , n = 0, 0, 0, 0
    w, h = robot.getImageWidth(), robot.getImageHeight()
    for x in range(0, w, 10):
        for y in range(0, h, 10):
            color = robot.getImagePixelRGB(x, y)
            red += color[0]
            green += color[1]
            blue += color[2]
            n += 1
    if n > 0:
        red = red // n
        green = green // n
        blue = blue // n
        print("📸 Camera img " + str(w) + "x" + str(h) + " shot after " +
              str(robot.getImageTimestamp()) + "ms")
        print("🔴<R>=" + str(red) + " 🟢<G>=" + str(green) + " 🔵<B>=" + str(blue))
        robot.setLedColor(red, green, blue)
    time.sleep(0.1)
robot.enableCamera(False)

print("########################")
print("🔴 END TEST")
endMelody = []
for i in range(10, 2, -1):
    endMelody.append((i, 50))
robot.playMelody(endMelody)
robot.stop()
robot.update()
