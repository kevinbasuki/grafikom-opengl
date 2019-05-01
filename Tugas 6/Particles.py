from OpenGL.GL import *
import random

class Particle:
	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

# class Smoke:
# 	def __init__(self, position, velocity, opacity):
# 		self.position = position
# 		self.velocity = velocity
# 		self.opacity = opacity

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

def updateRain(particles):
	for particle in particles:
		particle.position[1] -= particle.velocity
		if (particle.position[1] < -1.5):
			particles.remove(particle)

def spawnSmoke(n):
	particles = []
	for x in range (0, n):
		x = 0
		y = -1
		z = -2
		position = [x, y, z]
		particle = Particle(position, 0.015)
		particle.opacity = 1.0
		particles.append(particle)
	return particles

def updateSmoke(particles):
	for particle in particles:
		particle.position[0] -= random.uniform(-0.01,0.01)
		particle.position[1] += random.uniform(-0.01,0.01)
		particle.position[2] -= particle.velocity
		particle.opacity -= random.uniform(0.001,0.02)
		if (particle.opacity <= 0):
			particles.remove(particle)