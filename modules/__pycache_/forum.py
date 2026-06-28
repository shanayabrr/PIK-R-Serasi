import json
import os
from datetime import datetime

DB_FORUM = 'database/forum.json'

def load_posts():
    if not os.path.exists(DB_FORUM): return []
    with open(DB_FORUM, 'r') as f: return json.load(f)

def save_posts(posts):
    with open(DB_FORUM, 'w') as f: json.dump(posts, f, indent=4)

def add_post(author, content, role):
    posts = load_posts()
    new_post = {
        "id": len(posts) + 1,
        "author": author,
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
        "comments": []
    }
    posts.insert(0, new_post) # Postingan terbaru di atas
    save_posts(posts)

def add_comment(post_id, author, comment):
    posts = load_posts()
    for p in posts:
        if p['id'] == int(post_id):
            p['comments'].append({
                "author": author,
                "text": comment,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            break
    save_posts(posts)