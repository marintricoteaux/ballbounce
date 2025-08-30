import pygame
import math
import random

from definitions import *
from functions import *

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("sounds/pop.mp3")

class Ball:
    def __init__(self, color_contour = "white", text = ""):
        self.color = "white"
        self.rect = pygame.Rect(0,0,BALL_SIZE,BALL_SIZE)
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        # Pour plus de fluidité, on garde un vecteur pos
        self.pos = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.radius = self.rect.w / 2
        self.velocity = pygame.Vector2(math.cos(random.uniform(0,2*math.pi)),
                                        math.sin(random.uniform(0,2*math.pi)))
        font = pygame.font.SysFont("Arial", 25)
        self.hit_times = []

    def update(self, circle, frame_count):
        self.velocity.y += GRAVITY
        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        # Collision avec le cercle
        vec_arc_balle = pygame.Vector2(self.rect.centerx - circle.rect.centerx,
                                       self.rect.centery - circle.rect.centery)
        dist_arc_balle = math.hypot(*vec_arc_balle)
        max_dist = (circle.radius - (circle.width / 2) - self.radius)
        if dist_arc_balle > max_dist:
            # Rebond
            normale = vec_arc_balle / dist_arc_balle
            ps_v_norm = ((self.velocity.x * normale.x) +
                            (self.velocity.y * normale.y))
            self.velocity -= 2 * ps_v_norm * normale
            self.velocity *= ENERGY_LOST_COEFF
            self.rect.center = circle.rect.center + normale * max_dist
            self.hit_times.append(int((frame_count / FPS) * 1000))
            self.pos = circle.rect.center + normale * max_dist
            self.rect.center = self.pos
        # Mouvement
        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, surface):
        # Dessin de la balle
        pygame.draw.circle(surface, self.color,
                           self.rect.center, self.radius)

class Circle:
    def __init__(self):
        self.color = "white"
        self.rect = pygame.Rect(0,0,CIRCLE_SIZE,CIRCLE_SIZE)
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.radius = self.rect.w / 2
        self.width = 3

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center,
                           self.radius, self.width)