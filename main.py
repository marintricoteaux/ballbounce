import pygame
import os
import sys

from objects import *
from definitions import *
from functions import *

# Script main
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BallBounce V3")
    clock = pygame.time.Clock()
    running = True

    start_ticks = pygame.time.get_ticks()
    duration_ms = 1000 * (FPS / 2)
    timer_stopped = False
    color_timer = "white"

    out_circle_times = []
    out_all_circles_times = []

    os.makedirs("frames", exist_ok = True)
    os.makedirs("videos", exist_ok = True)
    frame_count = 0

    # Instanciation des entités
    balls = [Ball()]
    circles = [Circle()]

    # Boucle principale
    while running and frame_count < MAX_FRAMES:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_frames_audio()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) :
                    delete_frames_audio()
                    sys.exit()

        # Mouvement
        balls[0].update(circles[0], frame_count)

        # Affichage
        screen.fill("black")

        balls[0].draw(screen)
        circles[0].draw(screen)

        pygame.display.flip()

        # Sauvegarde de l'image dans le dossier frames
        pygame.image.save(screen, f"frames/frame_{frame_count:04d}.png")
        frame_count += 1

        clock.tick(FPS)

    hit_times = []
    for ball in balls:
        hit_times += ball.hit_times

    pygame.quit()
    
    # Création de la vidéo
    from video import *
    create_music_from_sounds(hit_times, out_circle_times,
                            out_all_circles_times)
    create_video()
    delete_frames_audio()