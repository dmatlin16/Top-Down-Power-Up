from barrier import Barrier

class Robot:
    # Constants
    ACCEL = 0.30
    FRICTION = 0.95
    ANGACCEL = PI/60
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
        self.x = x
        self.y = y
        self.color = color
        self.w = w
        self.h = h
        self.speed = 0
        self.angle = angle
        # if color == Robot.RED or color == Robot.BLUE:
        #     self.isredblue = True

    def draw(self, barriers, robots):
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
        
        # Collision detection
        for barrier in barriers:
            if self.is_colliding(barrier):
                normal_angle = self.get_normal_angle(barrier)
            while self.is_colliding(barrier):
                self.speed *= self.FRICTION
                self.x += cos(normal_angle)
                self.y += sin(normal_angle)

        for robot in robots:
            if not robot is self:
                for edge in robot.get_lines():
                    if self.is_colliding(edge):
                        normal_angle = self.get_normal_angle(edge)
                    while self.is_colliding(edge):
                        self.speed *= self.FRICTION
                        self.x += cos(normal_angle)
                        self.y += sin(normal_angle)

        # Puts draw functions (e.g., rect(), ellipse()) into robot's reference frame to make drawing easier
        translate(self.x, self.y)
        rotate(self.angle)
        
        rect(-self.w/2, -self.h/2, self.w, self.h, 3)
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
        
        self.x += self.speed * cos(self.angle)
        self.y += self.speed * sin(self.angle)

    def get_corners(self):
        """Returns corners of robot as a list of 4 tuples"""
        w = self.w    
        h = self.h
        x = self.x    
        y = self.y
        
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        
        dx1 = (w/2) * cos_a - (h/2) * sin_a
        dy1 = (w/2) * sin_a + (h/2) * cos_a 
        dx2 = (w/2) * cos_a + (h/2) * sin_a 
        dy2 = (w/2) * sin_a - (h/2) * cos_a 
        
        return [(x + dx1, y + dy1), (x + dx2, y + dy2), (x - dx1, y - dy1), (x - dx2, y - dy2)]
    
    def get_lines(self):
        """Returns edges of robot as a list of 4 barriers"""
        c = self.get_corners()
        return [Barrier(c[0][0], c[0][1], c[1][0], c[1][1]),
                Barrier(c[1][0], c[1][1], c[2][0], c[2][1]),
                Barrier(c[2][0], c[2][1], c[3][0], c[3][1]),
                Barrier(c[3][0], c[3][1], c[0][0], c[0][1])]

    
    def is_colliding(self, barrier):
        for robot_edge in self.get_lines():
            if robot_edge.is_colliding(barrier):
                return True
        return False
    
    def get_normal_angle(self, barrier):
        x = self.x
        y = self.y
        x1 = barrier.x1
        y1 = barrier.y1
        x2 = barrier.x2
        y2 = barrier.y2
        
        # Avoid division by 0
        if x1 == x2:
            x2 += 0.0001

        # Get equations of barrier line (y = mx + b), m is slope, b is y-intercept
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m*x1
        
        # Y-distance from the point to the line
        y_distance = m*x + b - y
        
        # If y-distance is positive, then the point is clockwise from the line with respect to Point 1 
        if y_distance >= 0:
            # Return the barrier's angle minus 90 degrees
            return atan(m) - PI/2
        # Otherwise, the point is counterclockwise from the line with respect to Point 1
        else:
            # Return the barrier's angle plus 90 degrees
            return atan(m) + PI/2