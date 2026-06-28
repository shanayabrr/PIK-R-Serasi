import json
import os
from datetime import datetime
from functools import wraps
from flask import session, flash, redirect, url_for

DB_PATH = 'database/users.json'

def load_users():
    """Mengambil data user dari Data Layer (JSON)."""
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_users(users):
    """Menyimpan data user ke Data Layer (JSON)."""
    with open(DB_PATH, 'w') as f:
        json.dump(users, f, indent=4)

def validate_age(birth_date_str):
    """
    Business Logic: Validasi Usia sesuai Proposal (10-24 Tahun).
    Menghitung selisih tahun antara hari ini dengan tanggal lahir.
    """
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return 10 <= age <= 24
    except ValueError:
        return False

def authenticate_user(username, password):
    """Logika untuk memverifikasi kredensial login."""
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def register_user(username, password, birth_date, role):
    """Logika pendaftaran user baru dengan validasi berlapis."""
    # 1. Validasi Usia (Aturan Bisnis Utama)
    if not validate_age(birth_date):
        return False, "Usia tidak memenuhi syarat (Wajib 10-24 Tahun)."

    users = load_users()
    
    # 2. Cek apakah username sudah ada
    if any(u['username'] == username for u in users):
        return False, "Username sudah terdaftar."

    # 3. Proses Simpan
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password, # Catatan: Idealnya gunakan werkzeug.security untuk hashing
        "birth_date": birth_date,
        "role": role
    }
    users.append(new_user)
    save_users(users)
    return True, "Registrasi Berhasil!"

def login_required(f):
    """Decorator untuk membatasi akses halaman (Hanya untuk yang sudah login)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Sesi berakhir atau Anda belum login.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function