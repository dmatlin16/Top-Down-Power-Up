import random
from barrier import Barrier
from cube import Cube
from rectangle import Rectangle

class Robot(Rectangle):
    # Constants
    ACCEL = 0.30
    FRICTION = 0.95
    ANGACCEL = PI/60
    RED = color(237, 28, 36)
    BLUE = color(1, 145, 255)

    def __init__(self, color = RED, x = 0.0, y = 0.0, w = 98, h = 83, angle = 0, speed = 0):
        """Initiates a robot instance.
        Will create a red robot at [0, 0] with a width of 33 inches and a height of 28 inches (max robot dimensions) that is unmoving
        and facing right unless otherwise specified"""
        super(Robot, self).__init__(x, y, w, h, angle, speed, color)
        self.accel = False
        self.decel = False
        self.turn_l = False
        self.turn_r = False
        self.has_cube = False
        self.intake_raise = False
        self.intake_height = 0
        self.climber_raise = False
        self.climb_height = 0
        self.score = 0
        
    def draw(self, barriers, robots, cubes, scale_plates):
        """Draws the instance of Robot"""
        self.move_robot()
        self.move_intake()
        self.climb_robot()

        # Collision detection
        for barrier in barriers:
            if self.is_colliding(barrier):
                normal_angle = self.get_normal_angle(barrier)
            while self.is_colliding(barrier):
                self.speed *= self.FRICTION
                self.x += cos(normal_angle)
                self.y += sin(normal_angle)

        for plate in scale_plates:
            for edge in plate.get_lines():
                if self.intake_height > 0 and self.is_colliding(edge):
                    normal_angle = self.get_normal_angle(edge)
                while self.intake_height > 0 and self.is_colliding(edge):
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
                        self.x += cos(normal_angle) / 2
                        self.y += sin(normal_angle) / 2
                        robot.x -= cos(normal_angle) / 2
                        robot.y -= sin(normal_angle) / 2
        
        # Puts draw functions (e.g., rect(), ellipse()) into robot's reference frame to make drawing easier
        pushMatrix() # Save the empty transform matrix in the stack so that it can be restored for next Robot instance 
        
        fill(self.color)
        stroke(0)
        strokeWeight(2)
        
        translate(self.x, self.y)
        rotate(self.angle)
        
        rect(-self.w/2, -self.h/2, self.w, self.h, 3)
        
        # If robot is holding a cube, render that cube
        rectMode(CENTER)
        if self.has_cube:
            fill(Cube.COLOR)
        else:
            fill(self.color)
        rect(20, 0, 39 + self.intake_height / 10, 39 + self.intake_height / 10)
        rectMode(CORNER)
        
        # Render indicator light
        if self.intake_height == 0:
            fill(color(0))
        elif self.intake_height == 100:
            fill(color(255))
        else:
            fill(self.color)
        
        if self.climb_height == 0:
            pass
        elif self.climb_height == 100:
            fill(color(0, 255, 0))
        else:
            fill(color(255, 255, 0))
        ellipse(-30, 0, 10, 10)

        popMatrix() # Restores reference frame to empty transform matrix by popping modified matrix off the stack

    def move_robot(self):
        if self.climb_height == 0:
            if self.accel:
                self.speed += self.ACCEL
            if self.decel:
                self.speed -= self.ACCEL
            self.speed *= self.FRICTION
    
            if self.turn_r:
                self.angle += self.ANGACCEL
            if self.turn_l:
                self.angle -= self.ANGACCEL
                    
            self.x += self.speed * cos(self.angle) * (1 - 0.005 * self.intake_height)
            self.y += self.speed * sin(self.angle) * (1 - 0.005 * self.intake_height)
    
    def intake(self, cubes, plates, scale_plates, robots):
        front_edge = self.get_lines()[0]
        
        if not self.has_cube and self.intake_height == 0:
            for cube in list(reversed(cubes)):
                if cube.is_colliding(front_edge) and cube.placed == False:
                    cube.x = 1000000.0
                    cube.y = 1000000.0
                    self.has_cube = True
                    if (self.color == self.RED and cube.side == "blue") or (self.color == self.BLUE and cube.side == "red"):
                        for robot in robots:
                            if not robot is self:
                                robot.score += 5
                    break
        
        elif self.has_cube:
            mid_x = front_edge.get_mid()[0]
            mid_y = front_edge.get_mid()[1]
            cube_x = mid_x + 19.5 * cos(self.angle)
            cube_y = mid_y + 19.5 * sin(self.angle)
            placed = False
            for plate in plates:
                left = plate.x - plate.w / 2
                right = plate.x + plate.w / 2
                top = plate.y - plate.h / 2
                bottom = plate.y + plate.h / 2
                space = Cube.SIDE_LENGTH / 2
                if cube_x > left and cube_x < right and cube_y > top and cube_y < bottom:
                    if cube_x - left < space:
                        cube_x = left + space
                    if right - cube_x < space:
                        cube_x = right - space
                    if cube_y - top < space:
                        cube_y = top + space
                    if bottom - cube_y < space:
                        cube_y = bottom - space
                    
                    if plate in scale_plates and self.intake_height < 100:
                        placed = False
                    else:
                        placed = True
                        center_y = 476.5
                        plate.mass += abs((center_y - cube_y) / 160.0)
                        
            cubes.append(Cube(cube_x, cube_y, self.angle, self.speed, placed = placed))
            self.has_cube = False
            self.intake_raise = False
    
    def elevator(self):
        self.intake_raise = not self.intake_raise
    
    def move_intake(self):
        if self.intake_raise and self.intake_height < 100:
            self.intake_height += 1
        elif not self.intake_raise and self.intake_height > 0:
            self.intake_height -= 1
    
    def portal(self, portal_count, cubes, in_auto):
        if not in_auto:
            y = self.y
            top_y = 43.0
            bottom_y = 910.0
            
            rand_angle = random.uniform(-PI/12, PI/12)
            rand_speed = random.uniform(0, 2)
            
            if self.color == self.RED:
                # If closer to top portal, try to spawn cube in upper right
                if abs(y - top_y) < abs(y - bottom_y):
                    if portal_count["red"]["top"] > 0:
                        portal_count["red"]["top"] -= 1
                        cubes.append(Cube(1854, 59, 2.262 + rand_angle, rand_speed))
    
                # Otherwise, try to spawn cube in lower right
                else:
                    if portal_count["red"]["bottom"] > 0:
                        portal_count["red"]["bottom"] -= 1
                        cubes.append(Cube(1854, 894, -2.262 + rand_angle, rand_speed))
            
            elif self.color == self.BLUE:
                # If closer to top portal, try to spawn cube in upper left
                if abs(y - top_y) < abs(y - bottom_y):
                    if portal_count["blue"]["top"] > 0:
                        portal_count["blue"]["top"] -= 1
                        cubes.append(Cube(66, 59, 0.880 + rand_angle, rand_speed))
                # Otherwise, try to drop a cube in the lower left
                else:
                    if portal_count["blue"]["bottom"] > 0:
                        portal_count["blue"]["bottom"] -= 1
                        # spawn lower left
                        cubes.append(Cube(66, 894, -0.880 + rand_angle, rand_speed))

    def climber(self):
        if self.climber_raise:
            self.climber_raise = False
        else:
            front_edge = self.get_lines()[0]
            mid_x = front_edge.get_mid()[0]
            mid_y = front_edge.get_mid()[1]
            
            self.climber_raise = 926 < mid_x and mid_x < 995 and 468 < mid_y and mid_y < 485
    
    def climb_robot(self):
        if self.climber_raise and self.climb_height < 100:
            self.climb_height += 1
        elif not self.climber_raise and self.climb_height > 0:
            self.climb_height -= 1