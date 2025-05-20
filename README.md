# pengaduan-app

Aplikasi Pengaduan Masyarakat

Aplikasi web sederhana untuk mengelola dan memproses pengaduan masyarakat secara online. Dibuat menggunakan Python Flask dan SQLite. Proyek ini merupakan bagian dari Capstone Project untuk studi Sistem Informasi.

Fitur Utama
Formulir pengaduan online

Dashboard admin untuk melihat dan mengelola pengaduan

Login admin

Penyimpanan data menggunakan SQLite

Responsive (dapat diakses dari berbagai perangkat)

Teknologi yang Digunakan
Python 3

Flask

SQLite

HTML dan CSS (Tailwind)

Railway (deployment)

Struktur Direktori
pengaduan-app/

app.py (file utama aplikasi)

create_admin.py (script untuk membuat akun admin)

clear_data.py (script hapus data - hanya untuk keperluan development)

cek_tabel.py (script untuk mengecek tabel SQLite - hanya untuk development)

database.db (file database SQLite)

templates/ (folder untuk file HTML)

static/ (folder untuk file CSS)

requirements.txt (daftar dependency Python)

runtime.txt, render.yaml, Procfile (file untuk keperluan deployment)

.gitignore

README.md

Cara Menjalankan Aplikasi Secara Lokal
Clone repositori ini dan masuk ke dalam foldernya.

Buat virtual environment (opsional) dan aktifkan.

Install semua dependency yang dibutuhkan menggunakan file requirements.txt.

Jalankan file app.py untuk memulai aplikasi.

Buka browser dan akses ke http://localhost:5000.

Akun Admin
Untuk membuat akun admin, jalankan file create_admin.py. Ikuti instruksi untuk memasukkan username dan password.

Catatan Developer
File berikut hanya digunakan saat development dan tidak disertakan dalam git karena sudah dimasukkan ke .gitignore:

clear_data.py

cek_tabel.py

Deployment
Aplikasi ini dideploy menggunakan Railway.

Link aplikasi live:
https://pengaduan-app-production.up.railway.app

Lisensi
Proyek ini dilisensikan di bawah MIT License.