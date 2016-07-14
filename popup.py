import bge

control = bge.logic.getCurrentScene().objects["GUI_control"]

def on_summon(cont):
    own = cont.owner
    sens = cont.sensors[0]
    
    if sens.positive:
        own.playAction("Build_popup_menu_appear", 0, 10)
        bge.logic.getCurrentScene().addObject("clickblocker", control)
        
def dismiss(cont):
    own = cont.owner
    mouse_over = own.sensors["MouseOver"]
    # dismiss popup if click event is registered *not* over the popup
    if mouse_over.getButtonStatus(bge.events.LEFTMOUSE) == bge.logic.KX_INPUT_JUST_ACTIVATED and not mouse_over.positive:
            own["dismissed"] = True
            own.playAction("Build_popup_menu_dismiss", 0, 10)
            bge.logic.sendMessage("dismiss_clickblocker")
            bge.logic.sendMessage("menu_closed")
        
    # only die after exit animation is done
    if own["dismissed"] == True:
        if not own.isPlayingAction():
            own.endObject()
