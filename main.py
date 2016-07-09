import bge
from mathutils import Vector, Euler
from ant import Ant
from detector import Detector
import random

# Lists of resource tile models
# please do add the name of new models to the appropriate list

rocks = [
"bouldertiles",
"bouldertiles (variant)",
"pebblestiles"
]

clay = [
"claytiles"
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
        
        # leave a clearing in the center of the map
        if tile.length > 15:
            d = spawn_object(cont, "Large_clearance_detector", tile.to_3d())
            Detector(d, random.choice(tiles))

def scatter_resources(cont):
    own = cont.owner
    
    
    spawn_resource(["Rock1", "Rock2", "Rock3"], 10, 20)
    
    spawn_resource(["Grass patch 1_mesh"], 300, 400)
    
    spawn_resource(["Rock1", "Rock2", "Rock3"], 10, 20)
    
    spawn_resource(["Rock Small1", "Rock Small2", "Rock Small3"], 30, 40)
    
    if bge.logic.globalDict["primary_food"] == "honey":
        spawn_resource(honey, 20, 30)
        spawn_resource(leaves, 2, 5)
    else:
        spawn_resource(leaves, 20, 30)
        spawn_resource(honey, 2, 5)
        
    spawn_resource(roots, 20, 30)
    spawn_resource(fossils, 2, 7)
    spawn_resource(water, 30, 40)
    
    
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
    
    # Refresh resourcecounts
    bge.logic.sendMessage("GUI")
    
    bge.logic.globalDict["primary_food"] = random.choice(["honey", "leaves"])
    
    scatter_resources(cont)
    #spawn_queen(cont)
    
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