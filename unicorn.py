# Reference
# Initialization & rectangle: https://noobtuts.com/python/opengl-introduction

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import json
import random

window = 0												# glut window number
width, height = 600, 600								# window size
color = []

def init_color():
    with open("input.json") as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            color.append(random.random())

def draw():												# ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# clear the screen
    #glLoadIdentity()									# reset position
    refresh2d(width, height)							# set mode to 2d
        
    with open("input.json") as json_file:
        data = json.load(json_file)
        for key,value in data.items():
            color_this = color[int(key.strip("triangle"))-1]
            glColor3f(0, 1.0, color_this)
            draw_triangle (value)
    glutSwapBuffers()									# important for double buffering

def draw_triangle(points):
	# draw a pentagon
    glBegin(GL_TRIANGLES)									# start drawing a pentagon
    for key,value in points.items():
        glVertex2f(int(value[0]), int(value[1]))
    glEnd() 

def refresh2d(width, height):
	# set mode to 2d
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


# initialization
init_color()
glutInit()												# initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)						# set window size
glutInitWindowPosition(0, 0)							# set window position
window = glutCreateWindow("Unicorn")				# create window with title
glutDisplayFunc(draw)									# set draw function callback
glutIdleFunc(draw)										# draw all the time
glutMainLoop()