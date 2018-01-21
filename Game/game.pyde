from robot import Robot
from barrier import BarrierLine, BarrierCircle
from cube import Cube

def setup():
    global field, red_robot, blue_robot, barriers, robots, game_y, scale_factor, cube

    fullScreen()

    textSize(50)
    text("TOP-DOWN FIRST POWER UP", 500, 500)

    # Used in scaling game
    game_y = displayWidth * 9.0 / 16.0
    scale_factor = displayWidth / 3840.0

    red_robot = Robot(Robot.RED, 100, 100, 99, 84)
    blue_robot = Robot(Robot.BLUE, 1820, 880, 99, 84, PI)
    cube = Cube()

    barriers = set()
    barriers.add(BarrierLine(0, 0, 1920, 0))
    barriers.add(BarrierLine(1920, 0, 1920, 953))
    barriers.add(BarrierLine(1920, 953, 0, 953))
    barriers.add(BarrierLine(0, 953, 0, 0))
    barriers.add(BarrierLine(0, 86, 104, 0))
    barriers.add(BarrierLine(1816, 0, 1920, 86))
    barriers.add(BarrierLine(0, 867, 104, 953))
    barriers.add(BarrierLine(1816, 953, 1920, 867))
    barriers.add(BarrierCircle(200, 200, 3, True))

    robots = set()
    robots.add(red_robot)
    robots.add(blue_robot)

    field = loadImage("../Assets/Images/Field/Field-(No-Scale-or-Switches)-3840x2160.png")
    field.resize(displayWidth, int(scale_factor * field.height))
    image(field, 0, 0)

    switch_img_path = "../Assets/Images/Field/Switch Variants"
    switch_imgs = {"balanced-left" : loadImage(switch_img_path + "/balanced-left.png"),
                   "balanced-right" : loadImage(switch_img_path + "/balanced-right.png"),
                   "bottom-tilt-1-left" : loadImage(switch_img_path + "/bottom-tilt-1-left.png"),
                   "bottom-tilt-1-right" : loadImage(switch_img_path + "/bottom-tilt-1-right.png"),
                   "bottom-tilt-2-left" : loadImage(switch_img_path + "/bottom-tilt-2-left.png"),
                   "bottom-tilt-2-right" : loadImage(switch_img_path + "/bottom-tilt-2-right.png"),
                   "top-tilt-1-left" : loadImage(switch_img_path + "/top-tilt-1-left.png"),
                   "top-tilt-1-right" : loadImage(switch_img_path + "/top-tilt-1-right.png"),
                   "top-tilt-2-left" : loadImage(switch_img_path + "/top-tilt-2-left.png"),
                   "top-tilt-2-right" : loadImage(switch_img_path + "/top-tilt-2-right.png"),
                   "lights-blue-top-left" : loadImage(switch_img_path + "/lights-blue-top-left.png"),
                   "lights-blue-top-right" : loadImage(switch_img_path + "/lights-blue-top-right.png"),
                   "lights-red-top-left" : loadImage(switch_img_path + "/lights-red-top-left.png"),
                   "lights-red-top-right" : loadImage(switch_img_path + "/lights-red-top-right.png")}

    for img in switch_imgs:
        switch_imgs[img].resize(displayWidth, int(scale_factor * field.height))

def draw():
    background(0)
    
    # Draw the field
    translate(0, int((displayHeight - game_y) / 2))
    image(field, 0, 0)
    
    # Scale the field
    scale(displayWidth / 1920.0)

    # Draw objects
    for robot in robots:
        robot.draw(barriers, robots)
    #cube.draw()
    
    for barrier in barriers:
        barrier.draw()

def keyPressed():
    lowerKey = str(key).lower()
    if lowerKey == 'w':
        red_robot.accel = True
    elif lowerKey == 's':
        red_robot.decel = True
    elif lowerKey == 'a':
        red_robot.turn_l = True
    elif lowerKey == 'd':
        red_robot.turn_r = True
    elif lowerKey == 'i':
        blue_robot.accel = True
    elif lowerKey == 'k':
        blue_robot.decel = True
    elif lowerKey == 'j':
        blue_robot.turn_l = True
    elif lowerKey == 'l':
        blue_robot.turn_r = True

def keyReleased():
    lowerKey = str(key).lower()
    if lowerKey == 'w':
        red_robot.accel = False
    elif lowerKey == 's':
        red_robot.decel = False
    elif lowerKey == 'a':
        red_robot.turn_l = False
    elif lowerKey == 'd':
        red_robot.turn_r = False
    elif lowerKey == 'i':
        blue_robot.accel = False
    elif lowerKey == 'k':
        blue_robot.decel = False
    elif lowerKey == 'j':
        blue_robot.turn_l = False
    elif lowerKey == 'l':
        blue_robot.turn_r = False