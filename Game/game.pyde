import random
from robot import Robot
from barrier import Barrier
from cube import Cube

def setup():
    """Creates global variables, draws the splash screen, manages monitor scaling, initializes game elements and variables, and loads images"""
    global field, red_robot, blue_robot, barriers, robots, game_y, scale_factor, cube1, cubes, switch_imgs, scale_imgs, switch_top_color, scale_top_color, scale_status, switch_1_status, switch_2_status, tilt_img_dict
 
    # Set background and draw splash screen
    background(0)
    textSize(50)
    textAlign(CENTER, CENTER)
    text("TOP-DOWN FIRST POWER UP\nLoading assets", displayWidth // 2, displayHeight // 2)

    fullScreen()

    # Used in scaling game
    game_y = displayWidth * 9.0 / 16.0
    scale_factor = displayWidth / 1920.0

    red_robot = Robot(x = 100, y = 100)
    blue_robot = Robot(Robot.BLUE, 1820, 880, 99, 84, angle = PI)

    barriers = set()
    # Field walls
    barriers.add(Barrier(0, 0, 1920, 0))
    barriers.add(Barrier(1920, 0, 1920, 953))
    barriers.add(Barrier(1920, 953, 0, 953))
    barriers.add(Barrier(0, 953, 0, 0))
    
    # Portal walls
    barriers.add(Barrier(0, 86, 104, 0))
    barriers.add(Barrier(1816, 0, 1920, 86))
    barriers.add(Barrier(0, 867, 104, 953))
    barriers.add(Barrier(1816, 953, 1920, 867))

    robots = set()
    robots.add(red_robot)
    robots.add(blue_robot)
    
    cubes = set()

    cubes.add(Cube(200, 100))
    cubes.add(Cube(200, 200))

    # Resize field to monitor size
    field = loadImage("../Assets/Images/Field/Field-(No-Scale-or-Switches)-3840x2160.png")
    field.resize(displayWidth, int(displayWidth / 3840.0 * field.height))

    # Create random switch and scale sides
    switch_top_color = random.choice(["red", "blue"])
    scale_top_color = random.choice(["red", "blue"])
    
    # Instantiate status variables for switches and scale
    scale_status = 0
    switch_1_status = 0
    switch_2_status = 0
    
    # This is a dictionary to help link switch and scale status to image path
    tilt_img_dict = {-2 : "top-tilt-2", -1 : "top-tilt-1", 0 : "balanced", 1 : "bottom-tilt-1", 2 : "bottom-tilt-2"}

    # Load switch and scale images
    switch_img_path = "../Assets/Images/Field/Switch Variants"
    switch_imgs = {"balanced" : loadImage(switch_img_path + "/balanced.png"),
                  "bottom-tilt-1" : loadImage(switch_img_path + "/bottom-tilt-1.png"),
                  "bottom-tilt-2" : loadImage(switch_img_path + "/bottom-tilt-2.png"),
                  "top-tilt-1" : loadImage(switch_img_path + "/top-tilt-1.png"),
                  "top-tilt-2" : loadImage(switch_img_path + "/top-tilt-2.png"),
                  "lights-blue-top" : loadImage(switch_img_path + "/lights-blue-top.png"),
                  "lights-red-top" : loadImage(switch_img_path + "/lights-red-top.png")}
    
    scale_img_path = "../Assets/Images/Field/Scale Variants"
    scale_imgs = {"balanced" : loadImage(scale_img_path + "/balanced.png"),
                  "bottom-tilt-1" : loadImage(scale_img_path + "/bottom-tilt-1.png"),
                  "bottom-tilt-2" : loadImage(scale_img_path + "/bottom-tilt-2.png"),
                  "top-tilt-1" : loadImage(scale_img_path + "/top-tilt-1.png"),
                  "top-tilt-2" : loadImage(scale_img_path + "/top-tilt-2.png"),
                  "lights-blue-top" : loadImage(scale_img_path + "/lights-blue-top.png"),
                  "lights-red-top" : loadImage(scale_img_path + "/lights-red-top.png")}

    for img_path in switch_imgs:
        img = switch_imgs[img_path]
        img.resize(int(scale_factor / 2 * img.width), int(scale_factor / 2 * img.height))
    
    for img_path in scale_imgs:
        img = scale_imgs[img_path]
        img.resize(int(scale_factor / 2 * img.width), int(scale_factor / 2 * img.height))

def draw():
    """Draws the field, switches and scale, robots, cubes, and barriers if necessary"""

    # Translates everything to a vertically-centered spot (CHECK THIS!) for safe monitor scaling
    translate(0, int((displayHeight - game_y) / 2))
    
    image(field, 0, 0)

    # Scales all objects drawn afterwards
    scale(scale_factor)

    # Draws the switch lights, the switches, the scale lights, and the scale using the CENTER mode for drawing images for safe monitor scaling. Afterwards, reverts to CORNER mode
    imageMode(CENTER)

    image(switch_imgs["lights-" + switch_top_color + "-top"], 496, 476.5)
    image(switch_imgs["lights-" + switch_top_color + "-top"], 1421, 476.5)
    image(scale_imgs["lights-" + scale_top_color + "-top"], 960, 476.5)

    image(switch_imgs[tilt_img_dict[switch_1_status]], 496, 476.5)
    image(switch_imgs[tilt_img_dict[switch_2_status]], 1421, 476.5)
    image(scale_imgs[tilt_img_dict[scale_status]], 960, 476.5)

    imageMode(CORNER)

    for robot in robots:
        robot.draw(barriers, robots, cubes)

    for cube in cubes:
        cube.draw(barriers)

    for barrier in barriers:
        barrier.draw()

def keyPressed():
    """Manages pressed keys for robot controls"""
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
    elif lowerKey == 'q':
        red_robot.intake(cubes)
    elif lowerKey == 'u':
        blue_robot.intake(cubes)
    elif lowerKey == 'e':
        red_robot.elevator()
    elif lowerKey == 'o':
        blue_robot.elevator()
    elif lowerKey == 'x':
        cubes.add(Cube(100, 100))

def keyReleased():
    """Manages released keys for robot controls"""
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