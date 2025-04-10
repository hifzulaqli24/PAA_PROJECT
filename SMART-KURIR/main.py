import pygame
from engine import GameEngine
from menu import start_menu

pygame.init()
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Courier v10")

engine = GameEngine(win, WIDTH, HEIGHT)
start_menu(engine)  # Menu tkinter dijalankan di thread terpisah

font = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()

while engine.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            engine.keluar()

    win.fill((255, 255, 255))

    if engine.map_surface:
        win.blit(engine.map_surface, (0, 0))

        # Gambar jalur path jika ada
        if engine.path:
            for point in engine.path:
                pygame.draw.circle(win, (0, 0, 255), point, 2)

        # Gambar bendera dan kurir
        if engine.yellow_flag_pos:
            win.blit(engine.yellow_flag_img, engine.yellow_flag_pos)
        if engine.red_flag_pos:
            win.blit(engine.red_flag_img, engine.red_flag_pos)
        if engine.courier_pos:
            rotated = pygame.transform.rotate(engine.courier_img, engine.courier_angle)
            rect = rotated.get_rect(center=engine.courier_pos)
            win.blit(rotated, rect.topleft)

        # Pergerakan otomatis
        if engine.is_moving:
            engine.move_smooth()

        status = "Kurir telah sampai!" if not engine.is_moving and engine.path_index >= len(engine.path) else \
                 "Mengantar..." if engine.is_moving else "Siap"
        text = font.render(f"Status: {status}", True, (0, 0, 0))
        win.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
