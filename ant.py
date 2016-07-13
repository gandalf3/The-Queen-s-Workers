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
        
        # DROP: drop off self.carrying at an appropriate building
        # GOGET: go to self.collect
        # GOTO: go to self.target
        # GOBACK: go to 0,0
        self.mode = "GOTO"
        
        self.idle = True
        
        self.target = Vector((0, 0))

        self.collect = None
        # useful to store this in case self.collect becomes invalid due to being used up
        self.collect_category = None
        
        self.carrying = None
        self.carry_type = None
        self.carry_category = None
        
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
        self.return_home_timer = None
    
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
            self.carrying = None
            
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
    
    
    def update_workercount(self, recount=False):
        gd = bge.logic.globalDict
        
        if recount:
            gd["foodworkers"] = 0
            gd["materialworkers"] = 0
            gd["scienceworkers"] = 0
            gd["idleworkers"] = 0
            
            for ant in Ant.antlist:
                if collect:
                    gd[category + "workers"] += 1
                else:
                    gd["idleworkers"] += 1
                    
        else:
            if self.collect:
                gd[self.collect["category"] + "workers"] += 1
            else:
                gd["idleworkers"] += 1
                    
        bge.logic.sendMessage("GUI")
    
    
    def go_to(self, coords):
        self.target = coords.copy()
        self.mode = "GOTO"
        
    
    def go_get(self, obj):
        if self.carrying is not None:
            # need to drop something off first
            self.go_drop()
            if obj is not None:
                self.collect = obj
        else:
            if obj is not None:
                self.collect = obj
                self.target = self.collect.worldPosition.copy()
                self.mode = "GOGET"
            else:
                self.collect = None
                self.collect_category = None
                self.go_back()
                
        
        self.update_workercount()
        
            
    def go_back(self):
        self.return_home_timer = 0
        self.go_to(Vector((0,-3,0)))
        
        
    def go_drop(self):
        # determine nearest possible dropoff point
        destination = None
        if self.carry_type == "leaf":
            destination = self.find_nearest(['Farm'])
        elif self.carry_type == "honey":
            destination = self.find_nearest(['Honey Den'])    
        else:
            destination = self.find_nearest(['Storage', 'Den'])
        
        # if there's no special buildings to deliver to, a generic one will do    
        if destination is None:
            destination = self.find_nearest(['Storage', 'Den'])
        
        # if *still* none we now have a real problem
        if destination is None:
            bge.logic.sendMessage("notify", "Nowhere to store resources!!")
        
        self.destination = destination
        self.target = self.destination.worldPosition.copy()
        self.mode = "DROP"
        
        
    def main(self):
        scene = bge.logic.getCurrentScene()
        
        # check for invalid gameobject references
        if self.collect is not None and self.collect.invalid:
            self.collect = None
        if self.destination is not None and self.destination.invalid:
            self.destination = None
        
        # order taking
        if not scene.objects["Placement_Empty"]['BuildModeActive']:
            if self["selected"]:
                if self.sensors["Click"].positive:
                    if self.sensors["CanGo"].positive:
                        
                        obj, hitPoint, normal = self.rayCast(self.sensors["CanGo"].rayTarget, self.sensors["CanGo"].raySource, 300)
                        
                        # only resources have a "points" property
                        if "points" in obj:
                            print("You clicked a Resource!")
                            self.go_get(obj)

                        else:
                            self.go_to(self.sensors["CanGo"].hitPosition)
                    
        
        # decision making
        
        if self.mode == "GOTO":
            if self.return_home_timer is not None:
                #counting away the ticks
                self.return_home_timer -= 1
            
            #have we arrived (away from home)?
            if (Vector((0,-3,0)) - self.target).length > 1.5:
                
                if (self.worldPosition - self.target).length < 1.5:
                    if self.return_home_timer is not None and self.return_home_timer < 1:
                        self.target = Vector((0,-3,0))
                        self.return_home_timer = None
                    elif self.return_home_timer is None:
                        self.return_home_timer = 60 * 10
                    
        
        elif self.mode == "GOGET":
            # is there still something to collect?
            if self.collect is not None:
                # go get resource
                if (self.worldPosition - self.collect.worldPosition).length < 1.5:
                    print("picking up resource")
                        
                    if self.collect["points"] > 0:
                        self.collect["points"] -= 1
                        
                        self.carry_type = self.collect["type"]
                        self.carry_category = self.collect["category"]
                        self.carrying = scene.addObject(self.carry_type + "fragment", self)
#                        if self.collect_type == "honey":
#                            print("replacing mesh")
#                            self.replaceMesh("Cube.001")
                    
                    # if we grabbed the last one, make resource vanish
                    if self.collect["points"] <= 0:
                        print("resource run out")
                
                        self.collect.parent.endObject()
                        self.collect.endObject()
                        
                    self.go_drop()
                        
            else:
                #send him back
                self.update_workercount(recount=True)
                self.go_get(None)
                
            
        elif self.mode == "DROP":
            # return with resource
            if (self.worldPosition - self.destination.worldPosition).length < 1.5:
                print("turning in resource")
                
                if self.collect_category == "food":
                    if "stored" in self.destination:
                        self.destination['stored'] += 1
                    else:
                        increase_resource(self, "food")
                else:
                    increase_resource(self, self.carry_category)
                
                if self.carrying:
                    self.carrying.endObject()
                    self.carrying = None
                
                # go back for more
                self.go_get(self.collect)
                
            
        elif self.mode == "GOBACK":
            # if resource is gone but we still are carrying some around
            if self.carrying is not None:
                self.mode = "DROP"
            
        if self.carrying is not None and not self.carrying.invalid:
            self.carrying.worldPosition = self.worldPosition                

        
        
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