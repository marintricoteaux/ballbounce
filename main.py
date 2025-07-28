import pygame
import os

from objects import *
from definitions import *
from video import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BallBounce V3")
    clock = pygame.time.Clock()
    running = True

    os.makedirs("frames", exist_ok = True)
    os.makedirs("videos", exist_ok = True)
    frame_count = 0

    balls = []
    balls.append(Ball())
    arcs = []
    arcs.append(Arc())

    while running and frame_count < MAX_FRAMES:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for arc in arcs:
            arc.rotate()
        for ball in balls:
            for arc in arcs:
                # On fait bouger la balle par rapport à l'arc
                ball.move(arc)
                # Lorsqu'une balle sort du cercle :
                if ball.is_out_circle and not ball.has_spawned:
                    for i in range (2):
                        balls.append(Ball())
                    ball.has_spawned = True
                # Lorque la balle sort de l'écran, elle est supprimée
                if ball.is_out_screen:
                    balls.remove(ball)
        for i in range(len(balls)):
            for j in range (i + 1, len(balls)):
                balls[i].collision_ball(balls[j])

        screen.fill("black")

        for ball in balls:
            ball.draw(screen)
        for arc in arcs:
            arc.draw(screen)

        pygame.display.flip()

        # Sauvegarde de l'image dans le dossier frames
        pygame.image.save(screen, f"frames/frame_{frame_count:04d}.png")
        frame_count += 1

        clock.tick(60)
        print(frame_count)

    pygame.quit()

    create_video_from_frames()
    delete_frames()