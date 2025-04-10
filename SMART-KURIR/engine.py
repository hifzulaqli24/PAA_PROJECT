import pygame, random, math, sys
from collections import deque

class GameEngine:
    def __init__(self, win):
        self.win = win
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
        self.current_index = 0
        self.is_moving = False
        self.speed = 2

    def load_map(self, path):
        self.map_surface = pygame.transform.scale(pygame.image.load(path), self.win.get_size())
        self.acak_posisi()

    def is_jalan(self, color):
        return color[:3] == (95, 95, 95)

    def acak_posisi(self):
        def cari_titik():
            while True:
                x, y = random.randint(50, 1150), random.randint(50, 750)
                if self.is_jalan(self.map_surface.get_at((x, y))):
                    return x, y

        self.yellow_flag_pos = cari_titik()
        self.courier_pos = list(self.yellow_flag_pos)
        self.red_flag_pos = cari_titik()
        self.path = self.bfs(self.courier_pos, self.red_flag_pos)
        self.current_index = 0
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

    def update_courier_position(self):
        if self.current_index < len(self.path):
            tx, ty = self.path[self.current_index]
            dx, dy = tx - self.courier_pos[0], ty - self.courier_pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.courier_pos = [tx, ty]
                self.current_index += 1
            else:
                self.courier_pos[0] += self.speed * dx / dist
                self.courier_pos[1] += self.speed * dy / dist
            self.update_angle_to_target(tx, ty)
        else:
            self.is_moving = False

    def update_angle_to_target(self, tx, ty):
        dx = tx - self.courier_pos[0]
        dy = ty - self.courier_pos[1]
        self.courier_angle = math.degrees(math.atan2(-dy, dx))

    def draw_path(self):
        if len(self.path) > 1:
            pygame.draw.lines(self.win, (0, 150, 255), False, self.path, 2)

    def render_all(self):
        if self.yellow_flag_pos:
            self.win.blit(self.yellow_flag_img, self.yellow_flag_pos)
        if self.red_flag_pos:
            self.win.blit(self.red_flag_img, self.red_flag_pos)
        if self.courier_pos:
            rotated_img = pygame.transform.rotate(self.courier_img, self.courier_angle)
            rect = rotated_img.get_rect(center=self.courier_pos)
            self.win.blit(rotated_img, rect.topleft)
        self.draw_path()
        if self.is_moving and self.path:
            self.update_courier_position()

    def stop(self):
        self.is_moving = False

    def keluar(self):
        self.running = False
        pygame.quit()
        sys.exit()
