import random
from robot import Robot
from barrier import Barrier
from cube import Cube
from rectangle import Rectangle

def setup():
    """Creates global variables, draws the splash screen, manages monitor scaling, initializes game elements and variables, and loads images"""

    global field, barriers, red_robot, blue_robot, robots, game_y, scale_factor, cubes, portal_count, switch_imgs, scale_imgs, switch_top_color, scale_top_color, scale_status, switch_red_status, switch_blue_status, tilt_img_dict, plates, switch_red_top, switch_red_bottom, switch_blue_top, switch_blue_bottom, scale_top, scale_bottom, scale_plates, start_time, match_time, in_match

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
    red_robot = Robot(x = 54, y = 488)
    blue_robot = Robot(Robot.BLUE, 1867, 467, angle = PI)
    robots = set()
    robots.add(red_robot)
    robots.add(blue_robot)
    
    # Create plates
    switch_red_top = Rectangle(496.5, 316.5, 145, 109)    
    switch_red_bottom = Rectangle(496.5, 637.5, 145, 109)
    switch_blue_top = Rectangle(1421.5, 316.5, 145, 109)
    switch_blue_bottom = Rectangle(1421.5, 637.5, 145, 109)
    scale_top = Rectangle(960, 263, 144, 110)
    scale_bottom = Rectangle(960, 690, 144, 108)
    plates = set()
    plates.add(switch_red_top)
    plates.add(switch_red_bottom)
    plates.add(switch_blue_top)
    plates.add(switch_blue_bottom)
    plates.add(scale_top)
    plates.add(scale_bottom)
    for plate in plates:
        plate.mass = 0.0
        
    scale_plates = set()
    scale_plates.add(scale_top)
    scale_plates.add(scale_bottom)
    
    # Create barriers
    barriers = set()
    barrier_regions = {"field_walls": [(0, 0, 1920, 0), (1920, 0, 1920, 953), (1920, 953, 0, 953), (0, 953, 0, 0)],
                       "portal_walls": [(0, 86, 104, 0), (1816, 0, 1920, 86), (0, 867, 104, 953), (1816, 953, 1920, 867)],
                       "red_switch": [(416, 251, 577, 251), (577, 251, 577, 702), (577, 702, 416, 702), (416, 702, 416, 251)], # (416, 251)(577, 251)(577, 702)(416, 702)
                       "blue_switch": [(1341, 251, 1502, 251), (1502, 251, 1502, 702), (1502, 702, 1341, 702), (1341, 702, 1341, 251)], # (1341, 251)(1502, 251)(1502, 702)(1341, 702)
                       "scale": [(936, 311, 985, 311), (985, 311, 985, 642), (985, 642, 936, 642), (936, 642, 936, 311)]} # (936, 311)(985, 311)(985, 642)(936, 642)

    for region in barrier_regions.values():
        for barrier in region:
            barriers.add(Barrier(barrier[0], barrier[1], barrier[2], barrier[3]))

    # Create cubes
    cubes = []
    red_cube_regions = {"red_platform_zone": [(599, 685), (599, 603), (599, 519), (599, 436), (599, 352), (599, 269)],
                        "red_power_cube_zone": [(394, 433), (394, 476), (394, 520), (354, 455), (354, 498), (314, 476), (394, 455), (394, 498), (354, 476), (394, 476)]}
    blue_cube_regions = {"blue_platform_zone": [(1320, 685), (1320, 603), (1320, 519), (1320, 436), (1320, 352), (1320, 269)],
                         "blue_power_cube_zone": [(1525, 433), (1525, 477), (1525, 520), (1565, 455), (1565, 498), (1605, 477), (1525, 455), (1525, 498), (1565, 477), (1525, 477)]}

    for region in red_cube_regions.values():
        for cube in region:
            cubes.append(Cube(cube[0], cube[1], side = "red"))
    
    for region in blue_cube_regions.values():
        for cube in region:
            cubes.append(Cube(cube[0], cube[1], side = "blue"))

    # Keep track of how many cubes are in each portal
    portal_count = {"red": {"top": 7, "bottom": 7}, "blue": {"top": 7, "bottom": 7}}
    
    # Resize field to monitor size
    field = loadImage("field.png")
    # field = loadImage("../Assets/Images/Field/Field-(No-Scale-or-Switches)-3840x2160.png")
    # field.resize(1920, int(field.height * 2/ 2))

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
    
    # Instantiate timer variables
    start_time = 0
    match_time = 0
    in_match = False
    in_auto = False
    
def draw():
    global start_time, match_time, in_match, in_auto, switch_red_status, switch_blue_status, scale_status
    """Draws the field, switches and scale, robots, cubes, and barriers if necessary"""
    # Translates everything to a vertically-centered spot (CHECK THIS!) for safe monitor scaling
    translate(0, int((displayHeight - game_y) / 2))

    # Scales all objects drawn afterwards
    scale(scale_factor)

    # Draws the switch lights, the switches, the scale lights, and the scale using the CENTER mode of drawing
    # images for easy alignment of switches/scales with lights. Afterwards, reverts to CORNER mode.
    image(field, 0, 0)

    # Update time and score
    if in_match and (millis() - start_time > 1000 * (151 - match_time)):
        match_time -= 1
        if in_auto:
            score_increment = 2
        else:
            score_increment = 1
        
        # Negative status means tilted towards top, positive status means tilted towards bottom
        if (switch_top_color == "red" and switch_red_status < 0) or (switch_top_color == "blue" and switch_red_status > 0):
            red_robot.score += score_increment
        if (switch_top_color == "red" and switch_blue_status > 0) or (switch_top_color == "blue" and switch_blue_status < 0):
            blue_robot.score += score_increment
        if (scale_top_color == "red" and scale_status < 0) or (scale_top_color == "blue" and scale_status > 0):
            red_robot.score += score_increment
        if (scale_top_color == "red" and scale_status > 0) or (scale_top_color == "blue" and scale_status < 0):  
            blue_robot.score += score_increment
        
        if match_time == 135:
            in_auto = False
        elif match_time == 0:
            # Give parking and climbing points
            if red_robot.climb_height == 100:
                red_robot.score += 30
            else:
                x = red_robot.x
                y = red_robot.y
                if 812 < x and x < 935 and 322 < y and y < 631:
                    red_robot.score += 5
                    
            if blue_robot.climb_height == 100:
                blue_robot.score += 30
            else:
                x = blue_robot.x
                y = blue_robot.y
                if 631 < x and x < 1107 and 322 < y and y < 631:
                    blue_robot.score += 5
            
            in_match = False
    
    # Display scores
    fill(color(0))
    textSize(48)
    text(red_robot.score, 637, 1015)
    text(blue_robot.score, 1282, 1015)
    
    # Display match time
    
    if in_match:
        fill(color(63, 158, 73))
        delta_x = int(match_time / 150.0 * 444.0)
        rect(738, 957, 444 - delta_x, 64)
        fill(color(0))
    
        textSize(36)
        if in_auto:
            text(match_time - 135, 959, 987)
        else:
            text(match_time, 959, 987)
    
    else:
        textSize(30)
        text("Press 'g' to start", 959, 987)
        
    # Update switch and scale status
    switch_red_mass = switch_red_bottom.mass - switch_red_top.mass
    switch_blue_mass = switch_blue_bottom.mass - switch_blue_top.mass
    scale_mass = scale_bottom.mass - scale_top.mass
    
    if switch_red_mass <= -2:
        switch_red_status = -2
    elif switch_red_mass <= -0.5:
        switch_red_status = -1
    elif switch_red_mass <= 0.5:
        switch_red_status = 0
    elif switch_red_mass <= 2:
        switch_red_status = 1
    else:
        switch_red_status = 2
        
    if switch_blue_mass <= -2:
        switch_blue_status = -2
    elif switch_blue_mass <= -0.5:
        switch_blue_status = -1
    elif switch_blue_mass <= 0.5:
        switch_blue_status = 0
    elif switch_blue_mass <= 2:
        switch_blue_status = 1
    else:
        switch_blue_status = 2
        
    if scale_mass <= -2:
        scale_status = -2
    elif scale_mass <= -0.5:
        scale_status = -1
    elif scale_mass <= 0.5:
        scale_status = 0
    elif scale_mass <= 2:
        scale_status = 1
    else:
        scale_status = 2
    
    imageMode(CENTER)

    image(switch_imgs["lights-" + switch_top_color + "-top"], 496, 476.5)
    image(switch_imgs["lights-" + switch_top_color + "-top"], 1421, 476.5)

    image(switch_imgs[tilt_img_dict[switch_red_status]], 496, 476.5)
    image(switch_imgs[tilt_img_dict[switch_blue_status]], 1421, 476.5)

    imageMode(CORNER)
    
    for cube in cubes:
        if not cube.placed:
            cube.draw()

    for barrier in barriers:
        barrier.draw()
    
    for robot in robots:
        robot.draw(barriers, robots, cubes, scale_plates)
        
    imageMode(CENTER)
    image(scale_imgs["lights-" + scale_top_color + "-top"], 960, 476.5)
    image(scale_imgs[tilt_img_dict[scale_status]], 960, 476.5)
    imageMode(CORNER)
    
    for cube in cubes:
        if cube.placed:
            cube.draw()

def keyPressed():
    global start_time, match_time, in_match, in_auto
    """Manages pressed keys for robot controls"""
    lowerKey = str(key).lower()
    if lowerKey == 'g' and not in_match:
        in_match = True
        in_auto = True
        red_robot.score = 0
        blue_robot.score = 0
        start_time = millis()
        match_time = 150
    
    if in_match:
        if lowerKey == 'w':
            red_robot.accel = True
        elif lowerKey == 's':
            red_robot.decel = True
        elif lowerKey == 'a':
            red_robot.turn_l = True
        elif lowerKey == 'd':
            red_robot.turn_r = True
        elif lowerKey == 'q':
            red_robot.intake(cubes, plates, scale_plates, robots)
        elif lowerKey == 'e':
            red_robot.elevator()
        elif lowerKey == 'x':
            red_robot.portal(portal_count, cubes, in_auto)
        elif lowerKey == 'c':
            red_robot.climber()
        
        elif lowerKey == 'i':
            blue_robot.accel = True
        elif lowerKey == 'k':
            blue_robot.decel = True
        elif lowerKey == 'j':
            blue_robot.turn_l = True
        elif lowerKey == 'l':
            blue_robot.turn_r = True
        elif lowerKey == 'u':
            blue_robot.intake(cubes, plates, scale_plates, robots)
        elif lowerKey == 'o':
            blue_robot.elevator()
        elif lowerKey == 'm':
            blue_robot.portal(portal_count, cubes, in_auto)
        elif lowerKey == 'n':
            blue_robot.climber()
    
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