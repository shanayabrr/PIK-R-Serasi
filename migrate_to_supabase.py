import os
import sqlite3
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

SQLITE_DB = 'database/pikr.db'

# Define table creation SQL queries in PostgreSQL syntax
SCHEMA_POSTGRES = {
    'users': """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            birth_date TEXT,
            role TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            bio TEXT,
            profile_pic TEXT
        );
    """,
    'sessions': """
        CREATE TABLE IF NOT EXISTS sessions (
            id SERIAL PRIMARY KEY,
            member_name TEXT NOT NULL,
            counselor_name TEXT NOT NULL,
            topic TEXT,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'PENDING',
            priority TEXT,
            reminder_sent INTEGER DEFAULT 0
        );
    """,
    'forum_posts': """
        CREATE TABLE IF NOT EXISTS forum_posts (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            role TEXT,
            is_announcement INTEGER DEFAULT 0,
            date TEXT
        );
    """,
    'education': """
        CREATE TABLE IF NOT EXISTS education (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            author TEXT,
            author_id INTEGER,
            dokumen TEXT
        );
    """,
    'education_comments': """
        CREATE TABLE IF NOT EXISTS education_comments (
            id SERIAL PRIMARY KEY,
            article_id INTEGER NOT NULL REFERENCES education(id) ON DELETE CASCADE,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            rating INTEGER
        );
    """,
    'messages': """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT,
            attachment TEXT,
            timestamp TEXT,
            seen INTEGER DEFAULT 0,
            is_bot INTEGER DEFAULT 0
        );
    """,
    'notifications': """
        CREATE TABLE IF NOT EXISTS notifications (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            link TEXT,
            is_read INTEGER DEFAULT 0,
            timestamp TEXT
        );
    """,
    'events': """
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT,
            time TEXT,
            author TEXT
        );
    """,
    'event_participants': """
        CREATE TABLE IF NOT EXISTS event_participants (
            event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
            username TEXT NOT NULL,
            PRIMARY KEY (event_id, username)
        );
    """,
    'about_history': """
        CREATE TABLE IF NOT EXISTS about_history (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    """,
    'about_officers': """
        CREATE TABLE IF NOT EXISTS about_officers (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            photo TEXT NOT NULL,
            caption TEXT NOT NULL
        );
    """,
    'achievements': """
        CREATE TABLE IF NOT EXISTS achievements (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            author TEXT,
            author_id INTEGER,
            dokumen TEXT,
            date TEXT
        );
    """,
    'achievements_comments': """
        CREATE TABLE IF NOT EXISTS achievements_comments (
            id SERIAL PRIMARY KEY,
            achievement_id INTEGER NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            rating INTEGER
        );
    """,
    'innovations': """
        CREATE TABLE IF NOT EXISTS innovations (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            author TEXT,
            author_id INTEGER,
            dokumen TEXT,
            date TEXT
        );
    """,
    'innovations_comments': """
        CREATE TABLE IF NOT EXISTS innovations_comments (
            id SERIAL PRIMARY KEY,
            innovation_id INTEGER NOT NULL REFERENCES innovations(id) ON DELETE CASCADE,
            username TEXT NOT NULL,
            text TEXT NOT NULL,
            rating INTEGER
        );
    """,
    'about_stakeholders': """
        CREATE TABLE IF NOT EXISTS about_stakeholders (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            role_title TEXT NOT NULL,
            role_desc TEXT,
            category TEXT,
            icon_type TEXT,
            logo TEXT
        );
    """
}

# The migration order is critical to avoid violating foreign key constraints
MIGRATION_ORDER = [
    'users',
    'sessions',
    'forum_posts',
    'education',
    'messages',
    'notifications',
    'events',
    'about_history',
    'about_officers',
    'achievements',
    'about_stakeholders',
    'innovations',
    'education_comments',
    'event_participants',
    'achievements_comments',
    'innovations_comments'
]

def migrate():
    supabase_url = os.environ.get('SUPABASE_DB_URL')
    if not supabase_url:
        print("[Error] SUPABASE_DB_URL tidak ditemukan di environment variable atau file .env")
        print("Silakan tambahkan SUPABASE_DB_URL=postgresql://... ke file .env terlebih dahulu.")
        return

    print("Menyambungkan ke database...")
    try:
        conn_lite = sqlite3.connect(SQLITE_DB)
        conn_lite.row_factory = sqlite3.Row
        cursor_lite = conn_lite.cursor()
    except Exception as e:
        print(f"[Error] Gagal menyambungkan ke SQLite: {e}")
        return

    try:
        conn_pg = psycopg2.connect(supabase_url)
        cursor_pg = conn_pg.cursor()
    except Exception as e:
        print(f"[Error] Gagal menyambungkan ke Supabase (PostgreSQL): {e}")
        conn_lite.close()
        return

    print("Koneksi database berhasil!")
    
    try:
        # Step 1: Create Tables
        print("\nMembuat tabel di Supabase...")
        for table_name in MIGRATION_ORDER:
            create_sql = SCHEMA_POSTGRES[table_name]
            cursor_pg.execute(create_sql)
        conn_pg.commit()
        print("Semua tabel berhasil dibuat/diverifikasi.")

        # Step 2: Copy Data Table by Table
        print("\nMenyalin data...")
        for table_name in MIGRATION_ORDER:
            # Check row count in SQLite
            cursor_lite.execute(f"SELECT COUNT(*) as c FROM {table_name}")
            row_count = cursor_lite.fetchone()['c']
            if row_count == 0:
                print(f"Tabel '{table_name}' kosong di SQLite. Dilewati.")
                continue

            print(f"Memindahkan {row_count} baris dari tabel '{table_name}'...")
            
            # Fetch all columns & data
            cursor_lite.execute(f"SELECT * FROM {table_name}")
            rows = cursor_lite.fetchall()
            
            # Get columns dynamically
            columns = rows[0].keys()
            
            # Clear target table in PostgreSQL (only if migrating fresh)
            # cursor_pg.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
            
            # Prepare Postgres INSERT query
            cols_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
            
            # Insert values
            values = [tuple(row) for row in rows]
            cursor_pg.executemany(insert_query, values)
            
            # Reset sequence for autoincrement ID columns in PostgreSQL
            # (only if the table has an auto-increment serial 'id' column)
            if 'id' in columns:
                seq_query = f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), COALESCE(max(id), 1)) FROM {table_name};"
                cursor_pg.execute(seq_query)
                
            conn_pg.commit()
            print(f"Tabel '{table_name}' berhasil dipindahkan.")
            
        print("\nMigrasi database SQLite ke Supabase selesai dengan sukses!")
        
    except Exception as e:
        conn_pg.rollback()
        print(f"\n[Error] Terjadi kesalahan saat migrasi: {e}")
    finally:
        conn_lite.close()
        conn_pg.close()
        print("Koneksi database ditutup.")

if __name__ == '__main__':
    migrate()
