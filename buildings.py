import bge
from resources import increase_resource
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
            if bge.logic.globalDict["food"] > 5:
                bge.logic.globalDict["food"] -= 5
                bge.logic.sendMessage("GUI")
                spawn_worker(cont)
            
            
        
def honeyden(cont):
    own = cont.owner
    sens = cont.sensors[0]
    
    if random.random() < own["efficiency"]*.08:
        if own["stored"] > 1/own["efficiency"]:
            own["stored"] -= 1/own["efficiency"]

            increase_resource(own, "food")

def farm(cont):
    own = cont.owner
    sens = cont.sensors[0]
    
    if random.random() < own["efficiency"]*.09:
        if own["stored"] > 1/own["efficiency"]:
            own["stored"] -= 1/own["efficiency"]

            increase_resource(own, "food")
