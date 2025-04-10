import pygame
import random
import math
from collections import deque

class GameEngine:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.map_surface = None

        self.yellow_flag_img = pygame.transform.scale(
            pygame.image.load("assets/yellow.png"), (50, 44)
        )
        self.red_flag_img = pygame.transform.scale(
            pygame.image.load("assets/red_flag.png"), (50, 50)
        )
        self.courier_img = pygame.transform.scale(
            pygame.image.load("assets/kurir.png"), (40, 40)
        )

        self.yellow_flag_pos = None
        self.red_flag_pos = None
        self.courier_pos = None
        self.courier_angle = 0

        self.path = []
        self.path_index = 0

    def load_map_and_random(self, filepath):
        self.map_surface = pygame.image.load(filepath)
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        self.randomize_positions()

    def is_jalan(self, color):
        r, g, b = color
        return abs(r - 95) <= 10 and abs(g - 95) <= 10 and abs(b - 95) <= 10

    def randomize_positions(self):
        def cari_posisi():
            while True:
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                if self.is_jalan(self.map_surface.get_at((x, y))[:3]):
                    return (x, y)

        self.yellow_flag_pos = cari_posisi()
        self.courier_pos = self.yellow_flag_pos
        self.red_flag_pos = cari_posisi()
        self.update_angle()
        self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
        self.path_index = 0

    def update_angle(self):
        dx = self.red_flag_pos[0] - self.courier_pos[0]
        dy = self.red_flag_pos[1] - self.courier_pos[1]
        angle_rad = math.atan2(-dy, dx)
        self.courier_angle = math.degrees(angle_rad)

    def update_courier_position(self):
        if self.path_index < len(self.path):
            self.courier_pos = self.path[self.path_index]
            self.update_angle()
            self.path_index += 1

    def generate_path_bfs(self, start, end):
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        while queue:
            (x, y), path = queue.popleft()
            if abs(x - end[0]) < 3 and abs(y - end[1]) < 3:
                return path + [end]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        if self.is_jalan(self.map_surface.get_at((nx, ny))[:3]):
                            visited.add((nx, ny))
                            queue.append(((nx, ny), path + [(nx, ny)]))
        return []
