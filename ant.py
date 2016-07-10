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
        self.target = Vector((0, 0, 0))
        
        self.vision_distance = 5
        self.stopping_margin = 1.3
        
        self.acceleration = .005
        self.max_speed = .1
        #self.max_turning_speed
        self.near_sens = self.sensors["Near"]
        
        self.zoffset = self.worldPosition.copy().z
        
        self.nearest_ant = 100
        
        self.speed = 0
        self.target_direction = Vector((0, -1, 0))
        self.direction = self.getAxisVect((0,-1,0))
        
        
        
    def towards_target(self):
        dist, vect, lvect = self.getVectTo(self.target.to_3d())
        
        vect.normalize()

        if dist < self.vision_distance:
            # apply braking force proportional to distance
            vect = vect - (vect * min((dist/-self.vision_distance) + 1/self.vision_distance + self.stopping_margin, 1))
        else:
            # apply acceleration
            pass
        
        return vect
    
    
    def around_obstacles(self):
        
        here = self.worldPosition
        ahead = self.worldPosition + self.direction * self.vision_distance
        
        obstacle = self.rayCastTo(ahead, self.vision_distance, "obstacle")
        if obstacle:
            dist, go_around, l = self.getVectTo(obstacle)
            go_around.z = 0
            
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
            self.playAction("antwalking", 0, 12)
            
        self.setActionFrame(self.getActionFrame()+self.direction.length)
        
        if not self.direction.length < 0.000001:
            self.alignAxisToVect(-self.direction, 1)
        self.worldPosition += self.direction * self.max_speed
        
    def main(self):
        # insist upon being at ground level at all times
        obj, hitpoint, normal = self.rayCast(self.worldPosition + Vector((0,0,-1)), self.worldPosition + Vector((0,0,1)), 10, "Ground", 0, 1)
        self.worldPosition.z = hitpoint.z + self.zoffset
        self.alignAxisToVect(normal, 2)
        
        #self.accelerate()
        
        bge.render.drawLine(self.worldPosition, self.target.to_3d(), (1, 1, 1))
        
        o = self.around_obstacles()
        t = self.towards_target()
        s = self.separate()
        
        self.target_direction = o + t + s
        self.target_direction.normalize()
        
        bge.render.drawLine(self.worldPosition, self.worldPosition + self.target_direction*10, (1, 0, 0))
        
        self.direction = self.direction.lerp(self.target_direction, .05)
        
        self.move()
        


def main(cont):
    own = cont.owner
    
    if "ant_init" not in own:
        own = Ant(own)
        own["ant_init"] = True
    else:
        own.main()