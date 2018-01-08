class Robot:
    # Internal Usage
    robot_color = 0x000000
    
    # Constants
    RWIDTH = 28
    RHEIGHT = 33
    ACCEL = 0.30
    DECEL = 0.93
    ANGACCEL = PI/60
    
    # States
    is_accel = False
    is_decel = False
    is_turn_l = False
    is_turn_r = False
    
    
    def __init__(self, x = 0.0, y = 0.0, vel = 0, theta = 0, is_blue = True):
        self.x = x
        self.y = y
        self.vel = 0
        self.theta = theta
        
        if is_blue:
            self.robot_color = color(1, 145, 255)
        else:
            self.robot_color = color(237, 28, 36)
    
    def get_corners(self):
        w = self.RWIDTH
        h = self.RHEIGHT
        theta = self.theta
        x = self.x
        y = self.y
        return [[w * cos(theta + PI / 2) + h * cos(theta) + x, w * sin(theta + PI / 2) + h * sin(theta) + y],
                [w * cos(theta - PI / 2) + h * cos(theta) + x, w * sin(theta - PI / 2) + h * sin(theta) + y],
                [w * cos(theta - PI / 2) - h * cos(theta) + x, w * sin(theta - PI / 2) - h * sin(theta) + y],
                [w * cos(theta + PI / 2) - h * cos(theta) + x, w * sin(theta + PI / 2) - h * sin(theta) + y]]
    
    def display(self):
        fill(self.robot_color)
        self.move_robot()
        stroke(0)
        strokeWeight(1)
        
        c = self.get_corners()
        quad(c[0][0], c[0][1], c[1][0], c[1][1], c[2][0], c[2][1], c[3][0], c[3][1])
        ellipse(self.x + cos(self.theta) * 25, self.y + sin(self.theta) * 25, 7, 7) # Temporary circle to show which side is front
        
    def move_robot(self):
        if self.is_accel:
            self.vel += self.ACCEL
        if self.is_decel:
            self.vel -= self.ACCEL
        self.vel *= self.DECEL
        
        if self.is_turn_r:
            self.theta += self.ANGACCEL
        if self.is_turn_l:
            self.theta -= self.ANGACCEL
        
        self.x += self.vel*cos(self.theta)
        self.y += self.vel*sin(self.theta)