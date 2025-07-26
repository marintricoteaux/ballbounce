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

    def move(self, arc):
        self.velocity.y += GRAVITY

        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        
        # Collision avec le cercle
        vec_arc_balle = pygame.Vector2(self.position.x - arc.rect.centerx,
                                       self.position.y - arc.rect.centery)
        dist_arc_balle = math.hypot(*vec_arc_balle)
        max_dist = arc.radius - self.radius
        if dist_arc_balle > max_dist:
            # Normale
            normale = vec_arc_balle / dist_arc_balle
            # Produit scalaire (vitesse . normale)
            ps_v_norm = ((self.velocity.x * normale.x) +
                         (self.velocity.y * normale.y))
            # Réflexion de la vitesse (rebond)
            self.velocity -= 2 * ps_v_norm * normale
            # Perte d'énergie due au rebond (ou gain)
            self.velocity *= ENERGY_LOST_COEFF
            # Replacerla balle correctement
            self.position = arc.rect.center + normale * max_dist
        
        print(abs(self.velocity.x), abs(self.velocity.y))
        self.position += self.velocity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

class Arc:
    def __init__(self):
        self.color = "white"

        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH / 1.5, SCREEN_WIDTH / 1.5)
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = self.rect.height / 2

        self.start_angle = 0
        self.end_angle = 2 * math.pi

        self.width = 5

    def rotate(self):
        pass

    def draw(self, surface):
        pygame.draw.arc(surface, self.color, self.rect,
                        self.start_angle, self.end_angle, self.width)