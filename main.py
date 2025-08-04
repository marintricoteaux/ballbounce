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

    pygame.mixer.init()
    out_sound = pygame.mixer.Sound("sounds/pet.wav")

    os.makedirs("frames", exist_ok = True)
    os.makedirs("videos", exist_ok = True)
    frame_count = 0

    ball_1 = Ball()
    arcs = []
    for i in range(0, 10):
        arcs.append(Arc(i * (30), i * (0.1), 0.95 - ((i+1) * 0.05)))
    index_arcs = 0

    while running and frame_count < MAX_FRAMES:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for arc in arcs:
            arc.rotate()

        ball_1.move(arcs[index_arcs])
        if ball_1.is_out_circle:
            index_arcs += 1
            ball_1.is_out_circle = False

        screen.fill("black")

        ball_1.draw(screen)
        for i in range(index_arcs, len(arcs)):
            arcs[i].draw(screen)

        pygame.display.flip()

        # Sauvegarde de l'image dans le dossier frames
        pygame.image.save(screen, f"frames/frame_{frame_count:04d}.png")
        frame_count += 1

        clock.tick(60)
        #print(frame_count)

    pygame.quit()

    #create_video_from_frames()
    delete_frames()