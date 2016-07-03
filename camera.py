import bge
import mathutils


## TODO
# refactor to use a class object (get rid of globals)
# use vector from center to cursor to control pan direction
# investigate using "pressure" to control pan speed in some way; else use timer to slowly speed up
# use smooth zooming
# adjust pan speed based on zoom (pan slower when closer)


# for debugging
bge.render.showMouse(True)

# on a scale from 0-9
zoom_level = 5

# inertia settings
acceleration = .01
damping = .96
margin = 10
edge_time = 1

margin /= 100
initial_height = bge.logic.getCurrentController().owner.worldPosition.z

win_x = bge.render.getWindowWidth()
win_y = bge.render.getWindowHeight()

bge.render.setMousePosition(int(win_x/2), int(win_y/2))

#def distance(a, b, c=0):
#    """
#    get distance between a and either b or c (whichever is closer)
#    """
#    if abs(a - b) < abs(a - c):
#        return abs(a - b)
#    else:
#        return abs(a - c)

momentum = mathutils.Vector((0,0))

def zoom(cont):
    global zoom_level
    own = cont.owner
    
    mouse_w_up = own.sensors['MouseWUp']
    mouse_w_down = own.sensors['MouseWDown']
    
    if mouse_w_up.positive:
        zoom_level -= 1
    elif mouse_w_down.positive:
        zoom_level += 1
        
    own.worldPosition.z = initial_height + zoom_level * 10
    

def pan(cont):
    global edge_time
    own = cont.owner

    mouse_sens = own.sensors['Mouse']    
    mouse_pos = mouse_sens.position
    
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    
    x_margin = win_x * margin
    y_margin = win_y * margin
  
    
    if (mouse_x > win_x):
        contact = True
        momentum.x += edge_time * acceleration
        edge_time += 1 * acceleration
        
    elif (mouse_x < 0):
        contact = True
        momentum.x -= edge_time * acceleration
        edge_time += 1 * acceleration

        
    if (mouse_y > win_y):
        contact = True
        momentum.y -= edge_time * acceleration
        edge_time += 1 * acceleration
        
    elif (mouse_y < 0):
        contact = True
        momentum.y += edge_time * acceleration
        edge_time += 1 * acceleration
        
#    if contact:
#        edge_time = 1
    
    momentum.x *= damping
    momentum.y *= damping
    
    print(edge_time)
    own.worldPosition.x += momentum.x
    own.worldPosition.y += momentum.y
    