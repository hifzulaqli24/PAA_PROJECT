import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load_map_callback():
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(
            initialdir="maps",
            title="Pilih Map",
            filetypes=[("Image Files", "*.jpeg *.jpg *.png")]
        )
        root.destroy()
        if filepath:
            engine.load_map(filepath)
            print("[INFO] Map berhasil dimuat.")

    def acak_callback():
        engine.acak_posisi()
        print("[INFO] Posisi acak untuk kurir dan tujuan sudah diatur.")

    def mulai_callback():
        if engine.path and len(engine.path) > 1:
            engine.is_moving = True
            print("[INFO] Kurir mulai bergerak.")
        else:
            print("[WARNING] Path belum tersedia. Klik Acak terlebih dahulu.")

    def stop_callback():
        engine.stop()
        print("[INFO] Pergerakan kurir dihentikan.")

    def keluar_callback():
        engine.keluar()

    def run_menu():
        menu = tk.Tk()
        menu.title("Menu Smart Courier")

        tk.Label(menu, text="Smart Courier Control Panel", font=("Arial", 14, "bold")).pack(pady=10)

        buttons = [
            ("Load Map", load_map_callback),
            ("Acak", acak_callback),
            ("Mulai", mulai_callback),
            ("Stop", stop_callback),
            ("Keluar", keluar_callback),
        ]

        for label, func in buttons:
            tk.Button(menu, text=label, command=func, width=20).pack(pady=5)

        menu.mainloop()

    threading.Thread(target=run_menu, daemon=True).start()
