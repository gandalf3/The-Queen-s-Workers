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
        self.max_speed = 10
        #self.max_turning_speed
        self.near_sens = bge.logic.getCurrentController().sensors["Near"]
        
        self.speed = 0
        
        self.nearest_ant = 100
        
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
        
        for ant in self.near_sens.hitObjectList:
            if ant not in self.children:
                vect = (self.worldPosition - ant.worldPosition)
                if vect.length < self.nearest_ant:
                    self.nearest_ant = vect.length
        
        if self.nearest_ant < 2 and vect:
            bge.render.drawLine(self.worldPosition, self.worldPosition - vect, (1, 0, 0))
            self.nearest_ant = 100
            return vect
        else:
            return Vector((0,0,0))

        
        
    
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
        s = self.separate()
        
        new_velocity = o + t + s
        new_velocity.normalize()
        new_velocity *= .1
        
        if self.velocity == Vector((0,0,0)):
            self.velocity = new_velocity
        else:    
            self.velocity.lerp(new_velocity, .7)
        
        self.move()
        


def main(cont):
    own = cont.owner
    
    if "ant_init" not in own:
        own = Ant(own)
        own["ant_init"] = True
    else:
        own.main()