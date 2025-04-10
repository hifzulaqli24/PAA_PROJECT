import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load_map_callback():
        file = filedialog.askopenfilename(
            initialdir="maps",
            title="Pilih Map",
            filetypes=[("Image Files", "*.jpeg *.jpg *.png")]
        )
        if file:
            engine.load_map_and_random(file)
            status_label.config(text="Map dimuat dan posisi diacak.")

    def acak_callback():
        engine.randomize_positions()
        status_label.config(text="Posisi acak berhasil.")

    def mulai_callback():
        if engine.path and len(engine.path) > 1:
            engine.is_moving = True
            status_label.config(text="Kurir mulai berjalan.")
        else:
            status_label.config(text="Klik Acak terlebih dahulu.")

    def stop_callback():
        engine.stop()
        status_label.config(text="Kurir berhenti.")

    def keluar_callback():
        engine.keluar()

    def run():
        menu = tk.Tk()
        menu.title("Smart Courier - Menu v12")

        tk.Button(menu, text="Load Map", command=load_map_callback).pack(pady=5)
        tk.Button(menu, text="Acak", command=acak_callback).pack(pady=5)
        tk.Button(menu, text="Mulai", command=mulai_callback).pack(pady=5)
        tk.Button(menu, text="Stop", command=stop_callback).pack(pady=5)
        tk.Button(menu, text="Keluar", command=keluar_callback).pack(pady=5)

        global status_label
        status_label = tk.Label(menu, text="Status: Menunggu perintah...")
        status_label.pack(pady=10)

        menu.mainloop()

    threading.Thread(target=run, daemon=True).start()
