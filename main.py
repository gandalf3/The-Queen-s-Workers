import bge
from mathutils import Vector, Euler
from ant import Ant
from detector import Detector
import random

# Lists of resource tile models
# please do add the name of new models to the appropriate list

rocks = [
"bouldertiles",
"bouldertiles (variant)"
]

clay = [
"claytiles",
"pebblestiles"
]

fossils = [
"fossiltiles"
]

honey = [
"honeytiles",
"honeytiles (variant)"
]

leaves = [
"leaftiles"
]

roots = [
"roottiles"
]

water = [
"watertiles"
]

def spawn_object(cont, obj, coords,):
    own = cont.owner
    oldpos = own.worldPosition.copy()
    own.worldPosition = coords
    
    ob = bge.logic.getCurrentScene().addObject(obj, own)
    ob.worldOrientation.rotate(Euler((0, 0, random.random() * 360)))
    own.worldPosition = oldpos

    return ob

def spawn_resource(tiles, min_amount, max_amount):
    cont = bge.logic.getCurrentController()
    
    for i in range(0, random.randint(min_amount, max_amount)):
        tile = Vector(( random.randint(-128, 128), random.randint(-128, 128) ))
        
        # leave a clearing in the center of the map, but offset
        if (tile - Vector((0,-6))).length > 14:
            d = spawn_object(cont, "Large_clearance_detector", tile.to_3d())
            Detector(d, random.choice(tiles), i)

def scatter_resources(cont):
    own = cont.owner
    own["elapsed"] = own.get("elapsed", 0) + 1
    
    if own["elapsed"] == 1:
        spawn_resource(["Rock1", "Rock2", "Rock3", "Suzock"], 40, 60)
        bge.logic.sendMessage("loadprogress", str(.1))
    
    if own["elapsed"] == 2:
        spawn_resource(["Grass patch 1", "Grass patch 2"], 400, 600)
        bge.logic.sendMessage("loadprogress", str(.2))

    if own["elapsed"] == 3:
        spawn_resource(["Rock Small1", "Rock Small2", "Rock Small3", "Rock Small4", "Rock Small5", "Rock Small6"], 100, 200)
        bge.logic.sendMessage("loadprogress", str(.3))

    if own["elapsed"] == 4:
        spawn_resource(["acorn"], 10, 20)
        bge.logic.sendMessage("loadprogress", str(.4))

    if own["elapsed"] == 5:
        if bge.logic.globalDict["primary_food"] == "honey":
            spawn_resource(honey, 20, 30)
            spawn_resource(leaves, 2, 5)
        else:
            spawn_resource(leaves, 20, 30)
            spawn_resource(honey, 2, 5)
        bge.logic.sendMessage("loadprogress", str(.5))
    
    if own["elapsed"] == 6:
        spawn_resource(clay, 50, 80)
        bge.logic.sendMessage("loadprogress", str(.6))

    if own["elapsed"] == 7:
        spawn_resource(roots, 20, 30)
        bge.logic.sendMessage("loadprogress", str(.7))

    if own["elapsed"] == 8:
        spawn_resource(fossils, 2, 7)
        bge.logic.sendMessage("loadprogress", str(.8))

    if own["elapsed"] == 9:
        spawn_resource(water, 30, 40)
        bge.logic.sendMessage("loadprogress", str(.9))
    
    if own["elapsed"] == 10:
        spawn_resource(["Grass patch 1", "Grass patch 2"], 400, 600)
        bge.logic.sendMessage("loadprogress", str(1))

    if own["elapsed"] >= 12:
        if "Large_clearance_detector" not in bge.logic.getCurrentScene().objects:
            bge.logic.sendMessage("loaded")
        

def spawn_queen(cont):
    own = cont.owner
    
    print("spawning queen")
    own.worldPosition = Vector((0, 0, 0))
    
    queen = bge.logic.getCurrentScene().addObject("Ant")
    Ant(queen)
    
def spawn_worker(cont):
    own = cont.owner
    worker = Ant(bge.logic.getCurrentScene().addObject("Ant"))
    worker.target = own.worldPosition + Vector((0, -3, 0))
    
def spawn_den(cont):
    own = cont.owner
    den = bge.logic.getCurrentScene().addObject("Plane.002", own)
    
    ground, hitpoint, normal = own.rayCast(own.worldPosition + Vector((0,0, -10)), own.worldPosition + Vector((0, 0, 10)), 30, "Ground", 1, 1)
    if hitpoint:
        den.worldPosition = hitpoint
        den.alignAxisToVect(normal, 2)
            
    den.localOrientation.rotate(Euler((0, 0, random.random() * 360)))
        

def initialize(cont):
    own = cont.owner
    sens = cont.sensors[0]
    if sens.positive:
        
        bge.logic.addScene('GUI')
        
        bge.logic.globalDict["food"] = 50
        bge.logic.globalDict["material"] = 50
        bge.logic.globalDict["science"] = 0
        bge.logic.globalDict["pop"] = len(Ant.antlist)
        
        bge.logic.globalDict["foodworkers"] = 0
        bge.logic.globalDict["materialworkers"] = 0
        bge.logic.globalDict["scienceworkers"] = 0
        
        bge.logic.globalDict["max_food"] = 50
        bge.logic.globalDict["max_material"] = 50
        bge.logic.globalDict["max_science"] = 100
        bge.logic.globalDict["max_pop"] = 0
        
        bge.logic.globalDict["day_offset"] = bge.logic.getRealTime()
        bge.logic.globalDict["day"] = 0
        bge.logic.globalDict["season"] = "Spring"
        
        # Refresh resourcecounts
        bge.logic.sendMessage("GUI")
        
        bge.logic.globalDict["primary_food"] = random.choice(["honey", "leaves"])
        
        #scatter_resources(cont)
        
        #spawn_queen(cont)
        
        spawn_worker(cont)
        
        spawn_den(cont)
    
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
        if bge.logic.globalDict["season"] != "Spring":
            bge.logic.sendMessage("season_update", "spring")
            bge.logic.globalDict["season"] = "Spring"
        
        
            # regenerate resources
            bge.logic.globalDict["primary_food"] = random.choice(["honey", "leaves"])
            
            if bge.logic.globalDict["primary_food"] == "honey":
                spawn_resource(honey, 20, 30)
                spawn_resource(leaves, 2, 5)
            else:
                spawn_resource(leaves, 20, 30)
                spawn_resource(honey, 2, 5)
                
            spawn_resource(clay, 50, 80)
            spawn_resource(roots, 20, 30)
            spawn_resource(fossils, 2, 7)
            
            spawn_resource(["Grass patch 1", "Grass patch 2"], 100, 150)
        
        
