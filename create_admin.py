from app import db
from models import User
from werkzeug.security import generate_password_hash

username = "admin"
password = "admin123"

# Buat user baru
new_user = User(
    username=username,
    password_hash=generate_password_hash(password),
    role="admin"
)

# Simpan ke database
db.session.add(new_user)
db.session.commit()

print(f"Admin '{username}' berhasil dibuat!")
