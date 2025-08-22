import pygame
import math
import random

from definitions import *

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("sounds/pop.mp3")

color_for_arcs = pygame.Color(random.randint(160, 250),
                              random.randint(160, 255),
                              random.randint(160, 255))

class Ball:
    def __init__(self):
        self.color = "black"
        self.color_contour = "white"
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = BALL_RADIUS

        initial_angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.Vector2(math.cos(initial_angle),
                                        math.sin(initial_angle))
        self.speed = random.uniform(-1.5, 1.5)
        self.velocity = self.direction * self.speed

        self.is_out_screen = False
        self.is_out_circle = False

        self.hit_times = []

    def move_in_arc(self, arc, frame_count):
        self.velocity.y += GRAVITY

        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        
        # Collision avec l'arc de cercle
        vec_arc_balle = pygame.Vector2(self.position.x - arc.rect.centerx,
                                       self.position.y - arc.rect.centery)
        dist_arc_balle = math.hypot(*vec_arc_balle)
        max_dist = (arc.radius - (arc.width / 2) - self.radius)
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
                #hit_sound.play()
                self.hit_times.append(int((frame_count / FPS) * 1000))
        
        # La balle sort de l'écran
        if not (0 < self.position.x < SCREEN_WIDTH or
                0 < self.position.y < SCREEN_HEIGHT):
            self.is_out_screen = True

        self.position += self.velocity

    def move(self):
        self.position += self.velocity

    def collision_ball(self, other_ball):
        delta = other_ball.position - self.position
        dist = delta.length()
        min_dist = self.radius + other_ball.radius
        if dist < min_dist and dist > 0:
            # Correction de la position pour éviter l'empilement
            overlap = 0.5 * (min_dist - dist + 1)
            direction = delta.normalize()
            self.position -= direction * overlap
            other_ball.position += direction * overlap
            # Calcul du rebond élastique (simplifié, masses égales)
            v1, v2 = self.velocity, other_ball.velocity
            self.velocity = v1 - direction * v1.dot(direction) + direction * v2.dot(direction)
            other_ball.velocity = v2 - direction * v2.dot(direction) + direction * v1.dot(direction)
            # Applique la perte d'énergie
            self.velocity *= ENERGY_LOST_COEFF
            other_ball.velocity *= ENERGY_LOST_COEFF

    def draw(self, surface):
        pygame.draw.circle(surface, self.color_contour, self.position, self.radius)
        pygame.draw.circle(surface, self.color, self.position, self.radius * 0.9)

class Arc:
    def __init__(self, bonus_size, malus_speed, bonus_color):
        self.color = (color_for_arcs.r + bonus_color,
                      color_for_arcs.g + bonus_color,
                      color_for_arcs.b + bonus_color) 

        self.rect = pygame.Rect(0, 0, (SCREEN_WIDTH / 2) + bonus_size,
                                (SCREEN_WIDTH / 2) + bonus_size)
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = self.rect.height / 2 

        # Quelques définitions pour les angles du trou et du cercle
        self.start_hole_angle = 2*math.pi
        self.end_hole_angle = self.start_hole_angle + 0.2 * math.pi
        if self.end_hole_angle > 2 * math.pi:
            self.end_hole_angle -= 2 * math.pi

        self.width = 5

        self.h_b_destroyed = False

        self.speed = ARC_SPEED_ROTATE * malus_speed

    def rotate(self):
        self.start_hole_angle = ((self.start_hole_angle + 
                                  (self.speed)) %
                                 (2 * math.pi))
        self.end_hole_angle = ((self.end_hole_angle + 
                                (self.speed)) %
                               (2 * math.pi))
    
    def change_orientation_rotation(self):
        self.speed = - self.speed
        
    def draw(self, surface):
        # Arc principal
        pygame.draw.arc(surface, self.color, self.rect, self.end_hole_angle,
                        self.start_hole_angle, self.width)