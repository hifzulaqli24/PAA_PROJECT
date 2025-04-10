import pygame
import math
import random
import sys
from collections import deque

class GameEngine:
    def __init__(self, win, width, height):
        self.win = winimport pygame
import math
import random
import sys
from collections import deque

class GameEngine:
    def __init__(self, win, width, height):
        self.win = win
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
        self.speed = 2

        self.status_log = "Status: Menunggu peta dimuat."

    def load_map_and_random(self, filepath):
        self.map_surface = pygame.image.load(filepath)
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        self.randomize_positions()
        self.status_log = "Map dimuat. Posisi diacak."

    def is_jalan(self, color):
        r, g, b = color
        return 90 <= r <= 100 and 90 <= g <= 100 and 90 <= b <= 100

    def randomize_positions(self):
        if not self.map_surface:
            self.status_log = "Peta belum dimuat."
            return

        def cari_titik():
            while True:
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                if self.is_jalan(self.map_surface.get_at((x, y))[:3]):
                    return (x, y)

        self.yellow_flag_pos = cari_titik()
        self.courier_pos = list(self.yellow_flag_pos)
        self.red_flag_pos = cari_titik()
        self.update_angle()

        self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
        self.path_index = 0
        self.is_moving = False

        if self.path:
            self.status_log = "Posisi acak dan path ditemukan."
        else:
            self.status_log = "Path tidak ditemukan."

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
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    if self.is_jalan(self.map_surface.get_at((nx, ny))[:3]):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
        return []

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
            self.status_log = "Kurir telah sampai tujuan."

    def update_angle(self):
        if self.red_flag_pos and self.courier_pos:
            dx = self.red_flag_pos[0] - self.courier_pos[0]
            dy = self.red_flag_pos[1] - self.courier_pos[1]
            angle = math.degrees(math.atan2(-dy, dx))
            self.courier_angle = angle

    def draw_flags(self):
        if self.yellow_flag_pos:
            self.win.blit(self.yellow_flag_img, self.yellow_flag_pos)
        if self.red_flag_pos:
            self.win.blit(self.red_flag_img, self.red_flag_pos)

    def draw_courier(self):
        if self.courier_pos:
            rotated = pygame.transform.rotate(self.courier_img, self.courier_angle)
            rect = rotated.get_rect(center=self.courier_pos)
            self.win.blit(rotated, rect.topleft)

    def draw_path(self):
        if self.path:
            for p in self.path:
                pygame.draw.circle(self.win, (0, 0, 255), p, 2)

    def get_status_text(self):
        return self.status_log

    def stop(self):
        self.is_moving = False
        self.status_log = "Kurir dihentikan."

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()

        self.width = width
        self.height = height
        self.running = True

        # === ORANG 2: VISUALISASI ===
        self.map_surface = None
        self.red_flag_img = pygame.transform.scale(pygame.image.load("assets/red_flag.png"), (50, 50))
        self.yellow_flag_img = pygame.transform.scale(pygame.image.load("assets/yellow.png"), (50, 44))
        self.courier_img = pygame.transform.scale(pygame.image.load("assets/kurir.png"), (40, 40))

        self.red_flag_pos = None
        self.yellow_flag_pos = None
        self.courier_pos = None
        self.courier_angle = 0

        # === ORANG 1: LOGIKA & BFS ===
        self.path = []
        self.path_index = 0
        self.is_moving = False
        self.speed = 2

    def load_map_and_random(self, filepath):
        self.map_surface = pygame.image.load(filepath)
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        self.randomize_positions()

    # ORANG 1
    def is_jalan(self, color):
        r, g, b = color
        return 90 <= r <= 100 and 90 <= g <= 100 and 90 <= b <= 100

    def randomize_positions(self):
        def cari_titik():
            while True:
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                if self.is_jalan(self.map_surface.get_at((x, y))[:3]):
                    return (x, y)

        self.yellow_flag_pos = cari_titik()
        self.courier_pos = list(self.yellow_flag_pos)
        self.red_flag_pos = cari_titik()
        self.update_angle()

        self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
        self.path_index = 0
        self.is_moving = False

    # ORANG 1
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
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    if self.is_jalan(self.map_surface.get_at((nx, ny))[:3]):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    # ORANG 2
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

    def update_angle(self):
        if self.red_flag_pos and self.courier_pos:
            dx = self.red_flag_pos[0] - self.courier_pos[0]
            dy = self.red_flag_pos[1] - self.courier_pos[1]
            angle = math.degrees(math.atan2(-dy, dx))
            self.courier_angle = angle

    # ORANG 2
    def draw_flags(self):
        if self.yellow_flag_pos:
            self.win.blit(self.yellow_flag_img, self.yellow_flag_pos)
        if self.red_flag_pos:
            self.win.blit(self.red_flag_img, self.red_flag_pos)

    def draw_courier(self):
        if self.courier_pos:
            rotated = pygame.transform.rotate(self.courier_img, self.courier_angle)
            rect = rotated.get_rect(center=self.courier_pos)
            self.win.blit(rotated, rect.topleft)

    def draw_path(self):
        if self.path:
            for p in self.path:
                pygame.draw.circle(self.win, (0, 0, 255), p, 2)

    def get_status_text(self):
        if not self.is_moving and self.path_index >= len(self.path):
            return "Status: Kurir telah sampai."
        elif self.is_moving:
            return "Status: Mengantar..."
        else:
            return "Status: Siap."

    # ORANG 3
    def stop(self):
        self.is_moving = False

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()
