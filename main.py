import pygame
import os
import sys

from objects import *
from definitions import *

# Script main
if __name__ == "__main__":
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

    out_circle_times = []
    out_all_circles_times = []

    os.makedirs("frames", exist_ok = True)
    os.makedirs("videos", exist_ok = True)
    frame_count = 0

    # Instanciation des entités
    balls = []
    for i in range(0, N_BALLS):
        balls.append(Ball())
    arcs = []
    i_arc_a_creer = 0
    for i in range(0, N_ARCS):
        arcs.append(Arc(i * BONUS_ARC_SIZE, 
                        1 - ((i+1) * MALUS_ARC_SPEED),
                        i * BONUS_COLOR))
        i_arc_a_creer = i

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

        # Mouvement
        for arc in arcs:
            arc.rotate()

        if len(arcs) > 0:
            for ball in balls:
                ball.move_in_arc(arcs[0], frame_count)
                if ball.is_out_circle:
                    out_circle_times.append(int((frame_count / FPS) * 1000))
                    for arc in arcs:
                        arc.change_orientation_rotation()
                    arcs.pop(0)
                    arcs.append(Arc(i_arc_a_creer * BONUS_ARC_SIZE, 
                                    1 - ((i_arc_a_creer+1) * MALUS_ARC_SPEED),
                                    i_arc_a_creer * BONUS_COLOR))
                    if len(arcs) == 0:
                        out_all_circles_times.append(int((frame_count / FPS) * 1000))
                    ball.is_out_circle = False
            # --- Collision entre balles ---
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    b1 = balls[i]
                    b2 = balls[j]
                    b1.collision_ball(b2)
        else:
            for ball in balls:
                ball.move()
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

        for ball in balls:
            ball.draw(screen)
        if len(arcs) > 0:
            for i in range(0, len(arcs)):
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

    # (PEUT-ETRE QUE CA MARCHE) A MODIFIER PLUS TARD, POUR LE SON
    hit_times = []
    for ball in balls:
        hit_times += ball.hit_times

    pygame.quit()
    
    make_video = True

    # Création de la vidéo
    if make_video:
        from video import *
        create_music_from_sounds(hit_times, out_circle_times,
                                out_all_circles_times)
        create_video()
        delete_frames_audio()