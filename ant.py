import bge
from resources import increase_resource
from mathutils import Vector, noise
import random

class Unit(bge.types.KX_GameObject):
    
    def __init__(self, own):
        pass
        
    def select(self):
        pass
        

class Ant(bge.types.BL_ArmatureObject):
    
    antlist = []
    
    def __init__(self, own):
        self["ant_init"] = True
        Ant.antlist.append(self)
        
        bge.logic.globalDict["pop"] = len(Ant.antlist)
        
        
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

        self.collect = None
        self.collect_type = None
        self.collect_type = None
        
        self.carrying = None
        self.destination = None
        
        self.vision_distance = 5
        self.stopping_margin = .5
        
        self.acceleration = .005
        self.max_speed = .1
        #self.max_turning_speed
        self.near_sens = self.sensors["Near"]
        
        self.zoffset = self.worldPosition.copy().z
        
        self.nearest_ant = 100
        
        self.speed = 0
        self.target_direction = Vector((0, -1, 0))
        self.direction = self.getAxisVect((0,-1,0))
        
        #self.wander_direction = Vector((.5,.5))
        
        self.currently_considering = 0
        
        self.ticks_since_last_meal = random.randint(0, 600)
        
    
    def eat(self):
        if self.ticks_since_last_meal > 900:
            print(bge.logic.globalDict["food"])
            if bge.logic.globalDict["food"] > 0:
                bge.logic.globalDict["food"] -= 1
                bge.logic.sendMessage("GUI")

                self.ticks_since_last_meal = 0
            else:
                # go without food
                self.ticks_since_last_meal = 0
                if random.random() < .3:
                    bge.logic.sendMessage("notify", "An ant starved!")
                    self.die()
                else:
                    bge.logic.sendMessage("notify", "An ant is hungry")

        self.ticks_since_last_meal += 1
        
    def die(self):
        if self.carrying is not None:
            self.carrying.endObject()
            
        for o in self.children:
            o.endObject()
            
        Ant.antlist.remove(self)
        
        bge.logic.globalDict["pop"] = len(Ant.antlist)
        bge.logic.sendMessage("GUI")
        self.endObject()
        
    def towards_target(self):
        dist, vect, lvect = self.getVectTo(self.target.to_3d())
        
        vect.normalize()

        if dist < self.vision_distance:
            # apply braking force proportional to distance
            vect = vect - (vect * min((dist/-self.vision_distance) + 1/self.vision_distance + self.stopping_margin, 1))
            self.stopping_margin = min(self.stopping_margin +.01, 1)
        else:
            self.stopping_margin = .5
            pass
        
        return vect
    
    
    def around_obstacles(self):
        
        here = self.worldPosition
        ahead = self.worldPosition + self.direction * self.vision_distance
        
        obstacle = self.rayCastTo(ahead, self.vision_distance, "obstacle")
        if obstacle:
            #print("watch out", obstacle)
            dist, go_around, l = self.getVectTo(obstacle)
            
            if dist < self.vision_distance:
                # apply braking force proportional to distance
                go_around = go_around - (go_around * min((dist/-self.vision_distance) + 1/self.vision_distance + self.stopping_margin, 1))
            
            return -go_around
        
        else:
            return Vector((0,0,0))
        
    def separate(self):
        
        # in case of death
        if len(Ant.antlist) <= self.currently_considering:
            self.currently_considering = 0
            
        if Ant.antlist[self.currently_considering] != self:
            next_ant = Ant.antlist[self.currently_considering]
        else:
            self.currently_considering = (self.currently_considering + 1) % len(Ant.antlist)
            next_ant = Ant.antlist[self.currently_considering]
        
        dist, vect, lvect = self.getVectTo(next_ant)
        
        if dist < self.nearest_ant:
            self.nearest_ant = dist
        
        self.currently_considering = (self.currently_considering + 1) % len(Ant.antlist)
        
        if self.nearest_ant < .5 and vect:
            #bge.render.drawLine(self.worldPosition, self.worldPosition + vect*10 , (.3, 0, 1))
            self.nearest_ant = 100
            return -vect
        else:
            return Vector((0,0,0))
        
    def wander(self):
        t = bge.logic.getRealTime()
        v = Vector((t, t, t)) + self.worldPosition
        n = noise.noise_vector(v)
        
        #return self.wander_direction
        return n.to_2d()
        
    
    def move(self):
        if not self.isPlayingAction():
            self.playAction("antwalking", 0, 12, 0, 0, 0, bge.logic.KX_ACTION_MODE_LOOP)
        
        self.setActionFrame((self.getActionFrame()+self.direction.length)%12)
        
        if not self.direction.length < 0.000001:
            self.alignAxisToVect(-self.direction, 1)
        
        self.worldPosition += self.direction * self.max_speed
        
        
    def find_nearest(self, ids):
        nearest_dist = 300
        nearest_dest = None
        for dest in bge.logic.getCurrentScene().objects:
            for id in ids:
                if dest.get("id", None) == id:
                    dist = (dest.worldPosition - self.worldPosition).length
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest_dest = dest

        return nearest_dest
        
    def main(self):
        scene = bge.logic.getCurrentScene()
        
        # order taking
        if not scene.objects["Placement_Empty"]['BuildModeActive']:
            if self["selected"]:
                if self.sensors["Click"].positive:
                    if self.sensors["CanGo"].positive:
                        
                        obj, hitPoint, normal = self.rayCast(self.sensors["CanGo"].rayTarget, self.sensors["CanGo"].raySource, 300)

                        if "points" in obj:
                            print("You clicked a Resource!")
                            self.collect = obj
                            self.target = self.collect.worldPosition.copy()
                            
                            self.collect_type = self.collect["type"]
                            self.collect_category = self.collect["category"]

                            bge.logic.globalDict[self.collect_category + "workers"] += 1
                            bge.logic.sendMessage("GUI")
                            
                        else:
                            if self.collect is not None:
                                self.collect = None
                            
                                if self.carrying is not None:
                                    self.carrying.endObject()
                                    self.carrying = None
                                    
                                bge.logic.globalDict[self.collect_category + "workers"] -= 1
                                bge.logic.sendMessage("GUI")
                                
                            self.target = self.sensors["CanGo"].hitPosition
                    
        
        # decision making
        
        # is there something to collect?
        if self.collect is not None and not self.collect.invalid:
            
            if self.carrying is not None:
                
                self.carrying.worldPosition = self.worldPosition
                
                # return with resource
                if (self.worldPosition - self.destination.worldPosition).length < 1.5:
                    print("turning in resource")
                    
                    if self.collect_category == "food":
                        if "stored" in self.destination:
                            self.destination['stored'] += 1
                        else:
                            increase_resource(self, "food")
                    else:
                        increase_resource(self, self.collect_category)

                    self.carrying.endObject()
                    self.carrying = None
                    
                    if self.collect:
                        self.target = self.collect.worldPosition.copy()

            else: 
                # go get resource
                if (self.worldPosition - self.collect.worldPosition).length < 1.5:
                    print("picking up resource")
                        
                    if self.collect["points"] > 1:
                        self.collect["points"] -= 1
                        
                        if self.collect_type == "honey":
                            print("replacing mesh")
                            self.replaceMesh("Cube.001")
                        self.carrying = scene.addObject(self.collect_type + "fragment", self)
                        
                    else:
                        print("resource run out")
                        
                        self.collect.parent.endObject()
                        self.collect.endObject()
                        self.collect = None
                        bge.logic.globalDict[self.collect_category + "workers"] -= 1
                    
                    # determine nearest possible dropoff point
                    if self.collect_type == "leaf":
                        self.destination = self.find_nearest(['Farm'])
                    elif self.collect_type == "honey":
                        self.destination = self.find_nearest(['Honey Den'])    
                    else:
                        self.destination = self.find_nearest(['Storage', 'Den'])
                        
                    if self.destination is None:
                        self.destination = self.find_nearest(['Storage', 'Den'])

                    if self.destination is None:
                        bge.logic.sendMessage("notify", "Nowhere to store resources!!")
                    
                    self.target = self.destination.worldPosition.copy()
                    
        else:
            # if resource is gone but we still are carrying some around
            if self.carrying is not None:
                # return with resource
                if (self.worldPosition - self.destination.worldPosition).length < 1.5:
                    print("turning in resource")
                    self.carrying = None
        
        
        # other stuff        
        
        # insist upon being at ground level at all times
        obj, hitpoint, normal = self.rayCast(self.worldPosition + Vector((0,0,-1)), self.worldPosition + Vector((0,0,1)), 10, "Ground", 0, 1)
        self.worldPosition.z = hitpoint.z + self.zoffset
        self.alignAxisToVect(normal, 2)
        
        #self.accelerate()
        
        #bge.render.drawLine(self.worldPosition, self.target.to_3d(), (1, 1, 1))
        
        o = self.around_obstacles()
        t = self.towards_target()
        s = self.separate()
        w = self.wander()
        
        self.target_direction = o.to_2d() + t.to_2d() + s.to_2d()
        self.target_direction = self.target_direction + (w.to_2d() * self.target_direction.length)
        self.target_direction.resize_3d()
        self.target_direction.normalize()
        
        #bge.render.drawLine(self.worldPosition, self.worldPosition + self.target_direction*10, (1, 0, 0))
        
        self.direction = self.direction.lerp(self.target_direction, .05)
        
        self.move()
        self.eat()
        


def main(cont):
    own = cont.owner
    
    if "ant_init" not in own:
        own = Ant(own)
        own["ant_init"] = True
    else:
        own.main()