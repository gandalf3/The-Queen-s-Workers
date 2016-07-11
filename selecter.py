from bge import logic, render
from mathutils import geometry, Vector

# from http://blender.stackexchange.com/a/28133/599
# and http://blender.stackexchange.com/a/2156/599

b = None
a_w = None
b_w = None

def get_world_coords(coords):
    cont = logic.getCurrentController()
    ray = cont.sensors["MouseRay"]
    
    ray_start = ray.raySource
    ray_end = ray.rayTarget
    
    plane_origin = Vector((0, 0, 0))
    plane_normal = Vector((0, 0, 1))
    
    intersection = geometry.intersect_line_plane(ray_start, ray_end, plane_origin, plane_normal)
    if intersection:
        return intersection

def box_selection_vis(cont):
    global b
    print("HALLO")
    scene = logic.getCurrentScene()
    cam = scene.active_camera
    own = cont.owner

    click = cont.sensors["MouseClick"]
    
    if click.positive:
        if own['held']:
            a = Vector(logic.mouse.position)
            
            print("draw")
            draw_box(a, b)
        else:
            a = Vector(logic.mouse.position)
            b = a.copy()
            own['held'] = True
        

    else:
        if own['held']:
            own['held'] = False
            
            
def box_selection(cont):
    global b_w
    global a_w
    scene = logic.getCurrentScene()
    cam = scene.active_camera
    own = cont.owner

    click = cont.sensors["MouseClick"]
    
    if click.positive:
        if own['held']:
            a_w = get_world_coords(Vector(logic.mouse.position))
            
        else:
            a_w = get_world_coords(Vector(logic.mouse.position))
            b_w = a_w.copy()
            own['held'] = True
        

    else:
        if own['held']:
            print("select")
            select_inside(a_w, b_w)
            own['held'] = False


def  select_inside(a, b):

    p1 = Vector((a.x, a.y))
    p2 = Vector((b.x, a.y))
    p3 = Vector((b.x, b.y))
    p4 = Vector((a.x, b.y))

    scene = logic.getCurrentScene()
    cam = scene.active_camera

    for obj in scene.objects:
        if geometry.intersect_point_quad_2d(obj.worldPosition.xy, p1, p2, p3, p4):
            print("selected", obj)
            


def draw_box(a, b):
    color = (1,1,1)
    
    print(a, b)
    
    a = a.copy()
    b = b.copy()
    
    a.x = a.x*16 - 8
    b.x = b.x*16 - 8
    a.y = a.y*9 - 4.5
    b.y = b.y*9 - 4.5
    
    a.y *= -1
    b.y *= -1
    
    print(a, b)

    p1 = Vector((a.x, a.y)).to_3d()
    p2 = Vector((b.x, a.y)).to_3d()
    p3 = Vector((b.x, b.y)).to_3d()
    p4 = Vector((a.x, b.y)).to_3d()


    render.drawLine(p1, p2, color)
    render.drawLine(p2, p3, color)
    render.drawLine(p3, p4, color)
    render.drawLine(p4, p1, color)