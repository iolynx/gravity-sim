import math
import pygame


class Particle:
    def __init__(self, x, y, xvel, yvel, mass, radius, colour, screen):
        self.x = x
        self.y = y
        self.xVel = xvel
        self.yVel = yvel
        self.radius = radius
        self.colour = colour
        self.mass = mass
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, self.colour,
                           (self.x, self.y), self.radius, self.radius)

    def drawTrail(self, surface):
        pygame.draw.circle(surface, self.colour,
                           (self.x, self.y), self.radius//2, self.radius//2)

    def updatePos(self):
        self.x += self.xVel
        self.y += self.yVel

    '''def updateVel(self, xForce, yForce):
		self.xVel = xForce / self.mass
		self.yVel = yForce / self.mass'''

    def updateForces(self, p):

        diffx = p.x - self.x
        diffy = p.y - self.y
        dist = math.sqrt(diffx**2 + diffy**2)
        fNet = (G * p.mass * self.mass)/(dist**2)

        theta = math.atan2(diffy, diffx)

        acc = fNet / self.mass

        self.xVel += (acc * math.cos(theta))
        self.yVel += (acc * math.sin(theta))