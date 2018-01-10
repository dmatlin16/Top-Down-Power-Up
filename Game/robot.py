class Robot:
    # Internal Usage

    # Constants
    ACCEL = 0.30
    DECEL = 0.93
    FRICTION = 0.95
    ANGACCEL = PI / 60
    RED = color(237, 28, 36)
    BLUE = color(1, 145, 255)

    # States
    accel = False
    decel = False
    turn_l = False
    turn_r = False

    def __init__(self, color = RED, x = 0.0, y = 0.0, w = 99, h = 84, theta = 0, vel = 0):
        """Initiates the instance of Robot.
        Will create a red robot at [0, 0] with a width of 99 and a height of 84 that is unmoving
        and facing right unless otherwise specified"""
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.vel = 0
        self.theta = theta

    def get_corners(self):
        """Returns corners of a rectangle at an angle."""
        w = self.w
        h = self.h
        theta = self.theta
        x = self.x
        y = self.y
        return [[(h / 2) * cos(theta + PI / 2) + (w / 2) * cos(theta) + x, (h / 2) * sin(theta + PI / 2) + (w / 2) * sin(theta) + y],
                [(h / 2) * cos(theta - PI / 2) + (w / 2) * cos(theta) + x, (h / 2) * sin(theta - PI / 2) + (w / 2) * sin(theta) + y],
                [(h / 2) * cos(theta - PI / 2) - (w / 2) * cos(theta) + x, (h / 2) * sin(theta - PI / 2) - (w / 2) * sin(theta) + y],
                [(h / 2) * cos(theta + PI / 2) - (w / 2) * cos(theta) + x, (h / 2) * sin(theta + PI / 2) - (w / 2) * sin(theta) + y]]
    
    def draw(self):
        """Draws the instance of Robot"""
        pushMatrix() # Save the empty transform matrix in the stack so that it can be restored for next Robot instance 
        self.move_robot()

        # Sets drawing options for instance of Robot
        fill(self.color)
        stroke(0)
        strokeWeight(2)

        # Puts draw functions (e.g., rect(), ellipse()) into robot's reference frame to make drawing easier
        translate(self.x, self.y)
        rotate(self.theta)
        
        rect(-self.w / 2, - self.h / 2, self.w, self.h, 3)
        ellipse(25, 0, 11, 11)

        popMatrix() # Restores reference frame to empty transform matrix by popping modified matrix off the stack

    def move_robot(self):
        if self.accel:
            self.vel += self.ACCEL
        if self.decel:
            self.vel -= self.ACCEL
        self.vel *= self.FRICTION

        if self.turn_r:
            self.theta += self.ANGACCEL
        if self.turn_l:
            self.theta -= self.ANGACCEL
    
        self.x += self.vel * cos(self.theta)
        self.y += self.vel * sin(self.theta)