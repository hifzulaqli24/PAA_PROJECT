import pygame
import random
import math
import sys
import os
from collections import deque

class GameEngine:
    def __init__(self, window, width, height):
        self.win = window
        self.width = width
        self.height = height
        self.running = True
        self.current_task = None
        self.has_arrived_at_source = False
        self.has_picked_package = False
        self.alert_message = None
        self.alert_timer = 0



        self.map_surface = None
        self.map_pixels = None

        self.red_flag_img = pygame.transform.scale(
            pygame.image.load("assets/red_flag.png"), (40, 40)
        )
        self.yellow_flag_img = pygame.transform.scale(
            pygame.image.load("assets/yellow.png"), (40, 40)
        )
        self.motor_img = pygame.transform.scale(
            pygame.image.load("assets/motor.png"), (35, 70)
        )
        self.motor_img = pygame.transform.scale(
            pygame.image.load("assets/motor.png"), (30, 65)
        )
        self.truck_img = pygame.transform.scale(
            pygame.image.load("assets/truk.png"), (40, 80)
        )

        self.courier_types = {
            "map1.jpeg": {
                0: "motor",
                1: "truck",
                2: "motor",
                3: "truck",
            },
            "map2.jpeg": {
                0: "truck",
                1: "motor",
                2: "truck",
                3: "motor",
            }
        }

        self.courier_img = self.motor_img  # default sementara

        self.red_flag_pos = None
        self.yellow_flag_pos = None
        self.courier_pos = None
        self.courier_angle = 0

        self.path = []
        self.path_index = 0
        self.is_moving = False
        self.current_task = None  # "to_source" or "to_destination"
        self.position_index = 0


        self.current_map_name = None  # Untuk menyimpan nama file map yang digunakan

        self.fixed_positions = {
            "map1.jpeg": {
                "kurir": [(786, 683), (1263, 669), (627, 246), (90, 665)],
                "kuning": [(401, 192), (97, 448), (897, 649), (581, 553)],
                "merah": [(1181, 355), (1189, 153), (1286, 440), (1083, 225)],
            },
            "map2.jpeg": {
                "kurir": [(269, 19), (13, 418), (915, 7), (603, 662)],
                "kuning": [(765, 121), (777, 246), (479, 560), (291, 264)],
                "merah": [(1228, 481), (405, 128), (1197, 283), (1192, 132)],
            }   
        }



    def show_alert(self, message, duration=120):  # 120 frame = 2 detik kalau 60 fps
        self.alert_message = message
        self.alert_timer = duration

    def draw_alert(self):
        if self.alert_message:
            # Kotak alert di tengah layar
            alert_width, alert_height = 400, 200
            alert_x = (self.width - alert_width) // 2
            alert_y = (self.height - alert_height) // 2
            pygame.draw.rect(self.win, (240, 240, 240), (alert_x, alert_y, alert_width, alert_height), border_radius=10)
            pygame.draw.rect(self.win, (100, 100, 100), (alert_x, alert_y, alert_width, alert_height), 2, border_radius=10)

            # Teks pesan
            font = pygame.font.SysFont(None, 28)
            text_surface = font.render(self.alert_message, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 30))
            self.win.blit(text_surface, text_rect)

            # Tombol OK
            self.ok_button_rect = pygame.Rect(alert_x + 150, alert_y + 120, 100, 40)
            pygame.draw.rect(self.win, (180, 180, 180), self.ok_button_rect, border_radius=5)
            pygame.draw.rect(self.win, (100, 100, 100), self.ok_button_rect, 2, border_radius=5)

            ok_text = font.render("OK", True, (0, 0, 0))
            ok_rect = ok_text.get_rect(center=self.ok_button_rect.center)
            self.win.blit(ok_text, ok_rect)

    def handle_alert_click(self, pos):
        if self.alert_message and hasattr(self, 'ok_button_rect') and self.ok_button_rect.collidepoint(pos):
            self.alert_message = None

    def load_map(self, filepath):
        self.map_surface = pygame.image.load(filepath)
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        self.current_map_name = os.path.basename(filepath)  # ⬅️ Tambahkan ini

    def get_random_jalan_pos(self):
        while True:
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            color = self.map_surface.get_at((x, y))[:3]
            if self.is_jalan(color):
                return (x, y)

    def acak_posisi(self):
        map_name = self.current_map_name
        if map_name in self.fixed_positions:
            positions = self.fixed_positions[map_name]
            index = self.position_index % len(positions["kurir"])  # pastikan rotasi
            # Tentukan jenis kurir berdasarkan index

            
            self.courier_pos = positions["kurir"][index]
            self.yellow_flag_pos = positions["kuning"][index]
            self.red_flag_pos = positions["merah"][index]

            # Tentukan gambar kurir berdasarkan tipe dan map
            map_name = self.current_map_name
            courier_type = self.courier_types.get(map_name, {}).get(index, "motor")  # default motor

            if courier_type == "motor":
                self.courier_img = self.motor_img
            else:
                self.courier_img = self.truck_img

            self.update_angle()
            self.path = []
            self.path_index = 0
            self.is_moving = False

            # 🔥 Reset status tugas
            self.has_arrived_at_source = False
            self.current_task = None
            self.has_picked_package = False

            # Naikkan index untuk pemanggilan berikutnya
            self.position_index += 1
        else:
            print("Map tidak dikenali untuk posisi tetap.")





    def is_jalan(self, color):
        r, g, b = color
        return all(90 <= c <= 150 for c in (r, g, b))    

    def generate_path_bfs(self, start, end):
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == end:
             return path


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

         # DEBUG: cek warna jalan
        print("Warna pada posisi kurir:", self.map_surface.get_at(self.courier_pos)[:3])
        print("Warna pada tujuan (kuning):", self.map_surface.get_at(self.yellow_flag_pos)[:3])

        if not self.path:
            self.show_alert("Tidak ada jalur ke bendera kuning!")
            return
        self.path_index = 0
        self.is_moving = True
        self.current_task = "to_source"
        self.has_arrived_at_source = False



    def start_to_destination(self):
        if not self.has_picked_package:
            self.show_alert("Ambil paket terlebih dahulu!")
            return
        
        print("Warna pada posisi kurir:", self.map_surface.get_at(self.courier_pos)[:3])
        print("Warna pada tujuan (merah):", self.map_surface.get_at(self.red_flag_pos)[:3])

        self.path = self.generate_path_bfs(self.courier_pos, self.red_flag_pos)
        if not self.path:
            self.show_alert("Tidak ada jalur ke bendera merah!")
            return
        self.path_index = 0
        self.is_moving = True
        self.current_task = "to_destination"

    def update_angle(self):
        if self.path_index < len(self.path) - 1:
            # Ambil dua titik, titik sekarang dan titik berikutnya
            x1, y1 = self.path[self.path_index]
            x2, y2 = self.path[self.path_index + 1]
            
            dx = x2 - x1
            dy = y2 - y1
            
            # Menghitung sudut dengan atan2 untuk memastikan rotasi yang tepat
            angle_rad = math.atan2(dy, dx)
            
            # Konversi ke derajat dan sesuaikan dengan rotasi yang benar
            self.courier_angle = -math.degrees(angle_rad) + 90  # +90 untuk koreksi karena gambar awal menghadap ke atas



    def update_courier_position(self):
        if self.path_index < len(self.path):
            self.courier_pos = self.path[self.path_index]
            self.update_angle()  # Update arah kurir
            self.path_index += 1
        else:
            if self.current_task == "to_source":
                print("Kurir telah sampai di bendera kuning (source).")
                self.has_arrived_at_source = True
                self.has_picked_package = True  # Paket telah diambil
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
