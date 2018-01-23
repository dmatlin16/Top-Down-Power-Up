from robot import Robot
from barrier import Barrier
from cube import Cube

def setup():
    global field, red_robot, blue_robot, barriers, robots, game_y, scale_factor, cubes, portal_count

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
    cube_regions = {"red_platform_zone": [(599, 688), (599, 605), (599, 521), (599, 438), (599, 354), (599, 271)],
                    "blue_platform_zone": [(1320, 688), (1320, 605), (1320, 521), (1320, 438), (1320, 354), (1320, 271)],
                    "red_power_cube_zone": [(398, 433), (398, 476), (398, 520), (355, 455), (355, 498), (313, 476), (376, 455), (376, 498), (334, 476), (356, 476)],
                    "blue_power_cube_zone": [(1520, 433), (1520, 477), (1520, 520), (1563, 455), (1563, 498), (1605, 477), (1542, 455), (1542, 498), (1584, 477), (1563, 477)]}
    for region in cube_regions.values():
        for cube in region:
            cubes.append(Cube(cube[0], cube[1]))
    
    # Keep track of how many cubes are in each portal
    portal_count = {"red": {"top": 7, "bottom": 7}, "blue": {"top": 7, "bottom": 7}}
    field = loadImage("../Assets/Images/Field/Field-(No-Scale-or-Switches)-3840x2160.png")
    field.resize(displayWidth, int(displayWidth / 3840.0 * field.height))

def draw():
    background(0)
    
    # Draw the field
    translate(0, int((displayHeight - game_y) / 2))
    image(field, 0, 0)
    
    # Scale the field
    scale(scale_factor)

    # Draw objects
    for robot in robots:
        robot.draw(barriers, robots, cubes)
    for cube in cubes:
        cube.draw(barriers)
    
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