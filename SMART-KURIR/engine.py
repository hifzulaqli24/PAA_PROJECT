import pygame
import random
import math
import sys
from collections import deque

class GameEngine:
    def __init__(self, window, width, height):
        self.win = window
        self.width = width
        self.height = height
        self.running = True

        self.map_surface = None

        self.red_flag_img = pygame.transform.scale(
            pygame.image.load("assets/red_flag.png"), (50, 50)
        )
        self.yellow_flag_img = pygame.transform.scale(
            pygame.image.load("assets/yellow.png"), (50, 44)
        )
        self.courier_img = pygame.transform.scale(
            pygame.image.load("assets/kurir.png"), (40, 40)
        )

        self.red_flag_pos = None
        self.yellow_flag_pos = None
        self.courier_pos = None
        self.courier_angle = 0

        self.path = []
        self.path_index = 0
        self.is_moving = False
        self.speed = 2

    def load_map(self, filepath):
        try:
            raw_image = pygame.image.load(filepath)
            self.map_surface = pygame.transform.scale(raw_image, (self.width, self.height))
            print(f"Map loaded from: {filepath}")
            self.acak_posisi()
        except Exception as e:
            print(f"Gagal memuat peta: {e}")
            self.map_surface = None

    def acak_posisi(self):
        def cari_posisi():
            for _ in range(1000):
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                color = self.map_surface.get_at((x, y))[:3]
                if self.is_jalan(color):
                    return (x, y)
            return None

        start_pos = cari_posisi()
        end_pos = cari_posisi()

        if start_pos and end_pos:
            self.yellow_flag_pos = start_pos
            self.courier_pos = list(start_pos)
            self.red_flag_pos = end_pos
            self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
            self.path_index = 0
            self.update_angle()
            print("Posisi acak berhasil diatur.")
        else:
            self.path = []
            self.yellow_flag_pos = None
            self.red_flag_pos = None
            self.courier_pos = None
            print("Gagal menemukan posisi yang valid.")

    def is_jalan(self, color):
        r, g, b = color
        return abs(r - 95) <= 10 and abs(g - 95) <= 10 and abs(b - 95) <= 10

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
            angle_rad = math.atan2(-dy, dx)
            self.courier_angle = math.degrees(angle_rad)

    def update_angle_to_target(self, target_x, target_y):
        dx = target_x - self.courier_pos[0]
        dy = target_y - self.courier_pos[1]
        if dx != 0 or dy != 0:
            angle_rad = math.atan2(-dy, dx)
            self.courier_angle = math.degrees(angle_rad)

    def update_courier_position(self):
        if self.path_index < len(self.path):
            target = self.path[self.path_index]
            tx, ty = target
            cx, cy = self.courier_pos
            dx, dy = tx - cx, ty - cy
            dist = math.hypot(dx, dy)

            if dist < self.speed:
                self.courier_pos = list(target)
                self.path_index += 1
            else:
                move_x = self.speed * dx / dist
                move_y = self.speed * dy / dist
                self.courier_pos[0] += move_x
                self.courier_pos[1] += move_y

            self.update_angle_to_target(tx, ty)
        else:
            self.is_moving = False

    def stop(self):
        self.is_moving = False

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()
