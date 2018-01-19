class BarrierLine:
    def __init__(self, x1, y1, x2, y2, visible = False):
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.visible = visible
    
    def draw(self):
        if self.visible:
            line(self.x1, self.y1, self.x2, self.y2)
            
    
    def is_colliding(self, barrier):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        if isinstance(barrier, BarrierLine):
            x3 = barrier.x1
            y3 = barrier.y1
            x4 = barrier.x2
            y4 = barrier.y2
        
        # Avoid division by 0
        if x1 == x2:
            x2 += 0.0001
        if x3 == x4:
            x4 += 0.0001
        
        # Get equations of both lines (y = mx + b), m is slope, b is y-intercept
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1*x1
        m3 = (y4 - y3) / (x4 - x3)
        b3 = y3 - m3*x3
    
        # If lines are parallel, return if they have the same y-intercept
        if m1 == m3:
            return b1 == b3
        
        # Find intersection point of both lines
        xInt = (b3 - b1) / (m1 - m3)
        yInt = m1*xInt + b1
        
        # Return true if intersection point is on both line segments
        onL1x = (x1 <= xInt and xInt <= x2) or (x1 >= xInt and xInt >= x2)
        onL1y = (y1 <= yInt and yInt <= y2) or (y1 >= yInt and yInt >= y2)
        onL2x = (x3 <= xInt and xInt <= x4) or (x3 >= xInt and xInt >= x4)
        onL2y = (y3 <= yInt and yInt <= y4) or (y3 >= yInt and yInt >= y4)
        return onL1x and onL1y and onL2x and onL2y

class BarrierCircle:
    def __init__(self, x, y, r, visible = False):
        self.x = x
        self.y = y
        self.r = r
    def draw(self):
        if self.visible:
            ellipse(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)        