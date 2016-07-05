import bge
import mathutils
from math import sqrt
from utils import clamp, lerp


## TODO
# refactor to use a class object (get rid of globals)
# use vector from center to cursor to control pan direction
# investigate using "pressure" to control pan speed in some way; else use timer to slowly speed up
# adjust pan speed based on resolution as well

# for debugging
bge.render.showMouse(True)

# number of steps of zoom
zoom_steps = 7
# lowest allowed camera altitude in BU
max_zoom = 3
# highest allowed camera altitude in BU
min_zoom = 90
# initial zoom level
zoom_level = 4

# inertia settings
acceleration = .01
damping = .96
edge_time = 1


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

def zoom_to_altitude(zoom_level):
    global acceleration
    acceleration = pow(clamp(zoom_level/zoom_steps, .3) * sqrt(.03), 2)
    
    return pow(zoom_level/zoom_steps * sqrt(min_zoom-max_zoom), 2) + max_zoom

target_altitude = zoom_to_altitude(zoom_level)

def zoom(cont):
    global zoom_level, target_altitude
    own = cont.owner
    
    mouse_w_up = own.sensors['MouseWUp']
    mouse_w_down = own.sensors['MouseWDown']
    
    if mouse_w_up.positive:
        zoom_level = clamp(zoom_level-1, 0, 7)
        target_altitude = zoom_to_altitude(zoom_level)
        
    elif mouse_w_down.positive:
        zoom_level = clamp(zoom_level+1, 0, 7)
        target_altitude = zoom_to_altitude(zoom_level)
        
    own.worldPosition.z = lerp(own.worldPosition.z, target_altitude, .1)
    

def pan(cont):
    global edge_time
    own = cont.owner

    mouse_sens = own.sensors['Mouse']    
    mouse_pos = mouse_sens.position
    
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
  
    
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
    
    #print(edge_time)
    own.worldPosition.x += momentum.x
    own.worldPosition.y += momentum.y
    