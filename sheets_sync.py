import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SheetsSync")

# Load environment variables
load_dotenv()

# We only import gspread if it is needed, inside functions, to avoid import errors if the library is not installed
gspread = None
credentials = None

def get_gspread_client():
    global gspread
    if gspread is None:
        try:
            import gspread as gs
            from google.oauth2.service_account import Credentials
            gspread = gs
        except ImportError:
            logger.warning("⚠️  Library 'gspread' atau 'google-auth' tidak terinstall. Sinkronisasi Google Sheets dilewati.")
            return None

    creds_path = os.environ.get('GOOGLE_CREDS_PATH', 'credentials.json')
    if not os.path.exists(creds_path):
        logger.warning(f"⚠️  File kredensial Google '{creds_path}' tidak ditemukan. Sinkronisasi Google Sheets dilewati.")
        return None

    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"❌ Gagal mengautentikasi Google Sheets: {e}")
        return None

def sync_table_to_sheets(table_name, rows_dict):
    """
    Menyelaraskan data tabel ke Google Sheets.
    rows_dict: list of dictionaries, contoh: [{'id': 1, 'username': 'admin'}, ...]
    """
    client = get_gspread_client()
    if not client:
        return False

    spreadsheet_name = os.environ.get('GOOGLE_SHEET_NAME', 'PIK-R Database')
    spreadsheet_id = os.environ.get('GOOGLE_SHEET_ID', '')
    
    try:
        # Buka spreadsheet menggunakan ID (lebih andal) atau nama
        try:
            if spreadsheet_id:
                sh = client.open_by_key(spreadsheet_id)
                logger.info(f"✅ Spreadsheet ditemukan menggunakan ID: {spreadsheet_id}")
            else:
                sh = client.open(spreadsheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            logger.info(f"✨ Membuat spreadsheet baru: '{spreadsheet_name}'")
            sh = client.create(spreadsheet_name)
            # Share spreadsheet dengan email service account atau user tertentu jika dikonfigurasi
            share_email = os.environ.get('SHARE_GOOGLE_SHEET_WITH')
            if share_email:
                sh.share(share_email, perm_type='user', role='writer')
                logger.info(f"🔗 Berbagi akses spreadsheet ke: {share_email}")

        # Buka atau buat worksheet/tab untuk tabel ini
        try:
            ws = sh.worksheet(table_name)
        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"📁 Membuat tab baru '{table_name}' di Google Sheets")
            # Cek jika worksheet pertama masih default ("Sheet1") dan kosong, ganti namanya saja
            worksheets = sh.worksheets()
            if len(worksheets) == 1 and worksheets[0].title == "Sheet1":
                ws = worksheets[0]
                ws.update_title(table_name)
            else:
                ws = sh.add_worksheet(title=table_name, rows="100", cols="20")

        # Jika data kosong, cukup bersihkan sheet dan tulis header jika ada
        if not rows_dict:
            ws.clear()
            logger.info(f"✅ Google Sheets: Tab '{table_name}' dibersihkan (data kosong).")
            return True

        # Urutkan kolom & siapkan data untuk ditulis
        headers = list(rows_dict[0].keys())
        values = [headers]
        for row in rows_dict:
            row_values = []
            for col in headers:
                val = row.get(col)
                # Ubah non-string/non-number ke string agar gspread bisa memprosesnya
                if val is None:
                    row_values.append("")
                elif isinstance(val, (dict, list)):
                    row_values.append(str(val))
                else:
                    row_values.append(val)
            values.append(row_values)

        # Bersihkan & Update seluruh isi sheet
        ws.clear()
        
        # Gunakan update() gspread untuk mengupload baris data
        ws.update(values)
        logger.info(f"✅ Google Sheets: Berhasil menyelaraskan {len(rows_dict)} baris ke tab '{table_name}'.")
        return True

    except Exception as e:
        logger.error(f"❌ Gagal menyelaraskan tabel '{table_name}' ke Google Sheets: {e}")
        return False
