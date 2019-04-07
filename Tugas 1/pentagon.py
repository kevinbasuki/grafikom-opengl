# Reference
# Initialization & rectangle: https://noobtuts.com/python/opengl-introduction

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = 0												# glut window number
width, height = 500, 400								# window size

def draw():												# ondraw is called all the time
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# clear the screen
	#glLoadIdentity()									# reset position
	refresh2d(width, height)							# set mode to 2d

	glColor3f(0.0, 1.0, 0.0)							# set color to green
	draw_triangle(100, 50, 150, 250, 50, 150)			# draw a pentagon with triangle
	glColor3f(0.2, 0.8, 0.0)
	draw_triangle(100, 50, 200, 50, 150, 250)
	glColor3f(0.4, 0.6, 0.0)
	draw_triangle(200, 50, 250, 150, 150, 250)
	
	glutSwapBuffers()									# important for double buffering

def draw_triangle(x1, y1, x2, y2, x3, y3):
	# draw a triangle
	glBegin(GL_TRIANGLES)								# start drawing a triangle
	glVertex2f(x1, y1)
	glVertex2f(x2, y2)
	glVertex2f(x3, y3)
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
glutInit()												# initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)						# set window size
glutInitWindowPosition(0, 0)							# set window position
window = glutCreateWindow("Green Pentagon")				# create window with title
glutDisplayFunc(draw)									# set draw function callback
glutIdleFunc(draw)										# draw all the time
glutMainLoop()