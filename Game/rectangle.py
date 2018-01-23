from barrier import Barrier

class Rectangle:
    def get_corners(self):
        """Returns rectangle corners as a list of 4 tuples"""
        w = self.w
        h = self.h
        x = self.x
        y = self.y
        
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        
        # Get x and  y distances from robot center to corners
        dx1 = (w/2) * cos_a - (h/2) * sin_a
        dy1 = (w/2) * sin_a + (h/2) * cos_a
        dx2 = (w/2) * cos_a + (h/2) * sin_a
        dy2 = (w/2) * sin_a - (h/2) * cos_a
        
        # Return corner coordinates with respect to origin
        return [(x + dx1, y + dy1), (x + dx2, y + dy2), (x - dx1, y - dy1), (x - dx2, y - dy2)]
    
    def get_lines(self):
        """Returns edges of robot as a list of 4 barriers"""
        c = self.get_corners()
        return [Barrier(c[0][0], c[0][1], c[1][0], c[1][1]),
                Barrier(c[1][0], c[1][1], c[2][0], c[2][1]),
                Barrier(c[2][0], c[2][1], c[3][0], c[3][1]),
                Barrier(c[3][0], c[3][1], c[0][0], c[0][1])]
    
    def is_colliding(self, object):
        """Returns if rectangle is colliding with barrier"""
        if isinstance(object, Barrier):
            for edge in self.get_lines():
                if edge.is_colliding(object):
                    return True
            return False
        elif isinstance(object, Rectangle):
            for edge in object.get_lines():
                if self.is_colliding(edge):
                    return True
            return False
            
    def get_normal_angle(self, barrier):
        """Returns the normal angle to a barrier, used in collision math"""
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