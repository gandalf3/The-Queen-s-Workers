import bge
from mathutils import Vector
from ant import Ant
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



#def snap_coords_to_grid(coords):
    

def scatter_resources(cont):
    own = cont.owner
    
    main_foodsource = random.choice(['honey', 'leaves'])
    
    r_tile = Vector(( random.randint(0, 256), random.randint(0, 256) ))
    
    
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
    
    bge.logic.sendMessage("GUI")
    
    spawn_queen(cont)
    
    
    
