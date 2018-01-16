from barrier import Barrier

class Cube:
    # Constants
    FRICTION = 0.95
    cubeimg = loadImage("../Assets/Images/Field/cube.png")
    
    def __init__(self, img = cubeimg, x = 100.0, y = 100.0, angle = 0, speed = 0):
        """Initiates the instance of Cube.
        Will create a power cube at [100, 100] that is unmoving unless otherwise specified"""
        self.x = x
        self.y = y
        self.img = img
        self.speed = 0
        self.angle = angle
        
    def draw(self):
        """Draws the instance of Cube"""
        pushMatrix() # Save the empty transform matrix in the stack so that it can be restored for next Robot instance 
        image(self.img, self.x, self.y)
        print(x,y)