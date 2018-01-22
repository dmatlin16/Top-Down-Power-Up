from barrier import Barrier

class Cube:
    # Constants
    FRICTION = 0.93
    COLOR = color(227, 251, 42)
    
    def __init__(self, x = 100.0, y = 100.0, w = 39, h = 39, angle = 0, speed = 0):
        """Initiates the instance of Cube.
        Will create a power cube at [100, 100] that is unmoving unless otherwise specified"""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.angle = angle
        self.color = Cube.COLOR
        
    def draw(self):
        """Draws the instance of Cube"""
        pushMatrix() # Save the empty transform matrix in the stack so that it can be restored for next Robot instance 
        self.move_cube()
        fill(self.color)
        translate(self.x, self.y)
        rotate(self.angle)
        rect(-self.w/2, -self.h/2, self.w, self.h, 3)
        popMatrix()
    
    def move_cube(self):
        self.speed *= Cube.FRICTION
        self.x += self.speed * cos(self.angle)
        self.y += self.speed * sin(self.angle)
    
    def get_lines(self):
        """Returns edges of cube as a list of 4 barriers"""
        c = self.get_corners()
        return [Barrier(c[0][0], c[0][1], c[1][0], c[1][1]),
                Barrier(c[1][0], c[1][1], c[2][0], c[2][1]),
                Barrier(c[2][0], c[2][1], c[3][0], c[3][1]),
                Barrier(c[3][0], c[3][1], c[0][0], c[0][1])]
    
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