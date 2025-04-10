import pygame
from engine import GameEngine

pygame.init()
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Courier - v1")

engine = GameEngine(win, WIDTH, HEIGHT)
engine.load_static_map("maps/map1.jpeg")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((255, 255, 255))

    if engine.map_surface:
        win.blit(engine.map_surface, (0, 0))
        win.blit(engine.yellow_flag_img, engine.yellow_flag_pos)
        win.blit(engine.red_flag_img, engine.red_flag_pos)

        rotated_img = pygame.transform.rotate(engine.courier_img, engine.courier_angle)
        rect = rotated_img.get_rect(center=engine.courier_pos)
        win.blit(rotated_img, rect.topleft)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
