import pygame
import math
import random

from definitions import *

class Ball:
    def __init__(self):
        self.color = pygame.Color(random.randint(0, 255),
                                  random.randint(0, 255),
                                  random.randint(0, 255))
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = 10

        initial_angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.Vector2(math.cos(initial_angle),
                                   math.sin(initial_angle))
        self.speed = random.uniform(-3, 3)
        self.velocity = self.direction * self.speed

    def move(self):
        self.velocity.y += GRAVITY

        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        
        #Collision avec les bords
        if self.position.x - self.radius < 0:
            self.position.x = 0 + self.radius
            self.velocity.x *= -ENERGY_LOST_COEFF
        if self.position.x + self.radius > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.radius
            self.velocity.x *= -ENERGY_LOST_COEFF
        if self.position.y - self.radius < 0:
            self.position.y = 0 + self.radius
            self.velocity.y *= -ENERGY_LOST_COEFF
        if self.position.y + self.radius > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.radius
            self.velocity.y *= -ENERGY_LOST_COEFF

        self.position += self.velocity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

class Arc:
    pass