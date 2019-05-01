from OpenGL.GL import *
import random

class Particle:
	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

def spawnRain(n):
	particles = []
	for x in range (0, n):
		x = random.uniform(-5.0,5.0)
		y = 3.0
		z = random.uniform(-5.0,5.0)
		position = [x, y, z]
		particle = Particle(position, 0.1)
		particles.append(particle)
	return particles

def updateFrame(particles):
	for particle in particles:
		particle.position[1] -= particle.velocity
		if (particle.position[1] < -2.0):
			particles.remove(particle)