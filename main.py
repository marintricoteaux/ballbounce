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
    out_circle_sound_pygame = pygame.mixer.Sound("sounds/pet.wav")

    out_circle_times = []

    os.makedirs("frames", exist_ok = True)
    os.makedirs("videos", exist_ok = True)
    frame_count = 0

    ball_1 = Ball()
    arcs = []
    for i in range(0, 10):
        arcs.append(Arc(i * BONUS_ARC_SIZE, 
                        1 - ((i+1) * MALUS_ARC_SPEED)))
    index_arcs = 0

    while running and frame_count < MAX_FRAMES:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Les arcs tournent
        for arc in arcs:
            arc.rotate()

        print(index_arcs)
        if index_arcs < N_ARCS:
            ball_1.move_in_arc(arcs[index_arcs], frame_count)
            if ball_1.is_out_circle:
                out_circle_sound_pygame.play()
                out_circle_times.append(int((frame_count / 60) * 1000))
                for arc in arcs:
                    arc.change_orientation_rotation()
                index_arcs += 1
                ball_1.is_out_circle = False
        else:
            ball_1.move()

        screen.fill("black")

        ball_1.draw(screen)
        if index_arcs < N_ARCS:
            for i in range(index_arcs, len(arcs)):
                arcs[i].draw(screen)

        pygame.display.flip()

        # Sauvegarde de l'image dans le dossier frames
        pygame.image.save(screen, f"frames/frame_{frame_count:04d}.png")
        frame_count += 1

        clock.tick(60)
        #print(frame_count)
    
    hit_times = ball_1.hit_times

    pygame.quit()

    create_music_from_sounds(hit_times, out_circle_times)
    create_video()
    delete_frames_audio()