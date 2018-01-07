class Robot:
    # Parameters
    x = 0.0
    y = 0.0
    vel = 0
    dir = 0
    
    # Internal Usage
    robotColor = 0x000000
    
    # Constants
    RWIDTH = 28
    RHEIGHT = 33
    ACCEL = 0.30
    DECEL = 0.93
    ANGACCEL = PI/60
    
    # States
    isAccel = False
    isDecel = False
    isTurnL = False
    isTurnR = False
    
    
    def __init__(self, x, y, dir, isBlue):
        self.x = x
        self.y = y
        self.vel = 0
        self.dir = dir
        
        if isBlue:
            self.robotColor = 0x0191FF
        else:
            self.robotColor = 0xED1C24
    
    def getCorners(self):
        rW = self.RWIDTH
        rH = self.RHEIGHT
        dir = self.dir
        x = self.x
        y = self.y
        return [[rW*cos(dir+PI/2)+rH*cos(dir)+x, rW*sin(dir+PI/2)+rH*sin(dir)+y],
                [rW*cos(dir-PI/2)+rH*cos(dir)+x, rW*sin(dir-PI/2)+rH*sin(dir)+y],
                [rW*cos(dir-PI/2)-rH*cos(dir)+x, rW*sin(dir-PI/2)-rH*sin(dir)+y],
                [rW*cos(dir+PI/2)-rH*cos(dir)+x, rW*sin(dir+PI/2)-rH*sin(dir)+y]]
    
    def display(self):
        self.moveRobot()
        
        fill(self.robotColor)
        stroke(0)
        strokeWeight(1)
        
        C = self.getCorners()
        quad(C[0][0], C[0][1], C[1][0], C[1][1], C[2][0], C[2][1], C[3][0], C[3][1])
        
    def moveRobot(self):
        if self.isAccel:
            self.vel += self.ACCEL
        if self.isDecel:
            self.vel -= self.ACCEL
        self.vel *= self.DECEL
        
        if self.isTurnR:
            self.dir += self.ANGACCEL
        if self.isTurnL:
            self.dir -= self.ANGACCEL
        
        self.x += self.vel*cos(self.dir)
        self.y += self.vel*sin(self.dir)