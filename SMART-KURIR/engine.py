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
        self.current_task = None
        self.has_arrived_at_source = False


        self.map_surface = None
        self.map_pixels = None

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
        self.current_task = None  # "to_source" or "to_destination"

    def load_map(self, filepath):
        self.map_surface = pygame.image.load(filepath)
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        self.courier_pos = self.get_random_jalan_pos()

    def get_random_jalan_pos(self):
        while True:
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            color = self.map_surface.get_at((x, y))[:3]
            if self.is_jalan(color):
                return (x, y)

    def acak_posisi(self):
        def cari_posisi():
            while True:
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                color = self.map_surface.get_at((x, y))[:3]
                if self.is_jalan(color):
                    return (x, y)

        self.yellow_flag_pos = cari_posisi()
        self.red_flag_pos = cari_posisi()
        self.courier_pos = cari_posisi()

        self.update_angle()
        self.path = []
        self.path_index = 0
        self.is_moving = False

        # 🔥 Reset status tugas
        self.has_arrived_at_source = False
        self.current_task = None



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

        print("Path tidak tersedia.")
        return []


    def start_to_source(self):
        self.path = self.generate_path_bfs(self.courier_pos, self.yellow_flag_pos)
        self.path_index = 0
        self.is_moving = True
        self.current_task = "to_source"
        self.has_arrived_at_source = False  # Reset status

    def start_to_destination(self):
        if not self.has_arrived_at_source:
            print("Ambil paket terlebih dahulu!")
            return
        self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
        self.path_index = 0
        self.is_moving = True
        self.current_task = "to_destination"

    def update_angle(self):
        if self.path_index < len(self.path):
            dx = self.path[self.path_index][0] - self.courier_pos[0]
            dy = self.path[self.path_index][1] - self.courier_pos[1]
            angle_rad = math.atan2(-dy, dx)
            self.courier_angle = math.degrees(angle_rad)

    def update_courier_position(self):
        if self.path_index < len(self.path):
            self.courier_pos = self.path[self.path_index]
            self.update_angle()
            self.path_index += 1
        else:
            if self.current_task == "to_source":
                print("Kurir telah sampai di bendera kuning (source).")
                self.has_arrived_at_source = True
            elif self.current_task == "to_destination":
                print("Kurir telah mengantar paket ke bendera merah (destination).")
            self.is_moving = False
            self.current_task = None


    def stop(self):
        self.is_moving = False
        print("Kurir dihentikan.")

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()
