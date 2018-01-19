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
        
        # Avoid division by 0
        if x1 == x2:
            x2 += 0.0001
        
        # Get equation of self (y = mx + b), m is slope, b is y-intercept
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1*x1
        
        # Collisions between two lines
        if isinstance(barrier, BarrierLine):
            x3 = barrier.x1
            y3 = barrier.y1
            x4 = barrier.x2
            y4 = barrier.y2
        
            # Calculate line equation for other barrier
            if x3 == x4:
                x4 += 0.0001
            
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
        
        # Collisions between a line and a circle
        elif isinstance(barrier, BarrierCircle):
            x3 = barrier.x
            y3 = barrier.y
            r = barrier.r
            
            # Get equations of lines perpendicular to self going through (x1, y1) and (x2, y2)
            if y1 == y2:
                y2 += 0.0001
            m_perp = -(x2 - x1) / (y2 - y1)
            b1_perp = y1 - m_perp*x1
            b2_perp = y2 - m_perp*x2
            
            # Get distances from the point to the perpendicular lines going through (x1, y1) and (x2, y2), squared to avoid sqrt()
            d1_perp_sqr = (m_perp*x3 + b1_perp - y3)**2 / (m_perp**2 + 1)
            d2_perp_sqr = (m_perp*x3 + b2_perp - y3)**2 / (m_perp**2 + 1)
            
            # Get distances from (x1, y1) and (x2, y2) to the point
            d1_sqr = (x1 - x3)**2 + (y1 - y3)**2
            d2_sqr = (x2 - x3)**2 + (y2 - y3)**2
            
            # If the point intersects with the line segment, see if there is an intersection point
            len_sqr = (y2 - y1)**2 + (x2 - x1)**2
            if (d1_perp_sqr <= len_sqr and d2_perp_sqr <= len_sqr) or d1_sqr <= r**2 or d2_sqr <= r**2:
                # Find intersection point of circle and line by solving a quadratic equation: ax^2 + bx + c = 0
                # If the discriminant >= 0, then there is a solution and the two shapes intersect
                # (x - x3)^2 + (y - y3)^2 - r^2 = 0
                # (x - x3)^2 + (m1*x + b1-y3)^2 - r^2 = 0
                a = 1 + m1**2 
                b = -2*x3 + 2*m1*(b1-y3)
                c = x3**2 + (b1-y3)**2 - r**2
                return (b**2 - 4*a*c) >= 0 
            return False
            
class BarrierCircle:
    def __init__(self, x, y, r, visible = False):
        self.x = float(x)
        self.y = float(y)
        self.r = float(r)
        self.visible = visible
        
    def draw(self):
        if self.visible:
            ellipse(self.x, self.y, 2 * self.r, 2 * self.r)     