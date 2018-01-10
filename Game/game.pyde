from robot import Robot

def setup():
    # REMINDER TO IMPLEMENT SCALE FACTOR IN CASE SOMEONE PLAYS ON A SCREEN LARGER OR SMALLER THAN 1080p (if wanted)
    global field, red_robot, blue_robot

    fullScreen()

    # Scales field and robots to screen size
    robot_default_size = (99, 84)
    scale_factor = displayWidth / 1920.0
    robot_scaled_size = (robot_default_size[0] * scale_factor, robot_default_size[1] * scale_factor)

    red_robot = Robot(Robot.RED, 100, 200, robot_scaled_size[0], robot_scaled_size[1])
    blue_robot = Robot(Robot.BLUE,  displayWidth - 100, displayHeight - 100, robot_scaled_size[0], robot_scaled_size[1], PI)
    field = loadImage("../Assets/Images/Field/Field-(No-Scale-or-Switches)-1920-px-wide.png")
    print(field.height)
    field.resize(displayWidth, int(scale_factor * field.height))

def draw():
    fill(0, 0, 0)
    rect(0, 0, displayWidth, displayHeight)
    
    # NOTE THAT THIS METHOD OF DRAWING THE FIELD IS TEMPORARY AND OPTIMALLY WILL BE DRAWN USING transform() TO CREATE A PROPER REFERENCE FRAME OF SOME SORT AND TO PREVENT HACKINESS
    imageMode(CORNERS)
    image(field, (displayWidth - field.width) / 2, displayHeight - field.height, (displayWidth + field.width) / 2, displayHeight)
    imageMode(CORNER)

    fill(color(255, 255, 255))
    textSize(40)
    text(u"Top-Down FIRST® POWER UP", 10, 10 + textAscent())
    red_robot.draw()
    blue_robot.draw()

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