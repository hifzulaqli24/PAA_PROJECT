import pygame
import math

class GameEngine:
    def __init__(self, window, width, height):
        self.win = window
        self.width = width
        self.height = height

        self.map_surface = None

        # Load dan ubah ukuran gambar
        self.red_flag_img = pygame.transform.scale(pygame.image.load("assets/red_flag.png"), (50, 50))
        self.yellow_flag_img = pygame.transform.scale(pygame.image.load("assets/yellow.png"), (50, 44))
        self.courier_img = pygame.transform.scale(pygame.image.load("assets/kurir.png"), (40, 40))

        # Posisi tetap (statik)
        self.yellow_flag_pos = (200, 300)
        self.red_flag_pos = (900, 600)
        self.courier_pos = self.yellow_flag_pos
        self.courier_angle = 0
        self.update_angle()

    def load_static_map(self, filepath):
        self.map_surface = pygame.image.load(filepath)
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))

    def update_angle(self):
        dx = self.red_flag_pos[0] - self.courier_pos[0]
        dy = self.red_flag_pos[1] - self.courier_pos[1]
        angle_rad = math.atan2(-dy, dx)
        self.courier_angle = math.degrees(angle_rad)
