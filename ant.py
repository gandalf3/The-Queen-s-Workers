import bge
from mathutils import Vector
import random

class Unit(bge.types.KX_GameObject):
    
    def __init__(self, own):
        pass
        
    def select(self):
        pass
        

class Ant(bge.types.BL_ArmatureObject):
    
    def __init__(self, own):
        
        # Tasks
        
        # Go here
        # Stay here
        
        #self.task = 
        
        # modes:
        # DO_NOTHING
        # GOTO
        # WORK
        self.mode = "GOTO"
        self.target = Vector((10, 3))
        
        self.vision_distance = 5
        
        self.acceleration = .005
        self.max_speed = .1
        #self.max_turning_speed
        self.near_sens = bge.logic.getCurrentController().sensors["Near"]
        
        self.speed = 0
        
        self.velocity = Vector((0, 0, 0))
        
    def accelerate(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration
    
            
    def decelerate(self, urgency):
        self.speed -= self.acceleration * urgency
        
        
    def towards_target(self):
        dist, vect, lvect = self.getVectTo(self.target.to_3d())
        return vect
    
    
    def around_obstacles(self):
        
        here = self.worldPosition
        ahead = self.worldPosition + self.velocity * self.vision_distance
        bge.render.drawLine(here, ahead, (1, 0, 1))
        obstacle = self.rayCastTo(ahead, self.vision_distance, "obstacle")
        if obstacle:
            dist, go_around, l = self.getVectTo(obstacle)
            go_around.z = 0
            bge.render.drawLine(self.worldPosition, self.worldPosition - go_around, (0, 1, 0))
            
            return -go_around
        
        else:
            return Vector((0,0,0))
        
    def separate(self):
        print(self.near_sens.hitObjectList)
        
    
    def move(self):
        if not self.isPlayingAction():
#            print("starting walkcycle", self)
            self.playAction("antwalking", 0, 12)
            
        self.worldPosition += self.velocity
        
    def main(self):
        # insist upon being level at all times
        self.alignAxisToVect(Vector((0,0,1)), 2)
        
        self.alignAxisToVect(-self.velocity, 1)
        
        self.accelerate()
        
        o = self.around_obstacles()
        t = self.towards_target()
        self.separate()
        
        self.velocity = o + t
        self.velocity.normalize()
        self.velocity *= self.speed
        
        self.move()
        


def main(cont):
    own = cont.owner
    
    if "ant_init" not in own:
        own = Ant(own)
        own["ant_init"] = True
    else:
        own.main()