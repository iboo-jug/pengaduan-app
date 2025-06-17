import sqlite3
from werkzeug.security import generate_password_hash

# Buat koneksi ke database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Data user baru
username = 'admin'
password = generate_password_hash('admin123')
role = 'admin'

# Masukkan ke tabel users
c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password, role))

conn.commit()
conn.close()

print(f"Admin '{username}' berhasil dibuat!")
