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

    def __init__(self, color = RED, x = 0.0, y = 0.0, w = 99, h = 84, corner = 5.0, angle = 0, speed = 0):
        """Initiates the instance of Robot.
        Will create a red robot at [0, 0] with a width of 99 and a height of 84 that is unmoving
        and facing right unless otherwise specified"""
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.corner = corner
        self.w = float(w) - 2 * corner
        self.h = float(h) - 2 * corner
        self.speed = float(speed)
        self.angle = float(angle)
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
            if self.is_colliding(barrier) >= 0:
                normal_angle = self.get_normal_angle(barrier)
            while self.is_colliding(barrier) >= 0:
                self.speed *= self.FRICTION
                self.x += cos(normal_angle)
                self.y += sin(normal_angle)

        for robot in robots:
            if not robot is self:
                for edge_id, edge in enumerate(robot.get_lines()):
                    colliding_id = self.is_colliding(edge)
                    if colliding_id >= 0:
                        normal_angle = self.get_normal_angle(edge)
                        torque_counterclockwise = self.get_torque_direction(robot, edge_id, colliding_id)
                    while self.is_colliding(edge) >= 0:
                        if torque_counterclockwise:
                            robot.angle += PI/180
                            self.angle -= PI/180
                        else:
                            robot.angle -= PI/180
                            self.angle += PI/180
                        
                        self.x += cos(normal_angle) / 2
                        self.y += sin(normal_angle) / 2
                        robot.x -= cos(normal_angle) / 2
                        robot.y -= sin(normal_angle) / 2

        # Puts draw functions (e.g., rect(), ellipse()) into robot's reference frame to make drawing easier
        translate(self.x, self.y)
        rotate(self.angle)
        
        rect(-self.w/2 - self.corner, -self.h/2 - self.corner, self.w + 2 * self.corner, self.h + 2 * self.corner, self.corner)
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
        for num, corner in enumerate(self.get_corners()):
            if barrier.near_point(corner[0], corner[1]):
                return num
        return -1
        
        # for robot_edge in self.get_lines():
        #     if robot_edge.is_colliding(barrier):
        #         return True
        # return False
    
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
        y_dist = m*x + b - y
        
        # If y-distance is positive, then the point is clockwise from the line with respect to Point 1 
        if y_dist >= 0:
            # Return the barrier's angle minus 90 degrees
            return atan(m) - PI/2
        # Otherwise, the point is counterclockwise from the line with respect to Point 1, so return the barrier's angle plus 90 degrees
        return atan(m) + PI/2
    
    def get_torque_direction(self, robot, edge_id, colliding_id):
        """Returns true if torque must be reversed"""
        robot_corners = robot.get_corners()
        colliding_corner = self.get_corners()[colliding_id]
        colliding_edge = robot.get_lines()[edge_id]
        x = colliding_corner[0]
        y = colliding_corner[1]
        x1 = colliding_edge.x1
        y1 = colliding_edge.y1
        x2 = colliding_edge.x2
        y2 = colliding_edge.y2
        
        if x2 == x1:
            x2 += 0.0001
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m*x1
        
        y_dist = m*x + b - y
        closer_p1 = (x - x1)**2 + (y - y1)**2 > (x - x2)**2 + (y - y2)**2
        
        if (closer_p1 and x1 >= x2) or (not closer_p1 and x1 < x2):
            return y_dist < 0
        return y_dist >= 0
        # # Get mid-lines of robot to split it into quadrants
        # xC = robot.x
        # yC = robot.y
        # x01 = (robot_corners[0][0] + robot_corners[1][0]) / 2
        # y01 = (robot_corners[0][1] + robot_corners[1][1]) / 2
        
        # if x01 == xC:
        #     x01 += 0.0001
        # m1 = (y01 - yC) / (x01 - xC)
        # b1 = yC - m1*xC
        
        # if y01 == yC:
        #     y01 += 0.0001
        # m2 = -(x01 - xC) / (y01 - yC)
        # b2 = yC - m2*xC
        
        # # Get y-distances from midlines to (x, y) to determine which quadrant (x, y) is in
        # y_dist_l1 = m1*x + b1 - y
        # y_dist_l2 = m2*x + b2 - y
        
        # if y_dist_l1 >= 0 and y_dist_l2 >= 0:
        #     quadrant = 0
        # elif y_dist_l1 < 0 and y_dist_l2 >= 0:
        #     quadrant = 1
        # elif y_dist_l1 < 0 and y_dist_l2 < 0:
        #     quadrant = 2
        # elif y_dist_l1 >= 0 and y_dist_l2 < 0:
        #     quadrant = 3
        
        # # If distance from (x, y) to first midline is greater than half the robot's height, then (x, y) is colliding along the side of the robot
        # dist_l1_sqr = (y_dist_l1)**2 / (m1**2 + 1)
        # if dist_l1_sqr > (robot.h / 2)**2:
        #     along_side = True
        # else:
        #     along_side = False
        
        # # Torque must be reversed if colliding along the robot's side in Quadrants 1 and 3, or if not colliding along the robot's side in Quadrants 0 and 2
        # return ((quadrant == 1 or quadrant == 3) and along_side) or ((quadrant == 0 or quadrant == 2) and not along_side)