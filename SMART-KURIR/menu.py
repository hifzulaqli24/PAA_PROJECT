import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load_map_callback():
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(
            initialdir="maps",
            title="Pilih Map",
            filetypes=[("Image Files", "*.jpeg *.jpg *.png")]
        )
        root.destroy()
        if file:
            engine.load_map_and_random(file)

    def acak_callback():
        engine.randomize_positions()

    def mulai_callback():
        if engine.path and len(engine.path) > 1:
            engine.is_moving = True
            print("[INFO] Kurir mulai bergerak...")
        else:
            print("[INFO] Klik Acak dulu untuk memulai.")

    def stop_callback():
        engine.stop()

    def reset_callback():
        engine.reset_positions()

    def keluar_callback():
        engine.keluar()

    def run_gui():
        menu = tk.Tk()
        menu.title("Menu Smart Courier v7")

        tk.Button(menu, text="Load Map", command=load_map_callback).pack(pady=5)
        tk.Button(menu, text="Acak", command=acak_callback).pack(pady=5)
        tk.Button(menu, text="Mulai", command=mulai_callback).pack(pady=5)
        tk.Button(menu, text="Stop", command=stop_callback).pack(pady=5)
        tk.Button(menu, text="Reset Posisi", command=reset_callback).pack(pady=5)
        tk.Button(menu, text="Keluar", command=keluar_callback).pack(pady=5)

        menu.mainloop()

    threading.Thread(target=run_gui, daemon=True).start()
