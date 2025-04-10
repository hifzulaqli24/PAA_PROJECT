import pygame
from engine import GameEngine
from menu import start_menu

pygame.init()
win = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Smart Courier v14")

engine = GameEngine(win)
start_menu(engine)

clock = pygame.time.Clock()
while engine.running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            engine.keluar()

    win.fill((255, 255, 255))
    if engine.map_surface:
        win.blit(engine.map_surface, (0, 0))
        engine.draw_path()
        engine.draw_flags()
        engine.draw_courier()
        if engine.is_moving:
            engine.move_smooth()

    pygame.display.update()
    clock.tick(60)
pygame.quit()
