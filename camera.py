import bge

bge.render.showMouse(True)

win_x = bge.render.getWindowWidth()
win_y = bge.render.getWindowHeight()

mouse_x = int(win_x/2)
mouse_y = int(win_y/2)

bge.render.setMousePosition(mouse_x, mouse_y)

#def distance(a, b, c=0):
#    """
#    get distance between a and either b or c (whichever is closer)
#    """
#    if abs(a - b) < abs(a - c):
#        return abs(a - b)
#    else:
#        return abs(a - c)
    

def pan(cont):
    own = cont.owner

    mouse_sens = own.sensors['Mouse']
    mouse_w_up = own.sensors['MouseWUp']
    mouse_w_down = own.sensors['MouseWDown']
    
    mouse_pos = mouse_sens.position
    
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    
    x_margin = win_x/7
    y_margin = win_y/7
    
    
    if (mouse_x > win_x - x_margin):
        own.worldPosition.x += abs(mouse_x - (win_x - x_margin)) * .005
    elif (mouse_x < x_margin):
        own.worldPosition.x -= abs(mouse_x - x_margin) * .005
        
    if (mouse_y > win_y - y_margin):
        own.worldPosition.y -= abs(mouse_y - (win_y - y_margin)) * .005
    elif (mouse_y < y_margin):
        own.worldPosition.y += abs(mouse_y - y_margin) * .005
    
    