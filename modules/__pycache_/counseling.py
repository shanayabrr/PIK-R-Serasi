import json
import os
from datetime import datetime

DB_SESSIONS = 'database/sessions.json'

def load_sessions():
    """Data Access: Mengambil semua data sesi dari JSON."""
    if not os.path.exists(DB_SESSIONS):
        return []
    with open(DB_SESSIONS, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_sessions(sessions):
    """Data Access: Menyimpan data sesi ke JSON."""
    with open(DB_SESSIONS, 'w') as f:
        json.dump(sessions, f, indent=4)

def create_booking(member_id, counselor_name, topic, date, time):
    from app import load_data, save_data, session
    sessions = load_data('sessions.json')
    
    new_session = {
        "session_id": len(sessions) + 1,
        "member_id": member_id,
        "member_name": session['username'], # Mengambil nama remaja yang login
        "counselor_name": counselor_name,    # Mengambil nama konselor dari form
        "topic": topic,
        "date": date,
        "time": time,
        "status": "pending"
    }
    
    sessions.append(new_session)
    save_data('sessions.json', sessions)

def get_user_sessions(user_id, role):
    """
    Business Logic: Mengambil sesi berdasarkan role pengguna.
    """
    all_sessions = load_sessions()
    if role == 'admin':
        return all_sessions
    elif role == 'konselor':
        return [s for s in all_sessions if s['counselor_id'] == user_id]
    else: # anggota_remaja
        return [s for s in all_sessions if s['member_id'] == user_id]

def update_session_status(session_id, new_status):
    """
    Business Logic: Mengubah status sesi (misal: 'completed' atau 'canceled').
    """
    sessions = load_sessions()
    for s in sessions:
        if s['session_id'] == int(session_id):
            s['status'] = new_status
            save_sessions(sessions)
            return True
    return False