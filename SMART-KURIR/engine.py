import pygame
import math
import random
import sys
from collections import deque

class GameEngine:
    def __init__(self, window, width, height):
        self.win = window
        self.width = width
        self.height = height
        self.running = True

        self.map_surface = None
        self.red_flag_img = pygame.transform.scale(pygame.image.load("assets/red_flag.png"), (50, 50))
        self.yellow_flag_img = pygame.transform.scale(pygame.image.load("assets/yellow.png"), (50, 44))
        self.courier_img = pygame.transform.scale(pygame.image.load("assets/kurir.png"), (40, 40))

        self.red_flag_pos = None
        self.yellow_flag_pos = None
        self.courier_pos = None
        self.courier_angle = 0

        self.path = []
        self.path_index = 0
        self.is_moving = False
        self.speed = 2  # smooth speed

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
                color = self.map_surface.get_at((x, y))[:3]
                if self.is_jalan(color):
                    return (x, y)

        self.yellow_flag_pos = cari_posisi()
        self.courier_pos = list(self.yellow_flag_pos)
        self.red_flag_pos = cari_posisi()
        self.update_angle()
        self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
        self.path_index = 0

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
                        color = self.map_surface.get_at((nx, ny))[:3]
                        if self.is_jalan(color):
                            visited.add((nx, ny))
                            queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    def update_angle(self):
        if self.red_flag_pos and self.courier_pos:
            dx = self.red_flag_pos[0] - self.courier_pos[0]
            dy = self.red_flag_pos[1] - self.courier_pos[1]
            angle = math.degrees(math.atan2(-dy, dx))
            self.courier_angle = angle

    def move_smooth(self):
        if self.path_index < len(self.path):
            target = self.path[self.path_index]
            dx = target[0] - self.courier_pos[0]
            dy = target[1] - self.courier_pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.courier_pos = list(target)
                self.path_index += 1
            else:
                self.courier_pos[0] += self.speed * dx / dist
                self.courier_pos[1] += self.speed * dy / dist
            self.update_angle()
        else:
            self.is_moving = False

    def stop(self):
        self.is_moving = False

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()
