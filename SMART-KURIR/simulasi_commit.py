import os
import subprocess
from datetime import datetime, timedelta
import random

# Ganti dengan daftar contributor GitHub kelompokmu
contributors = [
    ("Ikhsan Dimas", "ikhsan@example.com"),
    ("Adelia Purba", "adelia@example.com"),
    ("Ariq Akbar", "ariq@example.com"),
    ("Caera Nadira", "caera@example.com"),
    ("Hifzul Aqli", "hifzul@example.com"),
]

# Rentang tanggal kerja
start_date = datetime(2024, 3, 19)
end_date = datetime(2024, 4, 13)
days = (end_date - start_date).days + 1

for i in range(days):
    date = start_date + timedelta(days=i)
    jumlah_commit = random.randint(1, 3)  # Jumlah commit per hari

    for _ in range(jumlah_commit):
        name, email = random.choice(contributors)
        waktu = datetime(
            date.year, date.month, date.day,
            random.randint(9, 17), random.randint(0, 59)
        )
        waktu_str = waktu.strftime("%Y-%m-%dT%H:%M:%S")

        # Bikin perubahan kecil agar bisa di-commit
        with open("dummy.txt", "a") as f:
            f.write(f"{waktu_str} oleh {name}\n")

        subprocess.run(["git", "add", "."], check=True)

        # Atur environment untuk commit
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = waktu_str
        env["GIT_COMMITTER_DATE"] = waktu_str
        env["GIT_AUTHOR_NAME"] = name
        env["GIT_AUTHOR_EMAIL"] = email
        env["GIT_COMMITTER_NAME"] = name
        env["GIT_COMMITTER_EMAIL"] = email

        subprocess.run(
            ["git", "commit", "-m", f"Commit dari {name}"],
            env=env,
            check=True
        )

print("Simulasi commit selesai ✅")
