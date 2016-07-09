import bge
from mathutils import Vector, Euler
from ant import Ant
import random


def can_place(own):
    
    detector = bge.logic.getCurrentScene().addObject("Large_clearance_detector", own)
    
    #print(detector.sensors["TileCollision"].status)
    
    if detector.sensors["TileCollision"].positive:
        print("something is in the way")
        #detector.endObject()
        return False
    elif detector.sensors["PropCollision"].positive:
        for o in detector.sensors["PropCollision"].hitObjectList:
            print("removing grass")
            o.endObject()
        #detector.endObject()
        return True
    else:
        #detector.endObject()
        return True


def spawn_object(cont, obj, coords, check=True):
    own = cont.owner
    oldpos = own.worldPosition.copy()
    own.worldPosition = coords
    
    canplace = False
    
    if 0: # disable checking for available space for the moment, need to do this over multiple logic ticks it seems
        if check:
            if can_place(own):
                canplace = True
        else:
            canplace = True
    else:
        canplace = True
        
        
    if canplace:
        ob = bge.logic.getCurrentScene().addObject(obj, own)
        ob.worldOrientation.rotate(Euler((0, 0, random.random() * 360)))
        own.worldPosition = oldpos
        return ob
    else:
        own.worldPosition = oldpos
        return False
    
    

def scatter_resources(cont):
    own = cont.owner
    
    #for i in range(0, random.randint(3, 8)):
        #add_food()
        
    #for i in range(0, random.randint(6, 12)):
        #add_rock()
        
    for i in range(0, random.randint(3, 20)):
        tile = Vector(( random.randint(-128, 128), random.randint(-128, 128) ))

        spawn_object(cont, random.choice(["Rock1", "Rock2", "Rock3"]), tile.to_3d())
        
    for i in range(0, random.randint(300, 400)):
        tile = Vector(( random.randint(-128, 128), random.randint(-128, 128) ))

        spawn_object(cont, "Grass patch 1", tile.to_3d())
    
    
def spawn_queen():
    own = cont.owner
    
    print("spawning queen")
    own.worldPosition = Vector((0, 0, 0))
    
    queen = bge.logic.getCurrentScene().addObject("Queen ant mesh")
    Ant(queen)
    
def spawn_worker(cont):
    own = cont.owner
    if own.sensors[0].positive:
        worker = bge.logic.getCurrentScene().addObject("Armature")
        

def initialize(cont):
    own = cont.owner
    
    bge.logic.addScene('GUI')
    
    bge.logic.globalDict["food"] = 50
    bge.logic.globalDict["material"] = 50
    bge.logic.globalDict["science"] = 0
    
    bge.logic.globalDict["max_food"] = 100
    bge.logic.globalDict["max_material"] = 100
    bge.logic.globalDict["max_science"] = 100
    
    bge.logic.globalDict["day_offset"] = bge.logic.getRealTime()
    bge.logic.globalDict["day"] = 0
    
    bge.logic.sendMessage("GUI")
    
    #spawn_queen(cont)
    scatter_resources(cont)
    
def increment_day():
    day = bge.logic.getRealTime() - bge.logic.globalDict["day_offset"]
    bge.logic.globalDict["day"] = day
    
    yday = int(day % 365)
    
    
    if yday >= int(365/4 * 3):
        bge.logic.sendMessage("season_update", "winter")
        bge.logic.globalDict["season"] = "Winter"
    elif yday >= int(365/4 * 2):
        bge.logic.sendMessage("season_update", "fall")
        bge.logic.globalDict["season"] = "Fall"
    elif yday >= int(365/4):
        bge.logic.sendMessage("season_update", "summer")
        bge.logic.globalDict["season"] = "Summer"
    elif yday < int(365/4):
        bge.logic.sendMessage("season_update", "spring")
        bge.logic.globalDict["season"] = "Spring"