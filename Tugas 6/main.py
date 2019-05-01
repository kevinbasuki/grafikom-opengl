import glfw
from OpenGL.GL import *
import numpy
from pyrr import matrix44
from Camera import Camera
from ShaderLoader import *
import TextureLoader
import math
from Particles import *

#Constants
TRIANGLE_AMOUNT = 50
PI = 3.14159265359

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def generateCircleArray(x, y, z, radius, thickness):
    result = []
    height = []
    for i in range(TRIANGLE_AMOUNT):
        #buat lingkaran
        result.append(x)
        result.append(y)
        result.append(z)
        result.append(0.5)
        result.append(0.5)
        result.append(-1.0)
        result.append(0.0)
        result.append(0.0)
        result.append(x)
        result.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(-1.0)
        result.append(0.0)
        result.append(0.0)
        result.append(x)
        result.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(-1.0)
        result.append(0.0)
        result.append(0.0)

        result.append(x + thickness)
        result.append(y)
        result.append(z)
        result.append(0.5)
        result.append(0.5)
        result.append(1.0)
        result.append(0.0)
        result.append(0.0)
        result.append(x + thickness)
        result.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        result.append(1.0)
        result.append(0.0)
        result.append(0.0)
        result.append(x + thickness)
        result.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(0.5 + 0.5 * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        result.append(1.0)
        result.append(0.0)
        result.append(0.0)

        #Buat ketebalan
        #segitiga 1
        height.append(x)
        height.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        height.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))

        height.append(x)
        height.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        height.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        
        height.append(x + thickness)
        height.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        height.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        #segitiga 2
        height.append(x + thickness)
        height.append(y + radius * math.cos((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        height.append(z + radius * math.sin((i + 1) * 2 * PI / TRIANGLE_AMOUNT))
        
        height.append(x + thickness)
        height.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        height.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        
        height.append(x)
        height.append(y + radius * math.cos(i * 2 * PI / TRIANGLE_AMOUNT))
        height.append(z + radius * math.sin(i * 2 * PI / TRIANGLE_AMOUNT))
        

    result = numpy.array(result, dtype=numpy.float32)
    height = numpy.array(height, dtype=numpy.float32)
    return result, height

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

    car_back = [
        #Badan Mobil
        #front
        -1.0, -1.0, 1.0, 0.167, 0.0, 0.0, 0.0, 1.0,
        1.0, -1.0, 1.0, 0.833, 0.0, 0.0, 0.0, 1.0,
        1.0, 1.0, 1.0, 0.833, 1.0, 0.0, 0.0, 1.0,
        -1.0, 1.0, 1.0, 0.167, 1.0, 0.0, 0.0, 1.0,

        #right
        1.0, -1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        1.0, -1.0, -2.0, 1.0, 0.0, 1.0, 0.0, 0.0,
        1.0, 1.0, -2.0, 1.0, 1.0, 1.0, 0.0, 0.0,
        1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0,

        #back
        -1.0, -1.0, -2.0, 0.167, 0.0, 0.0, 0.0, -1.0,
        1.0, -1.0, -2.0, 0.833, 0.0, 0.0, 0.0, -1.0,
        1.0, 1.0, -2.0, 0.833, 1.0, 0.0, 0.0, -1.0,
        -1.0, 1.0, -2.0, 0.167, 1.0, 0.0, 0.0, -1.0,

        #left
        -1.0, -1.0, 1.0, 0.0, 0.0, -1.0, 0.0, 0.0,
        -1.0, -1.0, -2.0, 1.0, 0.0, -1.0, 0.0, 0.0,
        -1.0, 1.0, -2.0, 1.0, 1.0, -1.0, 0.0, 0.0,
        -1.0, 1.0, 1.0, 0.0, 1.0, -1.0, 0.0, 0.0,

        #top
        -1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 1.0, -2.0, 1.0, 1.0, 0.0, 1.0, 0.0,
        -1.0, 1.0, -2.0, 0.0, 1.0, 0.0, 1.0, 0.0,

        #bottom
        -1.0, -1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0,
        1.0, -1.0, 1.0, 1.0, 0.0, 0.0, -1.0, 0.0,
        1.0, -1.0, -2.0, 1.0, 1.0, 0.0, -1.0, 0.0,
        -1.0, -1.0, -2.0, 0.0, 1.0, 0.0, -1.0, 0.0
    ]
    
    car_front = [
        #Depan Mobil
        #front
        -1.0, -1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0,
        1.0, -1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0,
        1.0, 0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0,
        -1.0, 0, 2.0, 0.0, 1.0,  0.0, 0.0, 1.0,

        #right
        1.0, -1.0, 2.0, 0.167, 0.0, 1.0, 0.0, 0.0,
        1.0, -1.0, 1.0, 0.833, 0.0, 1.0, 0.0, 0.0,
        1.0, 0, 1.0, 0.833, 1.0, 1.0, 0.0, 0.0,
        1.0, 0, 2.0, 0.167, 1.0, 1.0, 0.0, 0.0,

        #back
        -1.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0,
        1.0, -1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0,
        1.0, 0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0,
        -1.0, 0, 1.0, 0.0, 1.0, 0.0, 0.0, -1.0,

        #left
        -1.0, -1.0, 2.0, 0.167, 0.0, -1.0, 0.0, 0.0,
        -1.0, -1.0, 1.0, 0.833, 0.0, -1.0, 0.0, 0.0,
        -1.0, 0, 1.0, 0.833, 1.0, -1.0, 0.0, 0.0,
        -1.0, 0, 2.0, 0.167, 1.0, -1.0, 0.0, 0.0,

        #top
        -1.0, 0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 0, 2.0, 1.0, 0.0, 0.0, 1.0, 0.0,
        1.0, 0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0,
        -1.0, 0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0,

        #bottom
        -1.0, -1.0, 2.0, 0.0, 0.0, 0.0, -1.0, 0.0,
        1.0, -1.0, 2.0, 1.0, 0.0, 0.0, -1.0, 0.0,
        1.0, -1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 0.0,
        -1.0, -1.0, 1.0, 0.0, 1.0, 0.0, -1.0, 0.0
    ]

    car_back = numpy.array(car_back, dtype=numpy.float32)
    car_front = numpy.array(car_front, dtype=numpy.float32)
    indices = [
        0,1,2,2,3,0,
        4,5,6,6,7,4,
        8,9,10,10,11,8,
        12,13,14,14,15,12,
        16,17,18,18,19,16,
        20,21,22,22,23,20,
    ]

    indices = numpy.array(indices, dtype=numpy.uint32)

    rains = spawnRain(100)

    rainparticles = []
    for rain in rains:
        rainparticles.append(rain.position[0])
        rainparticles.append(rain.position[1])
        rainparticles.append(rain.position[2])

    rainparticles = numpy.array(rainparticles, dtype=numpy.float32)

    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
    glPointSize(1000)
    car_program = compile_shader("Shaders/CarShader.vs", "Shaders/CarShader.fs")
    wheel_program = compile_shader("Shaders/WheelShader.vs", "Shaders/WheelShader.fs")
    rain_program = compile_shader("Shaders/RainShader.vs", "Shaders/RainShader.fs")
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    car_model_loc = glGetUniformLocation(car_program, "model")
    car_view_loc = glGetUniformLocation(car_program, "view")
    car_proj_loc = glGetUniformLocation(car_program, "proj")
    car_cam_pos = glGetUniformLocation(car_program, "viewPos")

    wheel_model_loc = glGetUniformLocation(wheel_program, "model")
    wheel_view_loc = glGetUniformLocation(wheel_program, "view")
    wheel_proj_loc = glGetUniformLocation(wheel_program, "proj")
    circle, thickness = generateCircleArray(0, 0, 0, 0.4, 0.2)

    rain_model_loc = glGetUniformLocation(rain_program, "model")
    rain_view_loc = glGetUniformLocation(rain_program, "view")
    rain_proj_loc = glGetUniformLocation(rain_program, "proj")


    VAO_wheel = glGenVertexArrays(1)
    glBindVertexArray(VAO_wheel)
    VBO_wheel = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_wheel)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, circle.itemsize * 3, ctypes.c_void_p(0))

    VAO_car = glGenVertexArrays(1)
    glBindVertexArray(VAO_car)
    VBO_car = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_car)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, car_back.itemsize * 8, ctypes.c_void_p(0))
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, car_back.itemsize * 8, ctypes.c_void_p(12))
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, car_back.itemsize * 8, ctypes.c_void_p(20))

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    VAO_rain = glGenVertexArrays(1)
    glBindVertexArray(VAO_rain)
    VBO_rain = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO_rain)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, rainparticles.itemsize * 3, ctypes.c_void_p(0))

    metal = TextureLoader.load_texture("Textures/badan_samping.jpg")
    metal2 = TextureLoader.load_texture("Textures/kap_samping.jpg")
    roda = TextureLoader.load_texture("Textures/roda.jpg")
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        do_movement()
        view = cam.get_view_matrix()
        camera_position = cam.get_cam_pos()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #Gambar Roda
        glBindVertexArray(VAO_car)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_car)
        glBufferData(GL_ARRAY_BUFFER, circle.itemsize * len(circle), circle, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        glUseProgram(car_program)

        wheel_positions = [(1.0, -1.0, 1.0), (-1.2, -1.0, 1.0), (-1.2, -1.0, -2.0), (1.0, -1.0, -2.0)]

        glUniformMatrix4fv(car_proj_loc, 1, GL_FALSE, projection)

        glUniformMatrix4fv(car_view_loc, 1, GL_FALSE, view)
        glUniform3fv(car_cam_pos, 1, camera_position)

        for i in range(len(wheel_positions)):
            wheel_model = matrix44.create_from_translation(wheel_positions[i])
            glUniformMatrix4fv(car_model_loc, 1, GL_FALSE, wheel_model)
            glBindTexture(GL_TEXTURE_2D, roda)
            glDrawArrays(GL_TRIANGLES, 0, len(circle))

        #Gambar Mobil
        glBindVertexArray(VAO_car)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_car)
        glBufferData(GL_ARRAY_BUFFER, car_back.itemsize * len(car_back), car_back, GL_STATIC_DRAW)

        glUniformMatrix4fv(car_proj_loc, 1, GL_FALSE, projection)

        glUniformMatrix4fv(car_view_loc, 1, GL_FALSE, view)

        car_model = matrix44.create_from_translation((0,0,0))
        glUniformMatrix4fv(car_model_loc, 1, GL_FALSE, car_model)
        glBindTexture(GL_TEXTURE_2D, metal)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glBufferData(GL_ARRAY_BUFFER, car_front.itemsize * len(car_front), car_front, GL_STATIC_DRAW)
        glBindTexture(GL_TEXTURE_2D, metal2)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)


        glBindVertexArray(VAO_wheel)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_wheel)
        glBufferData(GL_ARRAY_BUFFER, thickness.itemsize * len(thickness), thickness, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)

        glUseProgram(wheel_program)

        glUniformMatrix4fv(wheel_proj_loc, 1, GL_FALSE, projection)

        glUniformMatrix4fv(wheel_view_loc, 1, GL_FALSE, view)

        for i in range(len(wheel_positions)):
            wheel_model = matrix44.create_from_translation(wheel_positions[i])
            glUniformMatrix4fv(wheel_model_loc, 1, GL_FALSE, wheel_model)
            glDrawArrays(GL_TRIANGLES, 0, len(thickness))

        glBindVertexArray(VAO_rain)
        glBindBuffer(GL_ARRAY_BUFFER, VBO_rain)
        glBufferData(GL_ARRAY_BUFFER, rainparticles.itemsize * len(rainparticles), rainparticles, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glUseProgram(rain_program)
        glUniformMatrix4fv(rain_proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(rain_view_loc, 1, GL_FALSE, view)

        rain_model = matrix44.create_from_translation((0,0,0))
        glUniformMatrix4fv(rain_model_loc, 1, GL_FALSE, rain_model)

        glDrawArrays(GL_POINTS, 0, len(rainparticles))

        updateFrame(rains)

        added_rains = spawnRain(100)

        for added_rain in added_rains:
            rains.append(added_rain)

        rainparticles = []
        for rain in rains:
            rainparticles.append(rain.position[0])
            rainparticles.append(rain.position[1])
            rainparticles.append(rain.position[2])

        rainparticles = numpy.array(rainparticles, dtype=numpy.float32)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()