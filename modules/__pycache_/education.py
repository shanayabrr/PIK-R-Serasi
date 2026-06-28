import json
import os
from datetime import datetime

DB_EDUCATION = 'database/education.json'

def load_articles():
    """Data Access Layer: Mengambil semua artikel dari file JSON."""
    if not os.path.exists(DB_EDUCATION):
        return []
    with open(DB_EDUCATION, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_articles(articles):
    """Data Access Layer: Menyimpan artikel ke file JSON."""
    with open(DB_EDUCATION, 'w') as f:
        json.dump(articles, f, indent=4)

def get_article_by_id(article_id):
    """Business Logic: Mencari satu artikel spesifik berdasarkan ID."""
    articles = load_articles()
    return next((a for a in articles if a['id'] == int(article_id)), None)

def add_article(title, content, author, category):
    """
    Business Logic: Menambah artikel baru.
    Fungsi ini biasanya digunakan oleh Admin atau Konselor.
    """
    articles = load_articles()
    new_article = {
        "id": len(articles) + 1,
        "title": title,
        "content": content,
        "author": author,
        "category": category, # Contoh: Kesehatan Mental, Reproduksi, Sosial
        "date_published": datetime.now().strftime("%Y-%m-%d")
    }
    articles.append(new_article)
    save_articles(articles)
    return True

def search_articles(query):
    """Business Logic: Mencari artikel berdasarkan kata kunci pada judul."""
    articles = load_articles()
    return [a for a in articles if query.lower() in a['title'].lower()]