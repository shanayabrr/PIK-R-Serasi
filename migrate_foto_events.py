import os
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.environ.get('SUPABASE_DB_URL')

if not supabase_url:
    print("SUPABASE_DB_URL tidak ditemukan di .env - menggunakan SQLite saja")
else:
    import psycopg2
    print("Connecting to Supabase...")
    conn = psycopg2.connect(supabase_url)
    cur = conn.cursor()

    # Check if column already exists
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'events' AND column_name = 'foto'
    """)
    exists = cur.fetchone()

    if exists:
        print("OK - Kolom 'foto' sudah ada di tabel events Supabase.")
    else:
        cur.execute("ALTER TABLE events ADD COLUMN foto TEXT")
        conn.commit()
        print("SUKSES - Kolom 'foto' berhasil ditambahkan ke tabel events di Supabase!")

    # Verify
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'events' 
        ORDER BY ordinal_position
    """)
    cols = cur.fetchall()
    print("\nStruktur tabel events sekarang:")
    for col in cols:
        print("  - %s: %s" % (col[0], col[1]))

    cur.close()
    conn.close()
    print("\nMigrasi selesai!")
