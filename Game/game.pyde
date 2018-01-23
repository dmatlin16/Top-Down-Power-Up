from robot import Robot
from barrier import Barrier
from cube import Cube

def setup():
    global field, red_robot, blue_robot, barriers, robots, game_y, scale_factor, cube1, cubes

    fullScreen()

    # Used in scaling game
    game_y = displayWidth * 9.0 / 16.0
    scale_factor = displayWidth / 1920.0
    
    red_robot = Robot(x=100, y=100)
    blue_robot = Robot(Robot.BLUE, 1820, 880, angle=PI)
    
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
        cubes.add(Cube(100, 100))

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