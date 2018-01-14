class Robot:
    # Constants
    ACCEL = 0.30
    FRICTION = 0.95
    ANGACCEL = PI / 60
    RED = color(237, 28, 36)
    BLUE = color(1, 145, 255)

    # States
    accel = False
    decel = False
    turn_l = False
    turn_r = False
    has_cube = False

    # # Robot Images
    # bumpers_blue = loadImage("../Assets/Images/Robot/bumpers_blue.png")
    # bumpers_red = loadImage("../Assets/Images/Robot/bumpers_red.png")
    # robot = loadImage("../Assets/Images/Robot/robot.png")
    # robot_cube = loadImage("../Assets/Images/Robot/robot_cube.png")

    def __init__(self, color = RED, x = 0.0, y = 0.0, w = 99, h = 84, angle = 0, speed = 0):
        """Initiates the instance of Robot.
        Will create a red robot at [0, 0] with a width of 99 and a height of 84 that is unmoving
        and facing right unless otherwise specified"""
        self.pos = PVector(x, y)
        self.color = color
        self.w = w
        self.h = h
        self.speed = 0
        self.angle = angle
        self.vel = PVector(0, 0)
        # if color == Robot.RED or color == Robot.BLUE:
        #     self.isredblue = True

    def draw(self):
        """Draws the instance of Robot"""
        pushMatrix() # Save the empty transform matrix in the stack so that it can be restored for next Robot instance 
        self.move_robot()
        
        # if self.redblue:
        #     if self.has_cube:
        #         robotimg = Robot.robot_cube
        #     else:
        #         robotimg = Robot.robot
        #     image(robotimg, self.pos.x, self.pos.y)
        
        # Sets drawing options for instance of Robot
        fill(self.color)
        stroke(0)
        strokeWeight(2)

        # Puts draw functions (e.g., rect(), ellipse()) into robot's reference frame to make drawing easier
        translate(self.pos.x, self.pos.y)
        rotate(self.angle)
        
        rect(-self.w / 2, -self.h / 2, self.w, self.h, 3)
        ellipse(25, 0, 11, 11)

        popMatrix() # Restores reference frame to empty transform matrix by popping modified matrix off the stack

    def move_robot(self):
        if self.accel:
            self.speed += self.ACCEL
        if self.decel:
            self.speed -= self.ACCEL
        self.speed *= self.FRICTION

        if self.turn_r:
            self.angle += self.ANGACCEL
        if self.turn_l:
            self.angle -= self.ANGACCEL
    
        self.vel.x = self.speed * cos(self.angle)
        self.vel.y = self.speed * sin(self.angle)
        
        self.pos += self.vel