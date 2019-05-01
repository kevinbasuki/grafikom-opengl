import glfw
from OpenGL.GL import *
import numpy
from pyrr import matrix44
from Camera import Camera
from ShaderLoader import *
import math

#Constants
TRIANGLE_AMOUNT = 1000
PI = 3.14159265359

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def generateCircleArray(x, y, z, radius, thickness):
    result = []
    for i in range(TRIANGLE_AMOUNT):
        #buat lingkaran
        result.append(x)
        result.append(y)
        result.append(z)
        result.append(x)
        result.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(x)
        result.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))

        #Buat ketebalan
        #segitiga 1
        result.append(x)
        result.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))

        result.append(x)
        result.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        
        result.append(x + thickness)
        result.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        #segitiga 2
        result.append(x + thickness)
        result.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        
        result.append(x + thickness)
        result.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        
        result.append(x)
        result.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        

    result = numpy.array(result, dtype=numpy.float32)
    return result

cam = Camera()
keys = [False] * 1024
lastX, lastY = 640, 360
first_mouse = True

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key >= 0 and key < 1024:
        if action == glfw.PRESS:
            keys[key] = True
        elif action == glfw.RELEASE:
            keys[key] = False


def do_movement():
    if keys[glfw.KEY_W]:
        cam.process_keyboard("FORWARD", 0.05)
    if keys[glfw.KEY_S]:
        cam.process_keyboard("BACKWARD", 0.05)
    if keys[glfw.KEY_A]:
        cam.process_keyboard("LEFT", 0.05)
    if keys[glfw.KEY_D]:
        cam.process_keyboard("RIGHT", 0.05)
    if keys[glfw.KEY_RIGHT]:
        cam.process_mouse_movement(-5,0)
    if keys[glfw.KEY_LEFT]:
        cam.process_mouse_movement(5,0)
    if keys[glfw.KEY_UP]:
        cam.process_mouse_movement(0,-5)
    if keys[glfw.KEY_DOWN]:
        cam.process_mouse_movement(0,5)


def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)


def main():
    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1280, 720
    aspect_ratio = w_width / w_height

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    cube = [
        #Badan Mobil
        #front
        -1.0, -1.0, 1.0,
        1.0, -1.0, 1.0,
        1.0, 1.0, 1.0,
        -1.0, 1.0, 1.0,

        #right
        1.0, -1.0, 1.0,
        1.0, -1.0, -2.0,
        1.0, 1.0, -2.0,
        1.0, 1.0, 1.0,

        #back
        -1.0, -1.0, -2.0,
        1.0, -1.0, -2.0,
        1.0, 1.0, -2.0,
        -1.0, 1.0, -2.0,

        #left
        -1.0, -1.0, 1.0,
        -1.0, -1.0, -2.0,
        -1.0, 1.0, -2.0,
        -1.0, 1.0, 1.0,

        #top
        -1.0, 1.0, 1.0,
        1.0, 1.0, 1.0,
        1.0, 1.0, -2.0,
        -1.0, 1.0, -2.0,

        #bottom
        -1.0, -1.0, 1.0,
        1.0, -1.0, 1.0,
        1.0, -1.0, -2.0,
        -1.0, -1.0, -2.0,

        #Depan Mobil
        #front
        -1.0, -1.0, 2.0,
        1.0, -1.0, 2.0,
        1.0, 0, 2.0,
        -1.0, 0, 2.0,

        #right
        1.0, -1.0, 2.0,
        1.0, -1.0, 1.0,
        1.0, 0, 1.0,
        1.0, 0, 2.0,

        #back
        -1.0, -1.0, 1.0,
        1.0, -1.0, 1.0,
        1.0, 0, 1.0,
        -1.0, 0, 1.0,

        #left
        -1.0, -1.0, 2.0, 
        -1.0, -1.0, 1.0,
        -1.0, 0, 1.0,
        -1.0, 0, 2.0,

        #top
        -1.0, 0, 2.0,
        1.0, 0, 2.0,
        1.0, 0, 1.0,
        -1.0, 0, 1.0,

        #bottom
        -1.0, -1.0, 2.0,
        1.0, -1.0, 2.0, 
        1.0, -1.0, 1.0,
        -1.0, -1.0, 1.0
    ]

    cube = numpy.array(cube, dtype=numpy.float32)
    indices = [
        0,1,2,2,3,0,
        4,5,6,6,7,4,
        8,9,10,10,11,8,
        12,13,14,14,15,12,
        16,17,18,18,19,16,
        20,21,22,22,23,20,

        24,25,26,26,27,24,
        28,29,30,30,31,28,
        32,33,34,34,34,32,
        36,37,38,38,39,36,
        40,41,42,42,43,40,
        44,45,46,46,47,44
    ]

    indices = numpy.array(indices, dtype=numpy.uint32)

    car_program = compile_shader("Shaders/CarShader.vs", "Shaders/CarShader.fs")
    wheel_program = compile_shader("Shaders/WheelShader.vs", "Shaders/WheelShader.fs")
    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    car_model_loc = glGetUniformLocation(car_program, "model")
    car_view_loc = glGetUniformLocation(car_program, "view")
    car_proj_loc = glGetUniformLocation(car_program, "proj")

    wheel_model_loc = glGetUniformLocation(wheel_program, "model")
    wheel_view_loc = glGetUniformLocation(wheel_program, "view")
    wheel_proj_loc = glGetUniformLocation(wheel_program, "proj")
    circle = generateCircleArray(0, 0, 0, 0.4, 0.2)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, circle.itemsize * 3, ctypes.c_void_p(0))
        
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)


    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()
        view = cam.get_view_matrix()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Gambar Roda
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, circle.itemsize * len(circle), circle, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)

        glUseProgram(wheel_program)

        wheel_positions = [(1.0, -1.0, 1.0), (-1.2, -1.0, 1.0), (-1.2, -1.0, -2.0), (1.0, -1.0, -2.0)]

        glUniformMatrix4fv(wheel_proj_loc, 1, GL_FALSE, projection)

        glUniformMatrix4fv(wheel_view_loc, 1, GL_FALSE, view)

        for i in range(len(wheel_positions)):
            wheel_model = matrix44.create_from_translation(wheel_positions[i])
            glUniformMatrix4fv(wheel_model_loc, 1, GL_FALSE, wheel_model)
            glDrawArrays(GL_TRIANGLES, 0, len(circle))


        #Gambar Mobil
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

        # position
        glEnableVertexAttribArray(0)

        glUseProgram(car_program)

        glUniformMatrix4fv(car_proj_loc, 1, GL_FALSE, projection)

        glUniformMatrix4fv(car_view_loc, 1, GL_FALSE, view)

        car_model = matrix44.create_from_translation((0,0,0))
        glUniformMatrix4fv(car_model_loc, 1, GL_FALSE, car_model)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()