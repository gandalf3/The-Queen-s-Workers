import bge
from mathutils import Vector, noise
from math import sqrt
from utils import clamp, lerp


## TODO
# refactor to use a class object (get rid of globals)
# use vector from center to cursor to control pan direction
# investigate using "pressure" to control pan speed in some way; else use timer to slowly speed up
# adjust pan speed based on resolution as well

# number of steps of zoom
zoom_steps = 7
# lowest allowed camera altitude in BU
max_zoom = 4
# highest allowed camera altitude in BU
min_zoom = 40
# initial zoom level
zoom_level = 2



# inertia settings

acceleration = .01

# speed at min_zoom
max_speed = 2.5

# speed at max_zoom
min_speed = .3

damping = .94

edge_time = 0
# time needed to reach full pan speed
acceleration_time = 30 # in logic ticks

pan_speed = .03

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

momentum = Vector((0,0))

def zoom_to_altitude(zoom_level):
    global pan_speed
    own = bge.logic.getCurrentController().owner
    
    pan_speed = ((own.worldPosition.z-max_zoom)/(min_zoom-max_zoom)*(max_speed-min_speed))+min_speed
    
    return pow(zoom_level/zoom_steps * sqrt(min_zoom-max_zoom), 2) + max_zoom

target_altitude = zoom_to_altitude(zoom_level)

def zoom(cont):
    global zoom_level, target_altitude
    own = cont.owner
    #zoom_level = own["zoom_level"]
    
    mouse_w_up = own.sensors['MouseWUp']
    mouse_w_down = own.sensors['MouseWDown']
    
    if mouse_w_up.positive:
        zoom_level = clamp(zoom_level-1, 0, 7)
        target_altitude = zoom_to_altitude(zoom_level)
        
    elif mouse_w_down.positive:
        zoom_level = clamp(zoom_level+1, 0, 7)
        target_altitude = zoom_to_altitude(zoom_level)
        
    own.worldPosition.z = lerp(own.worldPosition.z, target_altitude, .1)
    
    
def get_pan_speed(edge_time):
    return min(pow(edge_time/30, 2), 1) * pan_speed

def pan(cont):
    global edge_time, momentum
    own = cont.owner

    #mouse_sens = own.sensors['Mouse']
    #mouse = Vector(mouse_sens.position)
    mouse = Vector(bge.logic.mouse.position)
    
    contact = False
    
    if (mouse.x >= .95):
        contact = True
        edge_time += 1
        
    elif (mouse.x <= .05):
        contact = True
        edge_time += 1
    
        
    if (mouse.y >= .95):
        contact = True
        edge_time += 1
        
    elif (mouse.y <= .05):
        edge_time += 1
        contact = True
        
    if contact:
        target_momentum = (mouse - Vector((.5,.5))) * get_pan_speed(edge_time)
        target_momentum.y *= -1
        
        momentum = momentum.lerp(target_momentum, .1)
    else:
        edge_time = 0
    
    momentum *= damping
    own.worldPosition.xy += momentum.xy
    
def auto_pan(cont):
    own = cont.owner
    
    
    target = bge.logic.getCurrentScene().objects["end_cam_placeholder"]
    
    own.worldPosition = own.worldPosition.lerp(target.worldPosition, own["pan_urgency"])
    own.worldOrientation = own.worldOrientation.lerp(target.worldOrientation, own["pan_urgency"])
    
def shake(cont):
    own = cont.owner
    
    t = bge.logic.getRealTime()
    n = noise.random_unit_vector()

    own.worldPosition = own.worldPosition + n*own["shake_amount"]
    