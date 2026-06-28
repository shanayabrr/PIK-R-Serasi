import json
import os
from datetime import datetime

DB_CHAT = 'database/chats.json'

def load_chats():
    if not os.path.exists(DB_CHAT): return []
    with open(DB_CHAT, 'r') as f:
        try: return json.load(f)
        except: return []

def save_chats(chats):
    with open(DB_CHAT, 'w') as f:
        json.dump(chats, f, indent=4)

def send_message(sender_user, receiver_user, message):
    from app import load_data, save_data
    chats = load_data('chats.json')
    new_chat = {
        "sender": sender_user,      # Pastikan tulisannya 'sender'
        "receiver": receiver_user,  # Pastikan tulisannya 'receiver'
        "message": message,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    chats.append(new_chat)
    save_data('chats.json', chats)
    
def get_chat_history(user_me, user_them):
    from app import load_data
    chats = load_data('chats.json')
    
    history = []
    for c in chats:
        # Gunakan .get() agar jika 'sender' tidak ada, aplikasi tidak error/crash
        s = c.get('sender')
        r = c.get('receiver')
        
        if (s == user_me and r == user_them) or (s == user_them and r == user_me):
            history.append(c)
            
    return history