from bge import logic, render
from mathutils import Vector

# from http://blender.stackexchange.com/a/28133/599
# and http://blender.stackexchange.com/a/2156/599

b = None

def box_selection(cont):
    global b
    scene = logic.getCurrentScene()
    cam = scene.active_camera
    own = cont.owner

    click = cont.sensors["MouseClick"] 


    if click.positive:
        if own['held']:
            a = Vector(logic.mouse.position)
            
            a_t = cam.camera_to_world * a.to_3d()
            b_t = cam.camera_to_world * b.to_3d()
            draw_box(a_t, b_t)
        else:
            a = Vector(logic.mouse.position)
            b = a.copy()
            own['held'] = True
        

    else:
        if own['held']:
            print("select")
            #select_inside(own['m_x_old'],own['m_y_old'],own['m_x_new'],own['m_y_new'])
            own['held'] = False


def  select_inside(p1_x,p1_y, p2_x,p2_y):

    if p1_x > p2_x :
        p = p2_x
        p2_x = p1_x
        p1_x = p

    if p1_y > p2_y :
        p = p2_y
        p2_y = p1_y
        p1_y = p

    scene = logic.getCurrentScene()
    cam = scene.active_camera

    for obj in scene.objects :
        if 'Select' in obj.getPropertyNames() :
            print('select found!', obj.name)
            pos = cam.getScreenPosition(obj)
            x = pos[0] * render.getWindowWidth()
            y = pos[1] * render.getWindowHeight()
            if x > p1_x and y > p1_y and x < p2_x and y < p2_y :
                print('obj inside')
                obj['Select'] = True


def draw_box(a, b):  # there is some distortion in the drawing
    color = (1,1,1)
    
    print(a, b)

    p1 = Vector((a.x, a.y)).to_3d()
    p2 = Vector((b.x, a.y)).to_3d()
    p3 = Vector((b.x, b.y)).to_3d()
    p4 = Vector((a.x, b.y)).to_3d()


    render.drawLine(p1, p2, color)
    render.drawLine(p2, p3, color)
    render.drawLine(p3, p4, color)
    render.drawLine(p4, p1, color)