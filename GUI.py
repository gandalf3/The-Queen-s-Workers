import bge

bge.render.showMouse(True)

def fix_text():
    objs = bge.logic.getCurrentScene().objects
    for o in objs:
        try:
            o.resolution = 1.25
        except AttributeError:
            pass


def update_resource_meters():
    objs = bge.logic.getCurrentScene().objects
    
    gd = bge.logic.globalDict
    
    food_p = gd["food"]/gd["max_food"]
    material_p = gd["material"]/gd["max_material"]
    science_p = gd["science"]/gd["max_science"]

    objs['Food_meter'].localScale.x = min(food_p, 1)
    objs['Materials_meter'].localScale.x = min(material_p, 1)
    objs['Science_meter'].localScale.x = min(science_p, 1)

    objs['Food_amount'].text = "{}/{}".format(int(gd["food"]), int(gd["max_food"]))
    objs['Material_amount'].text = "{}/{}".format(int(gd["material"]), int(gd["max_material"]))
    objs['Science_amount'].text = "{}/{}".format(int(gd["science"]), int(gd["max_science"]))
    
    objs['Food_worker_count'].text = "{}".format(int(gd["foodworkers"]))
    objs['Material_worker_count'].text = "{}".format(int(gd["materialworkers"]))
    objs['Science_worker_count'].text = "{}".format(int(gd["scienceworkers"]))

def update(cont):
    sens = cont.owner.sensors["Message"]
    
    # We should potentially check if we have actually added an ant; however, it isn't cirtical
    # A quick check could be to compare the value of Ant_count.text against the current property
    bge.logic.getCurrentScene().objects['Ant_count'].text = "{}/{}".format(bge.logic.globalDict["pop"],bge.logic.globalDict["max_pop"])
    
    if sens.positive:
        update_resource_meters()
        
def datestring(cont):
    own = cont.owner
    
    d = bge.logic.globalDict["day"]
    s = bge.logic.globalDict["season"]
    
    own.text = "Day {} Year {} - {}".format(int(d % 365), int(d/365), s)
