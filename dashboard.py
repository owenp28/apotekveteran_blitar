import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import io
import re
from datetime import date, datetime
import os
from io import BytesIO
from urllib.request import Request, urlopen
from openpyxl import load_workbook, Workbook

st.set_page_config(page_title="Apotek Veteran Blitar", layout="wide", page_icon="💊")

# ── CSS Custom untuk Menyesuaikan Tampilan ERP ─────────────────────────────────
st.markdown(
    """
    <style>
    /* Reset default margin dan padding */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    /* Dark Mode Background */
    body { background: #1a1a2e; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #e0e0e0; }
    
    /* Mengurangi padding di bagian atas sidebar */
    [data-testid="stSidebar"] > div:first-child { padding-top: 2rem !important; }
    
    /* Mengurangi margin di bagian atas konten utama */
    .block-container { padding-top: 3rem !important; padding-bottom: 2rem !important; margin-top: 0rem !important; padding-left: 20px !important; padding-right: 20px !important; }
    
    /* ── Header Aplikasi ────────────────────────────────────────────────────── */
    .app-header { text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #16213e 0%, #0f3460 100%); border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .app-title { font-size: 42px; font-weight: 700; color: #e94560; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .app-subtitle { font-size: 16px; color: #a0a0a0; font-weight: 400; }
    
    /* ── Form Container ─────────────────────────────────────────────────────── */
    .form-container { background: #16213e; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #0f3460; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .form-section-title { font-size: 18px; font-weight: 600; color: #e94560; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #e94560; display: flex; align-items: center; gap: 10px; }
    
    /* ── Grid Layout ────────────────────────────────────────────────────────── */
    .form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
    .form-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }
    .form-group { display: flex; flex-direction: column; gap: 8px; }
    .form-label { font-size: 14px; font-weight: 500; color: #a0a0a0; }
    .form-input { width: 100%; padding: 10px 14px; border: 1px solid #0f3460; border-radius: 6px; background: #1a1a2e; color: #e0e0e0; font-size: 14px; transition: all 0.3s ease; }
    .form-input:focus { outline: none; border-color: #e94560; box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2); }
    .form-input:disabled { background: #16213e; color: #666; cursor: not-allowed; font-weight: 600; }
    
    /* ── Tombol Custom ──────────────────────────────────────────────────────── */
    .btn-custom { padding: 12px 24px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 8px; border: none; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .btn-cari { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; }
    .btn-cari:hover { background: linear-gradient(135deg, #ee5a24 0%, #d64520 100%); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(238, 90, 36, 0.4); }
    .btn-save { background: linear-gradient(135deg, #28a745 0%, #218838 100%); color: white; }
    .btn-save:hover { background: linear-gradient(135deg, #218838 0%, #1e7e34 100%); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4); }
    .btn-reset { background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%); color: white; }
    .btn-reset:hover { background: linear-gradient(135deg, #5a6268 0%, #4e555b 100%); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(108, 117, 125, 0.4); }
    
    /* ── Total Nominal Container ────────────────────────────────────────────── */
    .total-container { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: linear-gradient(135deg, #16213e 0%, #0f3460 100%); border-radius: 12px; margin: 20px 0; border: 1px solid #0f3460; }
    .total-label { font-size: 16px; color: #a0a0a0; font-weight: 500; }
    .total-value { font-size: 42px; font-weight: 700; color: #e94560; text-align: right; font-family: 'Courier New', monospace; }
    
    /* ── Tabel Data Editor ──────────────────────────────────────────────────── */
    .table-container { background: #16213e; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #0f3460; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .table-title { font-size: 18px; font-weight: 600; color: #e94560; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #e94560; }
    .stDataFrame { background: #1a1a2e; border-radius: 8px; overflow: hidden; }
    .stDataFrame th { background: #0f3460; color: #e0e0e0; font-weight: 600; font-size: 13px; padding: 10px; }
    .stDataFrame td { color: #e0e0e0; font-size: 13px; padding: 8px; }
    .stDataFrame tr:hover { background: #1f3a5e; }
    
    /* ── Info Box ───────────────────────────────────────────────────────────── */
    .info-box { background: #1f3a5e; border-left: 4px solid #e94560; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 15px; }
    .info-box strong { color: #e94560; }
    
    /* ── Footer ─────────────────────────────────────────────────────────────── */
    .app-footer { text-align: center; padding: 20px; color: #666; font-size: 14px; margin-top: 30px; }
    .action-buttons { display: flex; gap: 15px; margin-top: 20px; }
    
    /* ── Responsive ─────────────────────────────────────────────────────────── */
    @media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } .form-grid-4 { grid-template-columns: 1fr; } .total-container { flex-direction: column; gap: 15px; } .total-value { text-align: center; } }
    </style>
    """,
    unsafe_allow_html=True
)
# ─────────────────────────────────────────────────────────────────────────────

DATASET_PATH = os.path.join(os.path.dirname(__file__), "stok_obat.csv")
RETUR_HISTORY_PATH = os.path.join(os.path.dirname(__file__), "retur_history.csv")
WORKBOOK_PATH = os.path.join(os.path.dirname(__file__), "DatasetObat_ApotekVeteran_4.xlsx")
SHIFT_LOG_PATH = os.path.join(os.path.dirname(__file__), "shift_log.csv")
DEFAULT_LINK_ONEDRIVE = "https://1drv.ms/x/c/2b91c5c1ac3eaa9f/IQBzkm7nxPNlRI4V4fKaVYERASx-hzJiaBEWDdCFPu79k3w?e=V5jQMP"
DEFAULT_SOURCE_URL = WORKBOOK_PATH
DEFAULT_SOURCE_LABEL = WORKBOOK_PATH

INVENTORY_SHEETS = ["PCS", "SACHET", "BOTOL", "TAB", "BOX", "STRIP"]
INVENTORY_COLUMNS = [
    "Nama produk", "Satuan", "Tanggal", "Nomor Faktur", "Nomor Batch", 
    "PBF", "Tanggal Kadaluwarsa", "Stok Masuk", "Stok Keluar", "Stok Sisa", 
    "Harga 1", "Harga 2", "Keterangan"
]

KOLOM_DATABASE_OBAT = [
    "id_obat", "nama_obat", "kategori", "satuan", "isi_per_strip", 
    "isi_per_box", "harga_beli", "harga_1", "harga_2", "harga_3",
    "stok_akhir", "tanggal_kadaluarsa"
]

KOLOM_WAJIB = [
    "Tanggal", "Nama Obat", "Kategori", "Satuan", "Stok Masuk", "Stok Keluar", 
    "Stok Akhir", "Harga Satuan (Rp)", "Total Nilai (Rp)", "Tanggal Kadaluarsa", "Keterangan"
]

RETUR_HISTORY_COLUMNS = ["Nomor Faktur", "Tanggal Retur", "Jumlah Item", "Total Nilai Retur", "Tanggal Disimpan"]

def load_data():
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH, parse_dates=["Tanggal", "Tanggal Kadaluarsa"])
        for kolom_lama in df.columns.tolist():
            if kolom_lama not in KOLOM_WAJIB:
                df = df.drop(columns=[kolom_lama])
        for kolom in KOLOM_WAJIB:
            if kolom not in df.columns:
                df[kolom] = None
        return df[KOLOM_WAJIB]
    return None

def load_retur_history():
    if os.path.exists(RETUR_HISTORY_PATH):
        df = pd.read_csv(RETUR_HISTORY_PATH, parse_dates=["Tanggal Retur", "Tanggal Disimpan"])
        for kolom_lama in df.columns.tolist():
            if kolom_lama not in RETUR_HISTORY_COLUMNS:
                df = df.drop(columns=[kolom_lama])
        for kolom in RETUR_HISTORY_COLUMNS:
            if kolom not in df.columns:
                df[kolom] = None
        return df[RETUR_HISTORY_COLUMNS]
    return None

def load_shift_log():
    if os.path.exists(SHIFT_LOG_PATH):
        return pd.read_csv(SHIFT_LOG_PATH)
    else:
        return pd.DataFrame(columns=[
            "Waktu Buka", "Waktu Tutup", "Shift", "Nama Kasir", "Saldo Awal", 
            "Hasil Penjualan", "Piutang", "Pendapatan Jurnal", "Total Pendapatan",
            "Retur Penjualan", "Pengeluaran Jurnal", "Total Pengeluaran",
            "Saldo Akhir", "Fisik Kasir", "Selisih", "Diserahkan Ke", "Nama Penyerah", "Catatan"
        ])

def save_data(df):
    df.to_csv(DATASET_PATH, index=False)

def save_retur_history(df):
    df.to_csv(RETUR_HISTORY_PATH, index=False)

def save_shift_log(df):
    df.to_csv(SHIFT_LOG_PATH, index=False)

def format_rupiah(val):
    try:
        return f"Rp {int(val):,}".replace(",", ".")
    except:
        return val


def parse_excel_date(val):
    if pd.isna(val):
        return pd.NaT
    val_str = str(val).strip()
    if val_str in ["", "-", "nan", "None", "NaT", "0", "0.0"]:
        return pd.NaT
    
    if isinstance(val, (datetime, date)):
        d = val.date() if isinstance(val, datetime) else val
        return pd.Timestamp(d) if d.year > 1970 else pd.NaT
        
    try:
        f_val = float(val)
        if f_val > 10000:
            d = (pd.Timestamp('1899-12-30') + pd.Timedelta(days=f_val)).date()
            return pd.Timestamp(d) if d.year > 1970 else pd.NaT
        return pd.NaT
    except Exception:
        pass
        
    try:
        d = pd.to_datetime(val)
        return pd.Timestamp(d) if d.year > 1970 else pd.NaT
    except Exception:
        return pd.NaT


def normalize_inventory_df(df):
    df = df.copy()
    renamed = {}
    for kolom in df.columns:
        nama_kolom = str(kolom).strip()
        if nama_kolom.lower() == "nama obat":
            renamed[kolom] = "Nama produk"
        elif nama_kolom.lower() == "nama produk":
            renamed[kolom] = "Nama produk"
        elif nama_kolom.lower() == "pbf ":
            renamed[kolom] = "PBF"
        elif nama_kolom.lower() == "keterangan ":
            renamed[kolom] = "Keterangan"
    if renamed:
        df = df.rename(columns=renamed)
        
    for kolom in INVENTORY_COLUMNS:
        if kolom not in df.columns:
            df[kolom] = None
    df = df[INVENTORY_COLUMNS]

    text_like_columns = ["Nama produk", "Satuan", "Nomor Faktur", "Nomor Batch", "PBF", "Keterangan"]
    for kolom in text_like_columns:
        if kolom in df.columns:
            df[kolom] = df[kolom].astype("string")

    numeric_columns = ["Stok Masuk", "Stok Keluar", "Stok Sisa", "Harga 1", "Harga 2"]
    for kolom in numeric_columns:
        if kolom in df.columns:
            df[kolom] = pd.to_numeric(df[kolom], errors="coerce")

    for col in ["Tanggal", "Tanggal Kadaluwarsa"]:
        if col in df.columns:
            df[col] = df[col].apply(parse_excel_date)

    return df


def prepare_sheet_for_editor(df):
    df = normalize_inventory_df(df)
    for kolom in ["Nomor Faktur", "Nomor Batch", "PBF", "Keterangan", "Nama produk", "Satuan"]:
        if kolom in df.columns:
            df[kolom] = df[kolom].astype("string")
            
    return df


def _find_inventory_header_row(rows):
    known_headers = {
        "nama produk", "nama obat", "satuan", "tanggal", "nomor faktur", "nomor batch",
        "pbf", "tanggal kadaluarsa", "stok masuk", "stok keluar", "stok sisa", 
        "harga 1", "harga 2", "keterangan"
    }
    for index, row in enumerate(rows):
        cleaned = [str(cell).strip().lower() if cell is not None else "" for cell in row]
        score = sum(1 for cell in cleaned if cell in known_headers)
        if score >= 4:
            return index, list(row)
    return 0, list(rows[0]) if rows else []


def load_inventory_sheet_dataframe(ws):
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return pd.DataFrame(columns=INVENTORY_COLUMNS)

    header_index, raw_header = _find_inventory_header_row(rows)
    header = [str(cell).strip() if cell is not None else "" for cell in raw_header]
    data_rows = rows[header_index + 1:]
    if not data_rows:
        return pd.DataFrame(columns=INVENTORY_COLUMNS)

    data_rows = [tuple(row[:len(header)]) for row in data_rows]
    df = pd.DataFrame(data_rows, columns=header)
    return normalize_inventory_df(df)


def create_default_inventory_workbook():
    wb = Workbook()
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
    for sheet_name in INVENTORY_SHEETS:
        ws = wb.create_sheet(title=sheet_name)
        ws.append(INVENTORY_COLUMNS)
    wb.save(WORKBOOK_PATH)


def normalize_source_url(source_url):
    source_url = (source_url or DEFAULT_SOURCE_URL).strip()
    if "1drv.ms" in source_url or "onedrive.live.com" in source_url or "sharepoint.com" in source_url:
        if "?" in source_url:
            return source_url.split("?")[0] + "?download=1"
        return source_url + "?download=1"
    
    if "drive.google.com" in source_url and "/d/" in source_url:
        try:
            file_id = source_url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except:
            pass
            
    if "download.aspx?UniqueId=" in source_url:
        return source_url
    if source_url.endswith(".csv") or source_url.endswith(".xlsx") or source_url.endswith(".xlsm"):
        return source_url
    return source_url


def sync_inventory_from_source(source_url=None):
    source_url = normalize_source_url(source_url)
    if not source_url or not source_url.startswith("http"):
        return False

    try:
        request = Request(
            source_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        with urlopen(request, timeout=45) as response:
            data = response.read()

        if not data or len(data) < 100:
            st.error("⚠️ File download dari link sumber kosong.")
            return False

        is_csv = source_url.lower().split("?")[0].endswith(".csv")
        if not is_csv and not data.startswith(b"PK"):
            st.error("⚠️ OneDrive memblokir download otomatis untuk link ini. Silakan gunakan fitur **Upload file Excel/CSV** di bawah.")
            return False

        with open(WORKBOOK_PATH, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        st.error(f"⚠️ Link tidak valid atau tidak bisa diakses otomatis. Gunakan menu Upload File.")
        return False


def load_inventory_from_bytes(file_bytes, filename):
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(BytesIO(file_bytes))
        return {"Sheet1": normalize_inventory_df(df)}

    wb = load_workbook(BytesIO(file_bytes), data_only=True)
    workbook_data = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        workbook_data[sheet_name] = load_inventory_sheet_dataframe(ws)
    return workbook_data


def load_inventory_workbook(source_url=None, uploaded_file=None):
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        loaded = load_inventory_from_bytes(data, uploaded_file.name)
        if loaded:
            return loaded

    if source_url and source_url != DEFAULT_SOURCE_URL and source_url.startswith("http"):
        sync_inventory_from_source(source_url)

    if os.path.exists(WORKBOOK_PATH):
        try:
            wb = load_workbook(WORKBOOK_PATH, data_only=True)
            workbook_data = {}
            for sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                workbook_data[sheet_name] = load_inventory_sheet_dataframe(ws)
            wb.close()
            return workbook_data
        except Exception:
            return {}

    return {}


def sanitize_excel_value(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple, dict, set)):
        return str(value)
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    if isinstance(value, pd.Timedelta):
        return str(value)
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if isinstance(value, (datetime, date)):
        return value
    if isinstance(value, (bool, int, float, str)):
        return value
    return str(value)


def sanitize_excel_dataframe(df):
    df = df.copy()
    for kolom in df.columns:
        df[kolom] = df[kolom].apply(lambda v: sanitize_excel_value(v))
    return df


def save_inventory_workbook(workbook_data):
    try:
        with pd.ExcelWriter(WORKBOOK_PATH, engine='openpyxl') as writer:
            for sheet_name, df_sheet in workbook_data.items():
                if df_sheet is None or df_sheet.empty:
                    df_sheet = pd.DataFrame(columns=INVENTORY_COLUMNS)
                
                df_sheet = sanitize_excel_dataframe(df_sheet)
                df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan ke file Excel. Pastikan file tidak sedang dibuka di aplikasi lain. Error: {e}")
        return False


def build_inventory_print_dataframe():
    workbook_data = st.session_state.get("inventory_data_cache")
    if not workbook_data:
        source_url = st.session_state.get("inventory_source_url", DEFAULT_SOURCE_LABEL)
        workbook_data = load_inventory_workbook(source_url)
        st.session_state.inventory_data_cache = workbook_data

    if not workbook_data:
        return None

    frames = []
    for sheet_name, df_sheet in workbook_data.items():
        df_sheet = prepare_sheet_for_editor(df_sheet.copy())
        df_sheet["Worksheet"] = sheet_name
        frames.append(df_sheet)

    if not frames:
        return pd.DataFrame(columns=INVENTORY_COLUMNS + ["Worksheet"])

    combined_df = pd.concat(frames, ignore_index=True)
    
    worksheet_series = combined_df["Worksheet"].copy()
    combined_df = normalize_inventory_df(combined_df)
    combined_df["Worksheet"] = worksheet_series
    
    return combined_df


def build_rtf_export(df, title="Laporan Stok Obat — Apotek Veteran Blitar"):
    lines = ["{\\rtf1\\ansi\\deff0", "{\\fonttbl\\f0\\fswiss Arial;}", "\\viewkind4\\uc1"]
    lines.append(f"\\pard\\plain\\f0\\fs20 {title}\\par")
    lines.append("\\pard\\plain\\f0\\fs18\\b " + "\\tab".join(str(col) for col in df.columns) + "\\par")
    for _, row in df.iterrows():
        row_text = "\\tab".join(str(v) if pd.notna(v) else "" for v in row.tolist())
        lines.append("\\pard\\plain\\f0\\fs18 " + row_text + "\\par")
    lines.append("}")
    return "".join(lines).encode("utf-8")


def parse_rupiah(val):
    try:
        if pd.isna(val):
            return 0
        teks = str(val).replace("Rp", "").replace(".", "").replace(",", "").strip()
        return int(float(teks)) if teks else 0
    except:
        return 0

def get_available_sheets():
    cache = st.session_state.get("inventory_data_cache", {})
    if cache:
        return list(cache.keys())
    return INVENTORY_SHEETS


# ══════════════════════════════════════════════════════════════════════════════
# AUTENTIKASI — LOGIN & USER MAPPING
# ══════════════════════════════════════════════════════════════════════════════
USERS = {
    "iponadmcantik@gmail.com": {"password": "IponAdmCantik!", "role": "Admin", "name": "Ivonne"},
    "karyawan1@gmail.com": {"password": "karyawan1", "role": "Kasir", "name": "Dian"},
    "karyawan2@gmail.com": {"password": "karyawan2", "role": "Kasir", "name": "Julia"}
}

if "logged_in" not in st.session_state:
    # Pengecekan Query Params untuk mempertahankan sesi saat refresh
    if st.query_params.get("logged_in") == "true":
        st.session_state.logged_in = True
        st.session_state.role = st.query_params.get("role")
        st.session_state.username = st.query_params.get("username")
    else:
        st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = st.query_params.get("role", None)
if "username" not in st.session_state:
    st.session_state.username = st.query_params.get("username", "")

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align:center; padding: 25px 20px 10px 20px; background-color: #16213e; 
                        border-radius: 12px 12px 0 0; border: 1px solid #0f3460; border-bottom: none;'>
                <img src='https://img.icons8.com/color/96/pharmacy-shop.png' width='72'/>
                <h2 style='color: #e94560; margin-top: 10px; margin-bottom: 5px;'>Apotek Veteran Blitar</h2>
                <p style='color: #a0a0a0; font-size: 14px; margin-bottom: 0;'>Silakan login untuk melanjutkan</p>
            </div>
            """, unsafe_allow_html=True
        )
        with st.form("form_login"):
            role_pilih = st.selectbox("Login sebagai", ["Admin", "Kasir"])
            username   = st.text_input("Username")
            password   = st.text_input("Password", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            login_btn  = st.form_submit_button("🔐 Login", use_container_width=True)

            if login_btn:
                uname = username.strip()
                if uname in USERS and USERS[uname]["password"] == password and USERS[uname]["role"] == role_pilih:
                    st.session_state.logged_in = True
                    st.session_state.role      = role_pilih
                    st.session_state.username  = uname
                    
                    # Set query params agar tidak ter-logout saat direfresh
                    st.query_params["logged_in"] = "true"
                    st.query_params["role"] = role_pilih
                    st.query_params["username"] = uname
                    
                    st.session_state.target_menu = "🏠 Dashboard" 
                    st.rerun()
                else:
                    st.error("❌ Username, password, atau role tidak sesuai.")
    st.stop()

# ── Session State (General & Shift) ───────────────────────────────────────────
if "inventory_source_url" not in st.session_state:
    st.session_state.inventory_source_url = DEFAULT_LINK_ONEDRIVE
if "retur_form_data" not in st.session_state:
    st.session_state.retur_form_data = {}
if "retur_items" not in st.session_state:
    st.session_state.retur_items = pd.DataFrame(columns=[
        "Nama produk", "Satuan", "Nomor Batch", "Tanggal Kadaluwarsa", 
        "Stok Sisa", "Jumlah Retur", "Harga 1", "Keterangan"
    ])
if "retur_history" not in st.session_state:
    st.session_state.retur_history = load_retur_history()
    if st.session_state.retur_history is None:
        st.session_state.retur_history = pd.DataFrame(columns=RETUR_HISTORY_COLUMNS)
if "cari_faktur" not in st.session_state:
    st.session_state.cari_faktur = False
if "hasil_pencarian" not in st.session_state:
    st.session_state.hasil_pencarian = pd.DataFrame()
if "item_pembelian" not in st.session_state:
    st.session_state.item_pembelian = pd.DataFrame()
if "selected_obat" not in st.session_state:
    st.session_state.selected_obat = None
if "obat_baru" not in st.session_state:
    st.session_state.obat_baru = False

# SHIFT STATE
if "shift_active" not in st.session_state:
    st.session_state.shift_active = False
if "active_shift_context" not in st.session_state:
    st.session_state.active_shift_context = {
        "saldo_awal": 0.0,
        "accumulated_sales_expected": 0.0,
        "start_time": None,
        "user_name": "",
        "shift_name": "Pagi"
    }

if "step_tutup_shift" not in st.session_state:
    st.session_state.step_tutup_shift = 1
if "input_saldo_kasir" not in st.session_state:
    st.session_state.input_saldo_kasir = 0.0
if "last_shift_data" not in st.session_state:
    st.session_state.last_shift_data = pd.DataFrame()

# ── Sidebar navigasi ──────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/pharmacy-shop.png", width=80)
st.sidebar.title("💊 Apotek Veteran Blitar")
st.sidebar.markdown("---")

_role = st.session_state.get("role", "Unknown")
_username = st.session_state.get("username", "")

if _username in USERS:
    _name = USERS[_username]["name"]
else:
    _name = "Pengguna"

st.sidebar.markdown(f"👤 **{_name}** — *{_role}*")
st.sidebar.markdown("---")

if _role == "Admin":
    _menu_options = [
        "🏠 Dashboard",
        "📋 Kelola Stok",
        "🖨️ Rekap Data",
        "📦 Retur & Entry",
        "🛒 Kasir Utama",
        "🕒 Sesi Shift"
    ]
else:  
    _menu_options = [
        "🏠 Dashboard",
        "📋 Kelola Stok",
        "🛒 Kasir Utama",
        "🕒 Sesi Shift"
    ]

# Mencegah routing bug saat reload dengan mekanisme "key"
if "target_menu" in st.session_state:
    target = st.session_state.target_menu
    del st.session_state.target_menu
    if target in _menu_options:
        st.session_state.main_menu = target

if "main_menu" not in st.session_state or st.session_state.main_menu not in _menu_options:
    st.session_state.main_menu = _menu_options[0]

menu = st.sidebar.radio("Pilih Fitur", _menu_options, key="main_menu")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.role      = None
    st.session_state.username  = ""
    st.query_params.clear() # Bersihkan token sesi
    st.session_state.shift_active = False
    st.session_state.active_shift_context = {
        "saldo_awal": 0.0, "accumulated_sales_expected": 0.0, "start_time": None, "user_name": "", "shift_name": "Pagi"
    }
    st.session_state.step_tutup_shift = 1
    st.session_state.input_saldo_kasir = 0.0
    if "main_menu" in st.session_state:
        del st.session_state["main_menu"]
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Dashboard":
    st.title("💊 Dashboard Apotek Veteran Blitar")
    st.markdown("Selamat datang! Pilih fitur di sidebar untuk mulai mengelola stok obat.")
    st.markdown("---")

    if "inventory_data_cache" not in st.session_state or not st.session_state.inventory_data_cache:
        st.session_state.inventory_data_cache = load_inventory_workbook()

    all_items_df = build_inventory_print_dataframe()
    
    if all_items_df is None or all_items_df.empty:
        st.info("Dataset belum tersedia. Silakan upload dataset di menu **📋 Kelola Stok**.")
    else:
        all_items_df["Nama produk"] = all_items_df["Nama produk"].astype(str).str.strip()
        all_items_df = all_items_df[
            (all_items_df["Nama produk"] != "") & 
            (all_items_df["Nama produk"].str.lower() != "nan") &
            (all_items_df["Nama produk"].notna())
        ]
        
        all_items_df["Stok Sisa"] = pd.to_numeric(all_items_df["Stok Sisa"], errors="coerce").fillna(0)
        all_items_df["Harga 1"] = pd.to_numeric(all_items_df["Harga 1"], errors="coerce").fillna(0)
        
        total_jenis = all_items_df["Nama produk"].nunique()
        total_stok = all_items_df["Stok Sisa"].sum()
        
        tgl_batas = pd.Timestamp(date.today()) + pd.Timedelta(days=30)
        exp_soon_df = all_items_df[(pd.to_datetime(all_items_df["Tanggal Kadaluwarsa"], errors='coerce') <= tgl_batas) & (all_items_df["Stok Sisa"] > 0)]
        total_exp_soon = exp_soon_df["Nama produk"].nunique()
        
        nilai_stok = (all_items_df["Stok Sisa"] * all_items_df["Harga 1"]).sum()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Jenis Obat", total_jenis)
        col2.metric("Total Stok Tersedia", f"{int(total_stok):,}".replace(",", "."))
        col3.metric("⚠️ Hampir Kadaluarsa (≤30 hari)", total_exp_soon)
        col4.metric("💰 Estimasi Nilai Stok (Rp)", format_rupiah(nilai_stok))

        st.markdown("---")

        col_low, col_exp = st.columns(2)
        with col_low:
            st.markdown("#### 📉 Stok Menipis (≤ 20)")
            
            cari_low = st.text_input("🔍 Cari (Nama, Batch, PBF, dll)", key="cari_low", placeholder="Cari obat stok menipis...")
            
            stok_df = all_items_df.copy()
            
            if cari_low.strip():
                mask_low = stok_df.astype(str).apply(lambda col: col.str.contains(cari_low.strip(), case=False, na=False)).any(axis=1)
                stok_df = stok_df[mask_low]
                
            stok_df["Worksheet"] = stok_df["Worksheet"].fillna("-")
            
            stok_summary = stok_df.groupby(["Worksheet", "Nama produk"])["Stok Sisa"].sum().reset_index()
            stok_menipis = stok_summary[stok_summary["Stok Sisa"] <= 20].sort_values("Stok Sisa")
            
            if stok_menipis.empty:
                st.success("Tidak ada obat dengan stok menipis atau yang cocok dengan pencarian.")
            else:
                st.dataframe(
                    stok_menipis.rename(columns={"Nama produk": "Nama Obat", "Stok Sisa": "Total Stok"}),
                    use_container_width=True, hide_index=True
                )
                
        with col_exp:
            st.markdown("#### ⏰ Segera Kadaluarsa (≤30 hari)")
            
            cari_exp = st.text_input("🔍 Cari (Nama, Batch, PBF, dll)", key="cari_exp", placeholder="Cari obat segera kadaluarsa...")
            
            exp_df = exp_soon_df.copy()
            
            if cari_exp.strip():
                mask_exp = exp_df.astype(str).apply(lambda col: col.str.contains(cari_exp.strip(), case=False, na=False)).any(axis=1)
                exp_df = exp_df[mask_exp]
                
            if exp_df.empty:
                st.success("Tidak ada obat yang mendekati tanggal kadaluarsa atau yang cocok dengan pencarian.")
            else:
                exp_show = exp_df[["Nama produk", "Worksheet", "Nomor Batch", "Tanggal Kadaluwarsa", "Stok Sisa"]].copy()
                exp_show["Tanggal Kadaluwarsa"] = exp_show["Tanggal Kadaluwarsa"].apply(lambda x: x.strftime("%d-%m-%Y") if pd.notna(x) else "")
                st.dataframe(
                    exp_show.rename(columns={"Nama produk": "Nama Obat", "Tanggal Kadaluwarsa": "Tgl Expired", "Nomor Batch": "Batch"}),
                    use_container_width=True, hide_index=True
                )

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 1 — KELOLA STOK
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📋 Kelola Stok":
    st.title("📋 Kelola Stok")
    
    if st.session_state.role == "Admin":
        st.caption("Pilih tab Edit Stok untuk mengelola data per worksheet, atau tab Stok Opname untuk pencocokan fisik.")
    else:
        st.caption("Tampilan data stok obat secara Read-Only.")

    if "inventory_data_cache" not in st.session_state:
        st.session_state.inventory_data_cache = {}

    tab_edit, tab_opname = st.tabs(["✏️ Edit Stok", "📦 Stok Opname Obat"])

    # ── TAB 1: EDIT STOK ──────────────────────────────────────────────────────
    with tab_edit:
        if st.session_state.role == "Admin":
            col_link, col_btn = st.columns([8, 2])
            with col_link:
                source_url = st.text_input(
                    "Link Dataset",
                    value=st.session_state.inventory_source_url,
                    placeholder="Masukkan tautan OneDrive Anda di sini...",
                    help="Contoh: link OneDrive (https://1drv.ms/x/...), Google Drive, atau URL file Excel/CSV."
                )
            with col_btn:
                st.write("")
                st.write("")
                submit_link = st.button("📥 Submit Link", use_container_width=True)

            if submit_link and source_url.strip():
                with st.spinner("Menganalisis link dan mengunduh dataset..."):
                    st.session_state.inventory_source_url = source_url
                    success = sync_inventory_from_source(source_url)
                    if success:
                        wb_data = load_inventory_workbook()
                        if wb_data:
                            st.session_state.inventory_data_cache = wb_data
                            st.success("✅ Dataset berhasil diunduh dan dimuat!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal memuat data dari file yang diunduh.")

            uploaded_inventory = st.file_uploader(
                "Atau upload file Excel/CSV langsung dari perangkat Anda:",
                type=["xlsx", "xlsm", "csv"],
                key="upload_inventory_source"
            )

            if uploaded_inventory is not None:
                file_id = f"{uploaded_inventory.name}_{uploaded_inventory.size}"
                if st.session_state.get("last_uploaded_file") != file_id:
                    workbook_data = load_inventory_workbook(uploaded_file=uploaded_inventory)
                    if workbook_data:
                        st.session_state.inventory_data_cache = workbook_data
                        save_inventory_workbook(workbook_data)
                        st.session_state["last_uploaded_file"] = file_id
                        st.success("✅ Data berhasil dimuat langsung dari file upload.")
                        st.rerun()

        workbook_data = st.session_state.inventory_data_cache
        if not workbook_data:
            workbook_data = load_inventory_workbook()
            st.session_state.inventory_data_cache = workbook_data

        if not workbook_data:
            st.info("Sumber file belum bisa dibaca, jadi sistem akan membuat struktur default.")

        AVAILABLE_SHEETS = get_available_sheets()
        
        sheet_name = st.selectbox(
            "Pilih Worksheet",
            AVAILABLE_SHEETS,
            index=0,
            key="inventory_selected_sheet"
        )

        if sheet_name not in workbook_data:
            sheet_df = pd.DataFrame(columns=INVENTORY_COLUMNS)
            sheet_df = prepare_sheet_for_editor(sheet_df)
        else:
            sheet_df = prepare_sheet_for_editor(workbook_data[sheet_name].copy())

        if st.session_state.role == "Admin":
            st.info("Setiap kolom dalam tabel dapat diedit langsung dengan ikon ✏️. Anda juga dapat memfilter menggunakan kotak pencarian di bawah.")
        else:
            st.info("Cari data stok di bawah ini. Anda hanya dapat melihat data (Read-Only) untuk menghindari manipulasi.")
            
        search_inv = st.text_input("🔍 Pencarian Baris (Nama, Batch, Faktur, PBF, dll di Worksheet ini)", placeholder="Ketik kata kunci...")
        if search_inv.strip():
            mask = sheet_df.astype(str).apply(lambda col: col.str.contains(search_inv.strip(), case=False, na=False)).any(axis=1)
            display_df = sheet_df[mask].copy()
        else:
            display_df = sheet_df.copy()

        if st.session_state.role == "Admin":
            edited_display_df = st.data_editor(
                display_df,
                use_container_width=True,
                num_rows="dynamic",
                hide_index=True,
                column_order=INVENTORY_COLUMNS,
                column_config={
                    "Nama produk": st.column_config.TextColumn("✏️ Nama Produk", width="large"),
                    "Satuan": st.column_config.TextColumn("✏️ Satuan", width="small"),
                    "Tanggal": st.column_config.DateColumn("✏️ Tanggal", format="YYYY-MM-DD", width="medium"),
                    "Nomor Faktur": st.column_config.TextColumn("✏️ Nomor Faktur", width="medium"),
                    "Nomor Batch": st.column_config.TextColumn("✏️ Nomor Batch", width="medium"),
                    "PBF": st.column_config.TextColumn("✏️ PBF", width="medium"),
                    "Tanggal Kadaluwarsa": st.column_config.DateColumn("✏️ Tanggal Kadaluarsa", format="YYYY-MM-DD", width="medium"),
                    "Stok Masuk": st.column_config.NumberColumn("✏️ Stok Masuk", min_value=0, step=1, width="small"),
                    "Stok Keluar": st.column_config.NumberColumn("✏️ Stok Keluar", min_value=0, step=1, width="small"),
                    "Stok Sisa": st.column_config.NumberColumn("✏️ Stok Sisa", min_value=0, step=1, width="small"),
                    "Harga 1": st.column_config.NumberColumn("✏️ Harga 1", min_value=0, step=1, width="small"),
                    "Harga 2": st.column_config.NumberColumn("✏️ Harga 2", min_value=0, step=1, width="small"),
                    "Keterangan": st.column_config.TextColumn("✏️ Keterangan", width="large"),
                },
                key="editor_inventory_grid"
            )

            if st.button("✅ Submit Data Terbaru", type="primary"):
                workbook_data = st.session_state.inventory_data_cache
                if not workbook_data:
                    workbook_data = load_inventory_workbook()
                    
                current_ws_df = prepare_sheet_for_editor(workbook_data[sheet_name].copy())
                
                existing_idx = edited_display_df.index.intersection(current_ws_df.index)
                current_ws_df.loc[existing_idx, edited_display_df.columns] = edited_display_df.loc[existing_idx]
                
                new_rows = edited_display_df[~edited_display_df.index.isin(current_ws_df.index)]
                if not new_rows.empty:
                    current_ws_df = pd.concat([current_ws_df, new_rows])
                    
                deleted_rows = display_df.index.difference(edited_display_df.index)
                if not deleted_rows.empty:
                    current_ws_df = current_ws_df.drop(deleted_rows)
                    
                current_ws_df = current_ws_df.reset_index(drop=True)
                workbook_data[sheet_name] = normalize_inventory_df(current_ws_df)
                
                success = save_inventory_workbook(workbook_data)
                if success:
                    st.session_state.inventory_data_cache = workbook_data
                    st.success(f"✅ Perubahan pada worksheet {sheet_name} berhasil disimpan ke Excel dan diperbarui di seluruh fitur secara real-time.")
                    st.rerun()
        else:
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_order=INVENTORY_COLUMNS,
                column_config={
                    "Tanggal": st.column_config.DateColumn("Tanggal", format="YYYY-MM-DD"),
                    "Tanggal Kadaluwarsa": st.column_config.DateColumn("Tanggal Kadaluarsa", format="YYYY-MM-DD"),
                },
                key="viewer_inventory_grid"
            )

        st.markdown("---")
        st.subheader("📊 Ringkasan Per Worksheet")
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("Worksheet Tersedia", len(workbook_data))
        with summary_cols[1]:
            st.metric("Total Record", sum(len(df) for df in workbook_data.values()))
        with summary_cols[2]:
            st.metric("Sheet Aktif", sheet_name)

        with st.expander("Lihat semua sheet yang tersedia"):
            for name, df in workbook_data.items():
                st.markdown(f"#### {name}")
                df_render = df.copy()
                for col in ["Tanggal", "Tanggal Kadaluwarsa"]:
                    if col in df_render.columns:
                        df_render[col] = df_render[col].apply(lambda x: x.strftime("%d-%m-%Y") if pd.notna(x) else "")
                st.dataframe(df_render, use_container_width=True, hide_index=True)


    # ── TAB 2: STOK OPNAME ────────────────────────────────────────────────────
    with tab_opname:
        st.markdown("<h3 style='color: #e94560;'>📦 Stok Opname Obat</h3>", unsafe_allow_html=True)
        st.caption("Gunakan tab ini untuk merekap dan mencocokkan stok fisik barang di rak dengan stok sistem. Perbedaan akan otomatis diperbarui ke Dataset.")

        if "opname_list" not in st.session_state:
            st.session_state.opname_list = pd.DataFrame()

        df_inv_full = build_inventory_print_dataframe()
        
        # --- BAGIAN 1: PENGUMPULAN ITEM OPNAME ("Pilih Obat" Modal Equivalent) ---
        with st.expander("🔍 Pilih Obat (Klik untuk mencari dan menambah item opname)", expanded=True):
            st.markdown("#### Daftar Obat Tersedia")
            
            c_f1, c_f2, c_f3 = st.columns(3)
            show_empty = c_f1.checkbox("Tampilkan Stok Habis", value=False, key="check_empty")
            sort_ed = c_f2.checkbox("Urutkan berdasarkan ED terdekat (FEFO)", value=False, key="check_fefo")
            
            if df_inv_full is not None and not df_inv_full.empty:
                df_pilih = df_inv_full.copy()
                
                if not show_empty:
                    df_pilih = df_pilih[pd.to_numeric(df_pilih["Stok Sisa"], errors='coerce').fillna(0) > 0]
                if sort_ed:
                    df_pilih["Tanggal Kadaluwarsa"] = pd.to_datetime(df_pilih["Tanggal Kadaluwarsa"], errors="coerce")
                    df_pilih = df_pilih.sort_values("Tanggal Kadaluwarsa")
                    
                df_pilih.insert(0, "Pilih", False) # Tambah kolom centang
                
                # Menggunakan kolom dataset asli yang dipetakan ke UI
                view_cols = ["Pilih", "Nama produk", "Stok Sisa", "PBF", "Worksheet", "Satuan", "Nomor Batch", "Tanggal Kadaluwarsa"]
                df_pilih_view = df_pilih[view_cols]
                
                cari_pilih = st.text_input("🔍 Cari nama obat, PBF, atau gudang (worksheet)...", key="cari_pilih")
                if cari_pilih:
                    mask_cari = df_pilih_view.astype(str).apply(lambda col: col.str.contains(cari_pilih, case=False, na=False)).any(axis=1)
                    df_pilih_view = df_pilih_view[mask_cari]
                
                edited_pilih = st.data_editor(
                    df_pilih_view,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Pilih": st.column_config.CheckboxColumn("Pilih", default=False),
                        "Nama produk": st.column_config.TextColumn("Nama Obat", disabled=True, width="large"),
                        "Stok Sisa": st.column_config.NumberColumn("Stok Sistem", disabled=True),
                        "PBF": st.column_config.TextColumn("Distributor (PBF)", disabled=True),
                        "Worksheet": st.column_config.TextColumn("Lokasi", disabled=True),
                        "Satuan": st.column_config.TextColumn("Satuan", disabled=True),
                        "Nomor Batch": st.column_config.TextColumn("No. Batch", disabled=True),
                        "Tanggal Kadaluwarsa": st.column_config.DateColumn("Tanggal Expired", disabled=True, format="DD MMM YYYY"),
                    },
                    key="pilih_obat_editor"
                )
                
                if st.button("➕ Tambahkan Item Terpilih ke Tabel Opname", type="secondary"):
                    selected_items = edited_pilih[edited_pilih["Pilih"] == True].copy()
                    if not selected_items.empty:
                        # Siapkan list untuk ditransfer ke bawah
                        new_opname = selected_items.drop(columns=["Pilih", "PBF"])
                        new_opname.rename(columns={"Stok Sisa": "Stok Sistem (Satuan)"}, inplace=True)
                        new_opname["Stok Fisik (Nyata)"] = 0.0
                        new_opname["Stok Expired/Rusak"] = 0.0
                        
                        if st.session_state.opname_list.empty:
                            st.session_state.opname_list = new_opname
                        else:
                            # Gabungkan tanpa duplikasi berdasarkan obat + lokasi + batch
                            st.session_state.opname_list = pd.concat([st.session_state.opname_list, new_opname]).drop_duplicates(subset=["Nama produk", "Worksheet", "Nomor Batch"])
                            
                        st.success(f"✅ {len(selected_items)} item berhasil ditambahkan ke daftar di bawah!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Centang minimal 1 obat pada kolom 'Pilih' terlebih dahulu.")
            else:
                st.info("Dataset masih kosong.")

        # --- BAGIAN 2: EKSEKUSI STOK OPNAME (Tabel Input) ---
        st.markdown("<br><br>", unsafe_allow_html=True)
        col_gud, col_pros, col_res = st.columns([2.5, 1.5, 1])
        with col_gud:
            AVAILABLE_SHEETS = get_available_sheets()
            pilih_gudang_opname = st.selectbox("Pilih Gudang (Filter Tampilan Bawah):", ["Semua Gudang"] + AVAILABLE_SHEETS)
            
        with col_pros:
            st.markdown("<br>", unsafe_allow_html=True)
            btn_proses_opname = st.button("✅ Proses Penyimpanan", use_container_width=True, type="primary")
            
        with col_res:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Kosongkan Daftar", use_container_width=True):
                st.session_state.opname_list = pd.DataFrame()
                st.rerun()

        if not st.session_state.opname_list.empty:
            display_opname = st.session_state.opname_list.copy()
            if pilih_gudang_opname != "Semua Gudang":
                display_opname = display_opname[display_opname["Worksheet"] == pilih_gudang_opname]
                
            if display_opname.empty:
                st.info(f"Belum ada item opname yang ditambahkan untuk gudang: {pilih_gudang_opname}")
            else:
                st.markdown(f"**Tabel Input Hitung Fisik ({len(display_opname)} data):**")
                edited_opname = st.data_editor(
                    display_opname,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Nama produk": st.column_config.TextColumn("Nama Obat", disabled=True, width="large"),
                        "Worksheet": st.column_config.TextColumn("Lokasi", disabled=True),
                        "Nomor Batch": st.column_config.TextColumn("No. Batch", disabled=True),
                        "Tanggal Kadaluwarsa": st.column_config.DateColumn("Tanggal Expired", disabled=True, format="DD MMM YYYY"),
                        "Stok Sistem (Satuan)": st.column_config.NumberColumn("Stok Sistem", disabled=True),
                        "Satuan": st.column_config.TextColumn("Satuan Terkecil", disabled=True),
                        "Stok Fisik (Nyata)": st.column_config.NumberColumn("✏️ Stok Nyata Terkecil", min_value=0.0, format="%.2f"),
                        "Stok Expired/Rusak": st.column_config.NumberColumn("✏️ Stok Expired Terkecil", min_value=0.0, format="%.2f"),
                    },
                    key="opname_main_editor"
                )
                
                st.session_state.opname_list.update(edited_opname)
                
                if btn_proses_opname:
                    workbook_data = st.session_state.inventory_data_cache
                    df_history = load_data()
                    if df_history is None:
                        df_history = pd.DataFrame(columns=KOLOM_WAJIB)
                    new_history_rows = []
                    changed_count = 0
                    
                    for idx, row in st.session_state.opname_list.iterrows():
                        stok_sistem = float(row["Stok Sistem (Satuan)"]) if pd.notna(row["Stok Sistem (Satuan)"]) else 0.0
                        stok_nyata = float(row["Stok Fisik (Nyata)"]) if pd.notna(row["Stok Fisik (Nyata)"]) else 0.0
                        stok_expired = float(row["Stok Expired/Rusak"]) if pd.notna(row["Stok Expired/Rusak"]) else 0.0
                        
                        if stok_sistem != stok_nyata or stok_expired > 0:
                            ws_name = row["Worksheet"]
                            if ws_name in workbook_data:
                                sheet_df = prepare_sheet_for_editor(workbook_data[ws_name].copy())
                                
                                mask = (sheet_df["Nama produk"].astype(str) == str(row["Nama produk"])) & (sheet_df["Nomor Batch"].astype(str) == str(row["Nomor Batch"]))
                                if mask.any():
                                    target_idx = sheet_df[mask].index[-1]
                                    sheet_df.loc[target_idx, "Stok Sisa"] = stok_nyata
                                    workbook_data[ws_name] = normalize_inventory_df(sheet_df)
                                    changed_count += 1
                                    
                                    selisih = stok_nyata - stok_sistem
                                    keterangan_opname = f"Stok Opname - Penyesuaian fisik. Selisih: {selisih}."
                                    if stok_expired > 0:
                                        keterangan_opname += f" Barang Expired/Rusak Terbuang: {stok_expired}."
                                        
                                    new_history_rows.append({
                                        "Tanggal": pd.Timestamp(date.today()),
                                        "Nama Obat": row["Nama produk"],
                                        "Kategori": ws_name, 
                                        "Satuan": row["Satuan"],
                                        "Stok Masuk": selisih if selisih > 0 else 0,
                                        "Stok Keluar": abs(selisih) if selisih < 0 else 0,
                                        "Stok Akhir": stok_nyata,
                                        "Harga Satuan (Rp)": 0,
                                        "Total Nilai (Rp)": 0,
                                        "Tanggal Kadaluarsa": row["Tanggal Kadaluwarsa"],
                                        "Keterangan": keterangan_opname
                                    })
                    
                    if changed_count > 0:
                        save_inventory_workbook(workbook_data)
                        st.session_state.inventory_data_cache = workbook_data
                        
                        if new_history_rows:
                            df_history = pd.concat([df_history, pd.DataFrame(new_history_rows)], ignore_index=True)
                            save_data(df_history)
                            
                        st.success(f"✅ Stok Opname berhasil diproses! {changed_count} jenis barang telah dikalibrasi ke dataset utama.")
                        st.session_state.opname_list = pd.DataFrame()
                        st.rerun()
                    else:
                        st.info("⚠️ Proses dibatalkan: Tidak ada data yang memiliki selisih fisik atau barang expired yang perlu disimpan (seluruh kolom Nyata & Expired bernilai 0).")
        else:
            st.info("Daftar masih kosong. Tambahkan obat melalui panel 'Pilih Obat' di atas terlebih dahulu.")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 3 — REKAP DATA
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🖨️ Rekap Data":
    st.title("🖨️ Rekap Data")
# ... [SISA CODE APLIKASI DI BAWAHNYA TETAP SAMA SEPERTI SEBELUMNYA]
