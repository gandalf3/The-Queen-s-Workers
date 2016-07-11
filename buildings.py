import bge
from main import spawn_worker
import random

def storage(cont):
    own = cont.owner
    sens = cont.sensors[0]
    
    if sens.positive:
        bge.logic.globalDict["max_food"] += own.children[0]["food_storage"]
        bge.logic.globalDict["max_material"] += own.children[0]["material_storage"]
        
def den(cont):
    own = cont.owner
    sens = cont.sensors[0]
    
    if "den_init" not in own:
        bge.logic.globalDict["max_pop"] += own.children[0]["pop"]
        own["den_init"] = True
        
    if random.random() < .2:
        if bge.logic.globalDict["pop"] < bge.logic.globalDict["max_pop"]:
            print(bge.logic.globalDict["pop"])
            spawn_worker(cont)