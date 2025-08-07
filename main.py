import pygame
import os
import sys

from objects import *
from definitions import *
from video import *

# Script main
if __name__ == "__main__":
    # Conditions pour que la vidéo soit optimale
    condition_respected = False

    while not condition_respected:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BallBounce V3")
        clock = pygame.time.Clock()
        running = True

        font = pygame.font.SysFont("Arial", 48)

        start_ticks = pygame.time.get_ticks()
        duration_ms = 1000 * (FPS / 2)
        timer_stopped = False
        color_timer = "white"

        pygame.mixer.init()
        out_circle_sound_pygame = pygame.mixer.Sound("sounds/pet.wav")
        out_all_circles_sound_pygame = pygame.mixer.Sound("sounds/victory_ring.mp3")

        out_circle_times = []
        out_all_circles_times = []

        os.makedirs("frames", exist_ok = True)
        os.makedirs("videos", exist_ok = True)
        frame_count = 0

        ball_1 = Ball()
        arcs = []
        for i in range(0, N_ARCS):
            arcs.append(Arc(i * BONUS_ARC_SIZE, 
                            1 - ((i+1) * MALUS_ARC_SPEED),
                            i * BONUS_COLOR))
        index_arcs = 0

        # Boucle principale
        while running and frame_count < MAX_FRAMES:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_q:
                        delete_frames_audio()
                        sys.exit()

            # Evolution des objets
            ball_1.radius += BONUS_BALL_RADIUS

            # Mouvement
            for arc in arcs:
                arc.rotate()

            if index_arcs < N_ARCS:
                ball_1.move_in_arc(arcs[index_arcs], frame_count)
                if ball_1.is_out_circle:
                    #out_circle_sound_pygame.play()
                    out_circle_times.append(int((frame_count / FPS) * 1000))
                    for arc in arcs:
                        arc.change_orientation_rotation()
                    index_arcs += 1
                    if index_arcs == N_ARCS:
                        #out_all_circles_sound_pygame.play()
                        out_all_circles_times.append(int((frame_count / FPS) * 1000))
                    ball_1.is_out_circle = False
            else:
                ball_1.move()
                if not timer_stopped:
                    frame_to_exit = frame_count + (1 * FPS)
                timer_stopped = True
                color_timer = (0, 255, 0)
                if frame_count >= frame_to_exit:
                    running = False

            # Calcul du timer
            if not timer_stopped:
                remaining_frames = max(0, (60 * FPS) - frame_count)
                seconds = remaining_frames // FPS
                centiseconds = int((remaining_frames % FPS) * (100 / FPS))
                timer_str = f"{seconds:02d}:{centiseconds:02d}"

            # Affichage
            screen.fill("black")

            ball_1.draw(screen)
            if index_arcs < N_ARCS:
                for i in range(index_arcs, len(arcs)):
                    arcs[i].draw(screen)

            timer_text = font.render(f"{timer_str}", True, color_timer)
            timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2))
            timer_rect.centery = (arcs[-1].rect.bottom + SCREEN_HEIGHT) / 2.1
            screen.blit(timer_text, timer_rect)

            pygame.display.flip()

            # Sauvegarde de l'image dans le dossier frames
            pygame.image.save(screen, f"frames/frame_{frame_count:04d}.png")
            frame_count += 1

            clock.tick(FPS)
        
        hit_times = ball_1.hit_times

        pygame.quit()

        if 0 <= duration_ms <= 5000:
            condition_respected = True
        else:
            delete_frames_audio()

    create_music_from_sounds(hit_times, out_circle_times, out_all_circles_times)
    create_video()
    delete_frames_audio()