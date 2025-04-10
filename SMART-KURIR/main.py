import pygame
from engine import GameEngine
from menu import start_menu

pygame.init()
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Courier v6")

engine = GameEngine(win, WIDTH, HEIGHT)
start_menu(engine)

clock = pygame.time.Clock()
while engine.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            engine.keluar()

    win.fill((255, 255, 255))

    if engine.map_surface:
        win.blit(engine.map_surface, (0, 0))
        if engine.yellow_flag_pos:
            win.blit(engine.yellow_flag_img, engine.yellow_flag_pos)
        if engine.red_flag_pos:
            win.blit(engine.red_flag_img, engine.red_flag_pos)
        if engine.courier_pos:
            rotated = pygame.transform.rotate(engine.courier_img, engine.courier_angle)
            rect = rotated.get_rect(center=engine.courier_pos)
            win.blit(rotated, rect.topleft)
        if engine.is_moving:
            engine.move_smooth()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
