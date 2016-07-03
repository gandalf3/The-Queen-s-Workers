import bge

def main():
    scenelist = bge.logic.getSceneList()
    cont = bge.logic.getCurrentController()
    
    overlay = scenelist[1]
    objects = overlay.objects
    mouseOver = cont.sensors['Mouse']
    display = objects['MouseDisplay']
    backdrop = objects['Backdrop']
    
    if mouseOver.positive:
        moused = mouseOver.hitObject
        display['Text'] = moused['id']
        display.visible = True
        backdrop.visible = True
        backdrop.worldPosition = mouseOver.hitPosition
    else:
        display.visible = False
        backdrop.visible = False