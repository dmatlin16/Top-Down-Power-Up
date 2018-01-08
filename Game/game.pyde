from robot import Robot

redRobot = Robot(100, 100)

def setup():
    size(640, 480)

def draw():
    fill(255, 255, 255)
    rect(0, 0, 640, 480)
    redRobot.display() # Note form Michael: maybe rename to ".draw()" because it's p standard

def keyPressed():
    if(key == 'w' or key == 'W'):
        redRobot.is_accel = True
    elif(key == 's' or key == 'S'):
        redRobot.is_decel = True
    elif(key == 'a' or key == 'A'):
        redRobot.is_turn_l = True
    elif(key == 'd' or key == 'D'):
        redRobot.is_turn_r = True

def keyReleased():
    if(key == 'w' or key == 'W'):
        redRobot.is_accel = False
    elif(key == 's' or key == 'S'):
        redRobot.is_decel = False
    elif(key == 'a' or key == 'A'):
        redRobot.is_turn_l = False
    elif(key == 'd' or key == 'D'):
        redRobot.is_turn_r = False