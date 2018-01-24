from barrier import Barrier
from rectangle import Rectangle

class Cube(Rectangle):
    # Constants
    FRICTION = 0.93
    PLACED_FRICTION = 0.75
    SIDE_LENGTH = 39.0
    COLOR = color(227, 251, 42)
    PLACED_COLOR = color(224, 211, 38)

    def __init__(self, x = 100.0, y = 100.0, angle = 0.0, speed = 0.0, placed = False):
        super(Cube, self).__init__(float(x), float(y), Cube.SIDE_LENGTH, Cube.SIDE_LENGTH, angle, speed, self.COLOR)
        self.placed = placed
        
    def draw(self, barriers, robots):
        """Draws the instance of Cube"""
        self.move_cube()
        
        # # Collision detection
        # for barrier in barriers:
        #     if self.is_colliding(barrier):
        #         normal_angle = self.get_normal_angle(barrier)
        #     while self.is_colliding(barrier):
        #         self.speed *= self.FRICTION
        #         self.x += cos(normal_angle)
        #         self.y += sin(normal_angle)
        
        # for robot in robots:
        #     for edge in robot.get_lines():
        #         if self.is_colliding(edge):
        #             normal_angle = self.get_normal_angle(edge)
        #         while self.is_colliding(edge):
        #             self.speed *= self.FRICTION
        #             self.x += cos(normal_angle)
        #             self.y += sin(normal_angle)
        
        # Puts draw functions (e.g., rect(), ellipse()) into cube's reference frame to make drawing easier
        pushMatrix() # Save the empty transform matrix in the stack so that it can be restored for next Robot instance 
        
        if not self.placed:
            fill(self.color)
        elif self.placed:
            fill(Cube.PLACED_COLOR)
        stroke(0)
        strokeWeight(2)
        
        translate(self.x, self.y)
        rotate(self.angle)
        
        rect(-self.w/2, -self.h/2, self.w, self.h, 3)
        
        popMatrix()
    
    def move_cube(self):
        if not self.placed:
            self.speed *= Cube.FRICTION
        elif self.placed:
            self.speed *= Cube.PLACED_FRICTION
        self.x += self.speed * cos(self.angle)
        self.y += self.speed * sin(self.angle)