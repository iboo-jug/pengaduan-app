from flask import Flask, render_template, request, redirect, session, url_for, Response
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import csv
from io import StringIO
import logging
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

# Inisialisasi database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Tabel pengaduan
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_type TEXT NOT NULL,
            location_description TEXT NOT NULL,
            details TEXT NOT NULL,
            contact_email TEXT,
            submission_timestamp TEXT,
            status TEXT DEFAULT "Baru"
        )
    ''')

    # Tabel admin
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT "admin"
        )
    ''')

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                  ('admin', generate_password_hash('admin123')))
    
    conn.commit()
    conn.close()

# Route: Form pengaduan
@app.route('/')
def form():
    return render_template('form.html')

# Route: Submit pengaduan
@app.route('/submit', methods=['POST'])
def submit():
    data = (
        request.form['complaint_type'],
        request.form['location_description'],
        request.form['details'],
        request.form.get('contact_email'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO complaints (complaint_type, location_description, details, contact_email, submission_timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()
    return render_template('success.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Login gagal, periksa username/password."
    return render_template('login.html')

# Route: Dashboard admin + Search, Filter, Pagination
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Hitung jumlah pengaduan baru (untuk notifikasi)
    c.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Baru'")
    new_count = c.fetchone()[0]

    # Ambil data untuk tampilan dashboard
    if search:
        c.execute("""
            SELECT * FROM complaints 
            WHERE complaint_type LIKE ? OR location_description LIKE ? OR details LIKE ? OR contact_email LIKE ?
            ORDER BY submission_timestamp DESC
            LIMIT ? OFFSET ?
        """, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset))

        c_total = conn.execute("""
            SELECT COUNT(*) FROM complaints 
            WHERE complaint_type LIKE ? OR location_description LIKE ? OR details LIKE ? OR contact_email LIKE ?
        """, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'))
    else:
        c.execute("""
            SELECT * FROM complaints 
            ORDER BY submission_timestamp DESC 
            LIMIT ? OFFSET ?
        """, (per_page, offset))

        c_total = conn.execute("SELECT COUNT(*) FROM complaints")

    complaints = c.fetchall()
    total = c_total.fetchone()[0]
    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template('dashboard.html', 
                       complaints=complaints, 
                       search=search, 
                       page=page, 
                       total_pages=total_pages,
                       new_complaint_count=new_count)


    
# Route: Export to CSV
@app.route('/export')
def export():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT complaint_type, location_description, details, contact_email, submission_timestamp FROM complaints")
    rows = c.fetchall()
    conn.close()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Jenis Pengaduan', 'Lokasi', 'Isi Pengaduan', 'Email Kontak', 'Waktu Submit'])
    writer.writerows(rows)

    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=pengaduan_export.csv"
    return output

# Route: Logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('form'))

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/update_status/<int:complaint_id>', methods=['POST'])
def update_status(complaint_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    new_status = request.form['status']

    if new_status not in ['Baru', 'Progress', 'Selesai']:
        return "Status tidak valid.", 400 

    # Lanjut update ke database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE complaints SET status = ? WHERE id = ?", (new_status, complaint_id))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))


# Jalankan server
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
