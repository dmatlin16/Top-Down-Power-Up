from robot import Robot

redRobot = Robot(100, 100, 0, True)

def setup():
    size(640, 480)

def draw():
    redRobot.display()

def keyPressed():
    if(key == 'w' or key == 'W'):
        redRobot.isAccel = True
    elif(key == 's' or key == 'S'):
        redRobot.isDecel = True
    elif(key == 'a' or key == 'A'):
        redRobot.isTurnL = True
    elif(key == 'd' or key == 'D'):
        redRobot.isTurnR = True

def keyReleased():
    if(key == 'w' or key == 'W'):
        redRobot.isAccel = False
    elif(key == 's' or key == 'S'):
        redRobot.isDecel = False
    elif(key == 'a' or key == 'A'):
        redRobot.isTurnL = False
    elif(key == 'd' or key == 'D'):
        redRobot.isTurnR = False