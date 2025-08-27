import pygame
import math
import random

from definitions import *
from functions import *

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("sounds/pop.mp3")

class Ball:
    def __init__(self, color_contour = "white", text = ""):
        self.color = "black"
        self.color_contour = color_contour
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = BALL_RADIUS

        initial_angle = random.uniform(0, 2 * math.pi)
        self.direction = pygame.Vector2(math.cos(initial_angle),
                                        math.sin(initial_angle))
        self.speed = random.uniform(-1.5, 1.5)
        self.velocity = self.direction * self.speed

        font = pygame.font.SysFont("Arial", 25)

        self.text = text
        self.text_in_circle = font.render(text, True, "white")
        self.text_rect = self.text_in_circle.get_rect(center=(self.position))

        self.count = 0

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
                self.count += 1
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
        self.text_rect.center = self.position

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
            self.velocity = (v1 - direction * v1.dot(direction) +
                             direction * v2.dot(direction))
            other_ball.velocity = (v2 - direction *
                                   v2.dot(direction) + direction *
                                   v1.dot(direction))
            # Applique la perte d'énergie
            self.velocity *= ENERGY_LOST_COEFF
            other_ball.velocity *= ENERGY_LOST_COEFF

    def draw(self, surface):
        # Dessin de la balle/contour
        pygame.draw.circle(surface, self.color_contour,
                           self.position, self.radius)
        pygame.draw.circle(surface, self.color,
                           self.position, self.radius * 0.9)
        # Dessin du texte
        surface.blit(self.text_in_circle, self.text_rect)

class CountBox:
    def __init__(self, ball):
        self.font = pygame.font.SysFont("Arial", 25)

        self.text = self.font.render(f"{ball.text} : {ball.count}",
                                True, "white", ball.color_contour)
        if ball.text == "YES":
            self.position = (SCREEN_WIDTH/4, SCREEN_HEIGHT/4)
        if ball.text == "NO":
            self.position = ((SCREEN_WIDTH*3)/4, SCREEN_HEIGHT/4)
        self.rect = self.text.get_rect(center=self.position)
        self.background_rect = self.text.get_rect(center=self.position)
        self.back_color = ball.color_contour

    def maj(self, ball):
        self.text = self.font.render(f"{ball.text} : {ball.count}",
                                True, "white")
        self.background_rect = self.text.get_rect(center=self.position)
        self.background_rect.width *= COEF_RECT_BACK
        self.background_rect.height *= COEF_RECT_BACK
        self.background_rect.center = self.position
        self.rect = self.text.get_rect(center=self.position)
        self.rect.center = self.position

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color,
                         self.background_rect, border_radius=8)
        surface.blit(self.text, self.rect)

class Arc:
    def __init__(self, size, color,
                 start_hole_angle = 2*math.pi, rotation_sens = 1):
        self.color = color

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.radius = self.rect.height / 2 

        # Quelques définitions pour les angles du trou et du cercle
        self.start_hole_angle = start_hole_angle
        self.end_hole_angle = self.start_hole_angle + SIZE_HOLE_COEFF * math.pi
        if self.end_hole_angle > 2 * math.pi:
            self.end_hole_angle -= 2 * math.pi

        self.width = 5

        self.h_b_destroyed = False

        self.speed = ARC_SPEED_ROTATE
        self.rotation_sens = rotation_sens

    def rotate(self):
        current_speed = self.speed * self.rotation_sens
        self.start_hole_angle = ((self.start_hole_angle + 
                                  (current_speed)) %
                                 (2 * math.pi))
        self.end_hole_angle = ((self.end_hole_angle + 
                                (current_speed)) %
                               (2 * math.pi))
    
    def change_orientation_rotation(self):
        self.rotation_sens = -self.rotation_sens
        
    def draw(self, surface):
        pygame.draw.arc(surface, self.color, self.rect, self.end_hole_angle,
                        self.start_hole_angle, self.width)