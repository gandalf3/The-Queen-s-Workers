import bge

control = bge.logic.getCurrentScene().objects["GUI_control"]

def main(cont):
    own = cont.owner
    mouseover = own.sensors["MouseOver"]
    mouseclick = own.sensors["MouseClick"]
    
    if mouseover.hitObject == own and mouseclick.positive:
        # spawn popup offscreen so it can transition onscreen smoothly
        control.worldPosition.y += 10
        bge.logic.getCurrentScene().addObject("Build_popup_menu", control)
        control.worldPosition.y -= 10