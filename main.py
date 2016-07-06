import bge
from mathutils import Vector
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
    
    

 
def initialize(cont):
    own = cont.owner
    
    bge.logic.addScene('GUI')
    
    bge.logic.globalDict["food"] = 500
    bge.logic.globalDict["material"] = 50
    bge.logic.globalDict["science"] = 0
    
    bge.logic.globalDict["max_food"] = 500
    bge.logic.globalDict["max_material"] = 500
    bge.logic.globalDict["max_science"] = 500
    
    print("sending message")
    bge.logic.sendMessage("GUI")
    
    
    
