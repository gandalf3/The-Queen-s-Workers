from selecter import gui_space
import bge

def main(cont):
    own = cont.owner
    hover = cont.sensors["MouseRay"]

    object = hover.hitObject
    if object:
        
        if "tooltip" and "id" in object:
            if own.get("tooltiptime", 0) > 30:
                bge.logic.sendMessage("tooltip", "{}\n{}".format(object["id"], object["tooltip"]))
            else:
                bge.logic.sendMessage("tooltip", object["id"])
                own["tooltiptime"] = own.get("tooltiptime", 0) + 1
                
        elif "tooltip" in object and not "id" in object:
            bge.logic.sendMessage("tooltip", object["tooltip"])
            
        elif "id" in object and not "tooltip" in object:
            bge.logic.sendMessage("tooltip", object["id"])
                
        else:
            own["tooltiptime"] = 0
            bge.logic.sendMessage("notooltip")
        
        if "points" in object:
            for obj in object.children:
                for mesh in obj.meshes:
                    for mat in meshes.materials:
                        mat.emit = 2
                        print("emit")
                        
                        
def tooltip(cont):
    own = cont.owner
    mouseover = cont.sensors["Mouse"]
    appear = cont.sensors["Newtip"]
    disappear = cont.sensors["Notip"]
    scene = bge.logic.getCurrentScene()
    
    if mouseover.positive:
        own["visible_tooltip"] = True
        own["tooltip_text"] = mouseover.hitObject["tooltip"]
        
    elif appear.positive:
        own["visible_tooltip"] = True
        own["tooltip_text"] = appear.bodies[0]
        
    elif disappear.positive:
        own["visible_tooltip"] = False
        
    if own["visible_tooltip"] == True:
        if "tooltip" in scene.objects:
            tooltip = scene.objects["tooltip"]
            tooltip.worldPosition.xy = gui_space(bge.logic.mouse.position)
            tooltip.children["tooltip_text"].text = own["tooltip_text"]
        else:
            tooltip = scene.addObject('tooltip')
            tooltip.worldPosition.xy = gui_space(bge.logic.mouse.position)
            tooltip.children["tooltip_text"].text = own["tooltip_text"]
    else:
        for o in scene.objects:
            if o.name == "tooltip":
                for child in o.children:
                    child.endObject()
                o.endObject()