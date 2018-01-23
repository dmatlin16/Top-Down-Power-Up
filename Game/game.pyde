import random
from robot import Robot
from barrier import Barrier
from cube import Cube

def setup():
    """Creates global variables, draws the splash screen, manages monitor scaling, initializes game elements and variables, and loads images"""

    global field, red_robot, blue_robot, barriers, robots, game_y, scale_factor, cubes, portal_count, switch_imgs, scale_imgs, switch_top_color, scale_top_color, scale_status, switch_red_status, switch_blue_status, tilt_img_dict

    # Set background and draw splash screen
    background(0)
    textSize(50)
    textAlign(CENTER, CENTER)
    text("TOP-DOWN FIRST POWER UP\nLoading assets", displayWidth // 2, displayHeight // 2)

    fullScreen()

    # Used in scaling game
    game_y = displayWidth * 9.0 / 16.0
    scale_factor = displayWidth / 1920.0

    # Create robots
    red_robot = Robot(x=100, y=100)
    blue_robot = Robot(Robot.BLUE, 1820, 880, angle=PI)

    robots = set()
    robots.add(red_robot)
    robots.add(blue_robot)

    # Create barriers
    barriers = set()
    barrier_regions = {"field_walls": [(0, 0, 1920, 0), (1920, 0, 1920, 953), (1920, 953, 0, 953), (0, 953, 0, 0)],
                       "portal_walls": [(0, 86, 104, 0), (1816, 0, 1920, 86), (0, 867, 104, 953), (1816, 953, 1920, 867)]}

    for region in barrier_regions.values():
        for barrier in region:
            barriers.add(Barrier(barrier[0], barrier[1], barrier[2], barrier[3]))

    # Create cubes
    cubes = []
    cube_regions = {"red_platform_zone": [(599, 685), (599, 603), (599, 519), (599, 436), (599, 352), (599, 269)],
                    "blue_platform_zone": [(1320, 685), (1320, 603), (1320, 519), (1320, 436), (1320, 352), (1320, 269)],
                    "red_power_cube_zone": [(394, 433), (394, 476), (394, 520), (354, 455), (354, 498), (314, 476), (394, 455), (394, 498), (354, 476), (394, 476)],
                    "blue_power_cube_zone": [(1525, 433), (1525, 477), (1525, 520), (1565, 455), (1565, 498), (1605, 477), (1525, 455), (1525, 498), (1565, 477), (1525, 477)]}

    for region in cube_regions.values():
        for cube in region:
            cubes.append(Cube(cube[0], cube[1]))

    # Keep track of how many cubes are in each portal
    portal_count = {"red": {"top": 7, "bottom": 7}, "blue": {"top": 7, "bottom": 7}}
    
    # Resize field to monitor size
    field = loadImage("../Assets/Images/Field/Field-(No-Scale-or-Switches)-3840x2160.png")
    # field.resize(displayWidth, int(displayWidth / 3840.0 * field.height))
    field.resize(1920, int(field.height / 2))

    # Create random switch and scale sides
    switch_top_color = random.choice(["red", "blue"])
    scale_top_color = random.choice(["red", "blue"])

    # Instantiate status variables for switches and scale
    scale_status = 0
    switch_red_status = 0
    switch_blue_status = 0

    # This is a dictionary to help link switch and scale status to image path
    tilt_img_dict = {-2 : "top-tilt-2", -1 : "top-tilt-1", 0 : "balanced", 1 : "bottom-tilt-1", 2 : "bottom-tilt-2"}

    # Load switch and scale images
    img_variants = ["balanced", "bottom-tilt-1", "bottom-tilt-2", "top-tilt-1", "top-tilt-2", "lights-blue-top", "lights-red-top"]
    switch_imgs = {}
    scale_imgs = {}

    for variant in img_variants:
        # Load switch image of that variant
        switch_imgs[variant] = loadImage("../Assets/Images/Field/Switch Variants/" + variant + ".png")

        # Load scale image of that variant
        scale_imgs[variant] = loadImage("../Assets/Images/Field/Scale Variants/" + variant + ".png")

def draw():
    """Draws the field, switches and scale, robots, cubes, and barriers if necessary"""
    # Translates everything to a vertically-centered spot (CHECK THIS!) for safe monitor scaling
    translate(0, int((displayHeight - game_y) / 2))

    # Scales all objects drawn afterwards
    scale(scale_factor)

    # Draws the switch lights, the switches, the scale lights, and the scale using the CENTER mode of drawing
    # images for easy alignment of switches/scales with lights. Afterwards, reverts to CORNER mode.
    image(field, 0, 0)

    imageMode(CENTER)

    image(switch_imgs["lights-" + switch_top_color + "-top"], 496, 476.5)
    image(switch_imgs["lights-" + switch_top_color + "-top"], 1421, 476.5)
    image(scale_imgs["lights-" + scale_top_color + "-top"], 960, 476.5)

    image(switch_imgs[tilt_img_dict[switch_red_status]], 496, 476.5)
    image(switch_imgs[tilt_img_dict[switch_blue_status]], 1421, 476.5)
    image(scale_imgs[tilt_img_dict[scale_status]], 960, 476.5)

    imageMode(CORNER)

    for robot in robots:
        robot.draw(barriers, robots, cubes)

    for cube in cubes:
        cube.draw(barriers, robots)

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
        y = red_robot.y
        top_y = 43.0
        bottom_y = 910.0
        # If closer to top portal, try to spawn a cube in the upper right
        if abs(y - top_y) < abs(y - bottom_y):
            if portal_count["red"]["top"] > 0:
                portal_count["red"]["top"] -= 1
                cubes.append(Cube(1854, 59, 0.691))
        # Otherwise, try to spawn a cube in the lower right
        else:
            if portal_count["red"]["bottom"] > 0:
                portal_count["red"]["bottom"] -= 1
                cubes.append(Cube(1854, 894, -0.691))

    elif lowerKey == 'm':
        y = blue_robot.y
        top_y = 43.0
        bottom_y = 910.0
        # If closer to top portal, try to drop a cube in the upper left
        if abs(y - top_y) < abs(y - bottom_y):
            if portal_count["blue"]["top"] > 0:
                portal_count["blue"]["top"] -= 1
                cubes.append(Cube(66, 59, -0.691))
        # Otherwise, try to drop a cube in the lower left
        else:
            if portal_count["blue"]["bottom"] > 0:
                portal_count["blue"]["bottom"] -= 1
                # spawn lower left
                cubes.append(Cube(66, 894, 0.691))

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