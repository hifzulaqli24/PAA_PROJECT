import pygame
from engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Courier")

engine = GameEngine(win, WIDTH, HEIGHT)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((255, 255, 255))

    if engine.map_surface:
        win.blit(engine.map_surface, (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
