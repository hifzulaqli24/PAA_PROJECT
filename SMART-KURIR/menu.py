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
            engine.finished = False
            status_label.config(text="Kurir mulai bergerak.")
        else:
            status_label.config(text="Path belum ada. Klik Acak.")

    def stop_callback():
        engine.stop()
        status_label.config(text="Kurir berhenti.")

    def keluar_callback():
        engine.keluar()

    def log_callback():
        log_window = tk.Toplevel(menu)
        log_window.title("Log Perjalanan")
        log_text = tk.Text(log_window, width=50, height=15)
        log_text.pack()
        log_text.insert(tk.END, "\n".join(engine.log))

    def run():
        global menu
        menu = tk.Tk()
        menu.title("Smart Courier - Menu v13")

        tk.Button(menu, text="Load Map", command=load_map_callback).pack(pady=4)
        tk.Button(menu, text="Acak", command=acak_callback).pack(pady=4)
        tk.Button(menu, text="Mulai", command=mulai_callback).pack(pady=4)
        tk.Button(menu, text="Stop", command=stop_callback).pack(pady=4)
        tk.Button(menu, text="Lihat Log", command=log_callback).pack(pady=4)
        tk.Button(menu, text="Keluar", command=keluar_callback).pack(pady=4)

        global status_label
        status_label = tk.Label(menu, text="Status: Menunggu perintah...")
        status_label.pack(pady=10)

        menu.mainloop()

    threading.Thread(target=run, daemon=True).start()
