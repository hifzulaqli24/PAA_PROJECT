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
    max_attempts = 1000

    def cari_posisi():
        for _ in range(max_attempts):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            color = self.map_surface.get_at((x, y))[:3]
            if self.is_jalan(color):
                return (x, y)
        print("Gagal menemukan posisi yang valid.")
        return None

    start_pos = cari_posisi()
    end_pos = cari_posisi()

    if start_pos and end_pos:
        self.yellow_flag_pos = start_pos
        self.courier_pos = start_pos
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
