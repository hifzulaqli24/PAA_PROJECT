import pygame, random, math, sys
from collections import deque

class GameEngine:
    def __init__(self, win):
        self.win = win
        self.running = True
        self.map_surface = None
        self.red_img = pygame.transform.scale(pygame.image.load("assets/red_flag.png"), (50, 50))
        self.yellow_img = pygame.transform.scale(pygame.image.load("assets/yellow.png"), (50, 44))
        self.kurir_img = pygame.transform.scale(pygame.image.load("assets/kurir.png"), (40, 40))
        self.red_pos = self.yellow_pos = self.kurir_pos = None
        self.angle = 0
        self.path = []
        self.idx = 0
        self.is_moving = False
        self.speed = 2

    def load_map_and_random(self, path):
        self.map_surface = pygame.transform.scale(pygame.image.load(path), self.win.get_size())
        self.randomize_positions()

    def is_jalan(self, color):
        return all(90 <= c <= 100 for c in color[:3])

    def randomize_positions(self):
        def cari_titik():
            while True:
                x, y = random.randint(50, 1150), random.randint(50, 750)
                if self.is_jalan(self.map_surface.get_at((x, y))):
                    return x, y
        self.yellow_pos = cari_titik()
        self.kurir_pos = list(self.yellow_pos)
        self.red_pos = cari_titik()
        self.path = self.bfs(self.kurir_pos, self.red_pos)
        self.idx = 0
        self.update_angle()
        self.is_moving = False

    def bfs(self, start, end):
        visited = set()
        queue = deque([(start, [start])])
        while queue:
            (x, y), path = queue.popleft()
            if abs(x - end[0]) < 3 and abs(y - end[1]) < 3:
                return path + [end]
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(1,-1),(-1,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < 1200 and 0 <= ny < 800 and (nx, ny) not in visited:
                    if self.is_jalan(self.map_surface.get_at((nx, ny))):
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
        return []

    def move_smooth(self):
        if self.idx < len(self.path):
            tx, ty = self.path[self.idx]
            dx, dy = tx - self.kurir_pos[0], ty - self.kurir_pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.kurir_pos = [tx, ty]
                self.idx += 1
            else:
                self.kurir_pos[0] += self.speed * dx / dist
                self.kurir_pos[1] += self.speed * dy / dist
            self.update_angle()
        else:
            self.is_moving = False

    def update_angle(self):
        dx, dy = self.red_pos[0] - self.kurir_pos[0], self.red_pos[1] - self.kurir_pos[1]
        self.angle = math.degrees(math.atan2(-dy, dx))

    def draw_flags(self):
        if self.yellow_pos:
            pygame.draw.circle(self.win, (255, 255, 0), self.yellow_pos, 6)
            self.win.blit(self.yellow_img, self.yellow_pos)
        if self.red_pos:
            pygame.draw.circle(self.win, (255, 0, 0), self.red_pos, 6)
            self.win.blit(self.red_img, self.red_pos)

    def draw_courier(self):
        if self.kurir_pos:
            rotated = pygame.transform.rotate(self.kurir_img, self.angle)
            rect = rotated.get_rect(center=self.kurir_pos)
            self.win.blit(rotated, rect.topleft)

    def draw_path(self):
        if len(self.path) > 1:
            pygame.draw.lines(self.win, (0, 100, 255), False, self.path, 2)

    def render_all(self):
        self.draw_path()
        self.draw_flags()
        self.draw_courier()
        if self.is_moving:
            self.move_smooth()

    def stop(self):
        self.is_moving = False

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()
