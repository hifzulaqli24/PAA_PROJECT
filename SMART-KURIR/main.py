import pygame
from engine import GameEngine
from menu import start_menu

pygame.init()
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Courier v12")

engine = GameEngine(win, WIDTH, HEIGHT)
start_menu(engine)

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

while engine.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            engine.keluar()

    win.fill((255, 255, 255))

    if engine.map_surface:
        win.blit(engine.map_surface, (0, 0))

        # Tampilkan jalur & kurir
        engine.draw_path()
        engine.draw_flags()
        engine.draw_courier()

        # Jalankan pergerakan kurir
        if engine.is_moving:
            engine.move_smooth()

        # Status di pojok kiri atas
        text = font.render(engine.get_status_text(), True, (0, 0, 0))
        win.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
