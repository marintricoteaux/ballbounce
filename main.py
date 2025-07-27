import pygame

from objects import *
from definitions import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BallBounce V3")
    clock = pygame.time.Clock()
    running = True

    balls = []
    arcs = []
    arcs.append(Arc())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    balls.append(Ball())

        for arc in arcs:
            arc.rotate()
        for ball in balls:
            for arc in arcs:
                ball.move(arc)
        
        screen.fill("black")

        for ball in balls:
            ball.draw(screen)
        for arc in arcs:
            arc.draw(screen)

        pygame.display.flip()

        clock.tick(120)

    pygame.quit()