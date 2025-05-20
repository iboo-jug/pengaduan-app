import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("DELETE FROM complaints")

conn.commit()
conn.close()

print("Semua data pengaduan berhasil dihapus.")
