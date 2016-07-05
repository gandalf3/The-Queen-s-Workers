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
    
    
    
    

def main(cont):
    own = cont.owner
    
    
