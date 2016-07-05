import bge
from mathutils import Vector
import random

class Ant(bge.types.KX_GameObject):
    
    def __init__(self, own):
        #self.task = "collect food"
        self.pathing_target = bge.logic.getCurrentScene().objects["target"].worldPosition
        
        self.vision_distance = 5
        
        self.acceleration = .005
        self.max_speed = .1
        #self.max_turning_speed
        
        self.speed = 0
        
        #self.forward = self.worldOrientation.inverted_safe()[1]
        
    def accelerate(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration
    
            
    def decelerate(self, urgency):
        self.speed -= self.acceleration * urgency
    
    
    def look_for_obstacles(self):
        
        here = self.worldPosition
        ahead = self.worldPosition + self.forward * self.vision_distance
        bge.render.drawLine(here, ahead, (1, 0, 1))
        obstacle = self.rayCastTo(ahead, self.vision_distance, "obstacle")
        if obstacle:
            return obstacle
        else:
            return None
            
    
    def steer(self, direction):
        self.alignAxisToVect(direction, 1, .08)
    
    def move(self):
        self.worldPosition += self.forward * self.speed
        
    def main(self):
        
        # insist upon being level at all times
        self.alignAxisToVect(Vector((0,0,1)), 2)
        
        dist, vect, lvect = self.getVectTo(self.pathing_target)
        self.forward = self.getAxisVect(Vector((0, 1, 0)))
        print(self.forward)
        #print()
        
        ob = self.look_for_obstacles()
        if ob:
            dist, go_around, l = self.getVectTo(ob)
            go_around.z = 0
            bge.render.drawLine(self.worldPosition, self.worldPosition - go_around, (0, 1, 0))
            self.steer(-go_around)
        else:
            self.steer(vect)
            
        
        self.accelerate()
        
        self.move()
        


def main(cont):
    own = cont.owner
    
    if "ant_init" not in own:
        own = Ant(own)
        own["ant_init"] = True
    else:
        own.main()