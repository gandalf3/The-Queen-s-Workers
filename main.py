import bge
from mathutils import Vector
from ant import Ant
import random




#def snap_coords_to_grid(coords):


    

def scatter_resources(cont):
    own = cont.owner
    
    
    
    tile = Vector(( random.randint(0, 256), random.randint(0, 256) ))
    
    
def spawn_queen(cont):
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