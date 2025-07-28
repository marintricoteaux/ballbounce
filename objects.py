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

        self.is_out_circle = False
        self.is_out_screen = False
        self.has_spawned = False

    def move(self, arc):
        self.velocity.y += GRAVITY

        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        
        # Collision avec l'arc de cercle
        vec_arc_balle = pygame.Vector2(self.position.x - arc.rect.centerx,
                                       self.position.y - arc.rect.centery)
        dist_arc_balle = math.hypot(*vec_arc_balle)
        max_dist = arc.radius - self.radius
        if dist_arc_balle > max_dist and self.is_out_circle == False:
            # On vérifie que la balle n'est pas face au trou
            angle = math.atan2(-vec_arc_balle.y, vec_arc_balle.x)
            if angle < 0:
                angle += 2 * math.pi
            if angle_in_interval(angle, arc.start_hole_angle,
                                 arc.end_hole_angle):
                self.is_out_circle = True
            else:
                # Rebond                
                normale = vec_arc_balle / dist_arc_balle
                ps_v_norm = ((self.velocity.x * normale.x) +
                             (self.velocity.y * normale.y))
                self.velocity -= 2 * ps_v_norm * normale
                self.velocity *= ENERGY_LOST_COEFF
                self.position = arc.rect.center + normale * max_dist
        
        # La balle sort de l'écran
        if not (0 < self.position.x < SCREEN_WIDTH or
                0 < self.position.y < SCREEN_HEIGHT):
            self.is_out_screen = True

        self.position += self.velocity
    
    def collision_ball(self, other):
        delta = other.position - self.position
        distance = delta.length()
        min_dist = self.radius + other.radius
        if distance < min_dist and distance != 0:
            # Correction de position
            overlap = min_dist - distance
            direction = delta.normalize()
            self.position -= direction * (overlap / 2)
            other.position += direction * (overlap / 2)
            # Rebond : échange de vitesse sur l'axe de collision
            v1 = self.velocity
            v2 = other.velocity
            n = direction
            p = 2 * (v1 - v2).dot(n) / 2

            self.velocity -= p * n
            other.velocity += p * n

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

class Arc:
    def __init__(self):
        self.color = "white"

        self.rect = pygame.Rect(0, 0, SCREEN_WIDTH / 1.5, SCREEN_WIDTH / 1.5)
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = self.rect.height / 2

        # Quelques définitions pour les angles du trou et du cercle
        self.start_hole_angle = random.uniform(0, 2 * math.pi)
        self.end_hole_angle = self.start_hole_angle + 0.2 * math.pi
        if self.end_hole_angle > 2 * math.pi:
            self.end_hole_angle -= 2 * math.pi

        self.width = 1

        # Effet néon extérieur
        self.neon_width = 1
        self.neon_color = []
        self.neon_rect = []
        for i in range (10):
            self.neon_color.append(pygame.Color(100 - (i * 5),
                                                100 - (i * 5),
                                                100 - (i * 5)))
            self.neon_rect.append(pygame.Rect(self.rect))
            self.neon_rect[i].width = self.rect.width + i
            self.neon_rect[i].height = self.rect.height + i
            self.neon_rect[i].center = self.rect.center 

    def rotate(self):
        self.start_hole_angle = ((self.start_hole_angle + ARC_SPEED_ROTATE) %
                                 (2 * math.pi))
        self.end_hole_angle = ((self.end_hole_angle + ARC_SPEED_ROTATE) %
                               (2 * math.pi))

    def draw(self, surface):
        # Arc principal
        pygame.draw.arc(surface, self.color, self.rect, self.end_hole_angle,
                        self.start_hole_angle, self.width)
        # Effet néon
        #for i in range(10):
            #pygame.draw.arc(surface, self.neon_color[i], self.neon_rect[i], self.end_hole_angle, self.start_hole_angle, self.neon_width)