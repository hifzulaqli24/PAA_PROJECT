import pygame
from menu import start_menu
from engine import GameEngine

pygame.init()
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Courier")

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
            rotated_img = pygame.transform.rotate(engine.courier_img, engine.courier_angle)
            rect = rotated_img.get_rect(center=engine.courier_pos)
            win.blit(rotated_img, rect.topleft)

        if engine.is_moving:
            engine.update_courier_position()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
