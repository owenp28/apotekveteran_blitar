import streamlit as st
import pandas as pd
import io
import re
from datetime import date, datetime
import os
from io import BytesIO
from urllib.request import Request, urlopen
from openpyxl import load_workbook, Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

st.set_page_config(page_title="Apotek Veteran Blitar", layout="wide", page_icon="💊")

# ── CSS Custom untuk Menyesuaikan Tampilan ERP ─────────────────────────────────
st.markdown(
    """
    <style>
    /* Reset default margin dan padding */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Dark Mode Background */
    body {
        background: #1a1a2e;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #e0e0e0;
    }
    
    /* Mengurangi padding di bagian atas sidebar */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem !important;
    }
    
    /* Mengurangi margin di bagian atas konten utama */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
    }
    
    /* ── Header Aplikasi ────────────────────────────────────────────────────── */
    .app-header {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .app-title {
        font-size: 42px;
        font-weight: 700;
        color: #e94560;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-subtitle {
        font-size: 16px;
        color: #a0a0a0;
        font-weight: 400;
    }
    
    /* ── Form Container ─────────────────────────────────────────────────────── */
    .form-container {
        background: #16213e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #0f3460;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .form-section-title {
        font-size: 18px;
        font-weight: 600;
        color: #e94560;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e94560;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* ── Grid Layout ────────────────────────────────────────────────────────── */
    .form-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .form-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .form-label {
        font-size: 14px;
        font-weight: 500;
        color: #a0a0a0;
    }
    
    .form-input {
        width: 100%;
        padding: 10px 14px;
        border: 1px solid #0f3460;
        border-radius: 6px;
        background: #1a1a2e;
        color: #e0e0e0;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #e94560;
        box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2);
    }
    
    .form-input:disabled {
        background: #16213e;
        color: #666;
        cursor: not-allowed;
        font-weight: 600;
    }
    
    /* ── Tombol Custom ──────────────────────────────────────────────────────── */
    .btn-custom {
        padding: 12px 24px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Tombol Cari - Coral/Merah */
    .btn-cari {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
    }
    
    .btn-cari:hover {
        background: linear-gradient(135deg, #ee5a24 0%, #d64520 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(238, 90, 36, 0.4);
    }
    
    /* Tombol Simpan - Hijau */
    .btn-save {
        background: linear-gradient(135deg, #28a745 0%, #218838 100%);
        color: white;
    }
    
    .btn-save:hover {
        background: linear-gradient(135deg, #218838 0%, #1e7e34 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
    }
    
    /* Tombol Reset - Abu-abu */
    .btn-reset {
        background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
        color: white;
    }
    
    .btn-reset:hover {
        background: linear-gradient(135deg, #5a6268 0%, #4e555b 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(108, 117, 125, 0.4);
    }
    
    /* ── Total Nominal Container ────────────────────────────────────────────── */
    .total-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px;
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border-radius: 12px;
        margin: 20px 0;
        border: 1px solid #0f3460;
    }
    
    .total-label {
        font-size: 16px;
        color: #a0a0a0;
        font-weight: 500;
    }
    
    .total-value {
        font-size: 42px;
        font-weight: 700;
        color: #e94560;
        text-align: right;
        font-family: 'Courier New', monospace;
    }
    
    /* ── Tabel Data Editor ──────────────────────────────────────────────────── */
    .table-container {
        background: #16213e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #0f3460;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .table-title {
        font-size: 18px;
        font-weight: 600;
        color: #e94560;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e94560;
    }
    
    /* Styling untuk data editor */
    .stDataFrame {
        background: #1a1a2e;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .stDataFrame th {
        background: #0f3460;
        color: #e0e0e0;
        font-weight: 600;
        font-size: 13px;
        padding: 10px;
    }
    
    .stDataFrame td {
        color: #e0e0e0;
        font-size: 13px;
        padding: 8px;
    }
    
    .stDataFrame tr:hover {
        background: #1f3a5e;
    }
    
    /* ── Info Box ───────────────────────────────────────────────────────────── */
    .info-box {
        background: #1f3a5e;
        border-left: 4px solid #e94560;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
    
    .info-box strong {
        color: #e94560;
    }
    
    /* ── Footer ─────────────────────────────────────────────────────────────── */
    .app-footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 14px;
        margin-top: 30px;
    }
    
    /* ── Action Buttons Container ───────────────────────────────────────────── */
    .action-buttons {
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }
    
    /* ── Responsive ─────────────────────────────────────────────────────────── */
    @media (max-width: 768px) {
        .form-grid {
            grid-template-columns: 1fr;
        }
        
        .form-grid-4 {
            grid-template-columns: 1fr;
        }
        
        .total-container {
            flex-direction: column;
            gap: 15px;
        }
        
        .total-value {
            text-align: center;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ─────────────────────────────────────────────────────────────────────────────

DATASET_PATH = os.path.join(os.path.dirname(__file__), "stok_obat.csv")
RETUR_HISTORY_PATH = os.path.join(os.path.dirname(__file__), "retur_history.csv")
WORKBOOK_PATH = os.path.join(os.path.dirname(__file__), "DatasetObat_ApotekVeteran.xlsx")
CSV_PATH = os.path.join(os.path.dirname(__file__), "apotek_realtime.csv")
SHIFT_LOG_PATH = os.path.join(os.path.dirname(__file__), "shift_log.csv")
DEFAULT_SOURCE_URL = WORKBOOK_PATH
DEFAULT_SOURCE_LABEL = WORKBOOK_PATH

INVENTORY_SHEETS = ["PCS", "SACHET", "BOTOL", "TAB", "BOX", "STRIP"]
INVENTORY_COLUMNS = [
    "Nama produk",
    "Satuan",
    "Tanggal",
    "Nomor Faktur",
    "Nomor Batch",
    "PBF",
    "Tanggal Kadaluwarsa",
    "Stok Masuk",
    "Stok Keluar",
    "Stok Sisa",
    "Harga 1",
    "Harga 2",
    "Keterangan"
]

KOLOM_DATABASE_OBAT = [
    "id_obat",
    "nama_obat",
    "kategori",
    "satuan",           
    "isi_per_strip",    
    "isi_per_box",      
    "harga_beli",       
    "harga_1",          
    "harga_2",          
    "harga_3",
    "stok_akhir",       
    "tanggal_kadaluarsa"
]

KOLOM_WAJIB = [
    "Tanggal", "Nama Obat", "Kategori", "Satuan",
    "Stok Masuk", "Stok Keluar", "Stok Akhir",
    "Harga Satuan (Rp)", "Total Nilai (Rp)",
    "Tanggal Kadaluarsa", "Keterangan"
]

RETUR_HISTORY_COLUMNS = [
    "Nomor Faktur", "Tanggal Retur",
    "Jumlah Item", "Total Nilai Retur", "Tanggal Disimpan"
]

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
            "Waktu Buka", "Waktu Tutup", "Pilih Shift", "Nama Kasir", "Saldo Awal", 
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


def normalize_inventory_df(df):
    df = df.copy()
    renamed = {}
    for kolom in df.columns:
        nama_kolom = str(kolom).strip()
        if nama_kolom == "Nama obat":
            renamed[kolom] = "Nama produk"
        elif nama_kolom == "Nama Produk":
            renamed[kolom] = "Nama produk"
        elif nama_kolom == "PBF ":
            renamed[kolom] = "PBF"
        elif nama_kolom == "Keterangan ":
            renamed[kolom] = "Keterangan"
        elif nama_kolom == "Nama produk":
            renamed[kolom] = "Nama produk"
    if renamed:
        df = df.rename(columns=renamed)
    for kolom in INVENTORY_COLUMNS:
        if kolom not in df.columns:
            df[kolom] = None
    df = df[INVENTORY_COLUMNS]

    text_like_columns = [
        "Nama produk",
        "Satuan",
        "Nomor Faktur",
        "Nomor Batch",
        "PBF",
        "Keterangan"
    ]
    for kolom in text_like_columns:
        if kolom in df.columns:
            df[kolom] = df[kolom].astype("string")

    numeric_columns = ["Stok Masuk", "Stok Keluar", "Stok Sisa", "Harga 1", "Harga 2"]
    for kolom in numeric_columns:
        if kolom in df.columns:
            df[kolom] = pd.to_numeric(df[kolom], errors="coerce")

    if "Tanggal" in df.columns:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    if "Tanggal Kadaluwarsa" in df.columns:
        df["Tanggal Kadaluwarsa"] = pd.to_datetime(df["Tanggal Kadaluwarsa"], errors="coerce")

    return df


def prepare_sheet_for_editor(df):
    df = normalize_inventory_df(df)
    for kolom in ["Nomor Faktur", "Nomor Batch", "PBF", "Keterangan", "Nama produk", "Satuan"]:
        if kolom in df.columns:
            df[kolom] = df[kolom].astype("string")
    return df


def _find_inventory_header_row(rows):
    known_headers = {
        "nama produk",
        "nama obat",
        "satuan",
        "tanggal",
        "nomor faktur",
        "nomor batch",
        "pbf",
        "tanggal kadaluarsa",
        "stok masuk",
        "stok keluar",
        "stok sisa",
        "harga 1",
        "harga 2",
        "keterangan"
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
    if "1drv.ms" in source_url or "onedrive.live.com/:x:" in source_url:
        return DEFAULT_SOURCE_URL
    if "download.aspx?UniqueId=" in source_url:
        return source_url
    if source_url.endswith(".csv") or source_url.endswith(".xlsx") or source_url.endswith(".xlsm"):
        return source_url
    return DEFAULT_SOURCE_URL


def sync_inventory_from_source(source_url=None):
    source_url = normalize_source_url(source_url)
    if not source_url:
        return False

    try:
        request = Request(
            source_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/octet-stream, */*"
            }
        )
        with urlopen(request, timeout=45) as response:
            data = response.read()

        if not data:
            raise ValueError("File download dari link sumber kosong.")

        with open(WORKBOOK_PATH, "wb") as f:
            f.write(data)
        return os.path.exists(WORKBOOK_PATH)
    except Exception:
        if not os.path.exists(WORKBOOK_PATH):
            create_default_inventory_workbook()
        return os.path.exists(WORKBOOK_PATH)


def load_inventory_from_bytes(file_bytes, filename):
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(BytesIO(file_bytes))
        return {sheet_name: normalize_inventory_df(df) for sheet_name in INVENTORY_SHEETS[:1]}

    wb = load_workbook(BytesIO(file_bytes), data_only=True)
    workbook_data = {}
    for sheet_name in INVENTORY_SHEETS:
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        workbook_data[sheet_name] = load_inventory_sheet_dataframe(ws)
    return workbook_data


def load_inventory_workbook(source_url=None, uploaded_file=None):
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        loaded = load_inventory_from_bytes(data, uploaded_file.name)
        if loaded:
            return loaded

    if os.path.exists(WORKBOOK_PATH):
        try:
            wb = load_workbook(WORKBOOK_PATH, data_only=True)
            workbook_data = {}
            for sheet_name in INVENTORY_SHEETS:
                if sheet_name not in wb.sheetnames:
                    continue
                ws = wb[sheet_name]
                workbook_data[sheet_name] = load_inventory_sheet_dataframe(ws)
            wb.close()
            return workbook_data
        except Exception:
            return {}

    sync_inventory_from_source(source_url)
    if not os.path.exists(WORKBOOK_PATH):
        return {}

    try:
        wb = load_workbook(WORKBOOK_PATH, data_only=True)
        workbook_data = {}
        for sheet_name in INVENTORY_SHEETS:
            if sheet_name not in wb.sheetnames:
                continue
            ws = wb[sheet_name]
            workbook_data[sheet_name] = load_inventory_sheet_dataframe(ws)
        wb.close()
        return workbook_data
    except Exception:
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
            for sheet_name in INVENTORY_SHEETS:
                df_sheet = workbook_data.get(sheet_name)
                if df_sheet is None:
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
    combined_df = normalize_inventory_df(combined_df)
    combined_df["Worksheet"] = combined_df.get("Worksheet", pd.Series([None] * len(combined_df)))
    return combined_df


def build_rtf_export(df):
    lines = ["{\\rtf1\\ansi\\deff0", "{\\fonttbl\\f0\\fswiss Arial;}", "\\viewkind4\\uc1"]
    lines.append("\\pard\\plain\\f0\\fs20 Laporan Stok Obat — Apotek Veteran Blitar\\par")
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


# ══════════════════════════════════════════════════════════════════════════════
# AUTENTIKASI — LOGIN & USER MAPPING
# ══════════════════════════════════════════════════════════════════════════════
USERS = {
    "admin123@gmail.com": {"password": "admin123", "role": "Admin", "name": "Ivonne"},
    # Mengganti role "Karyawan Apotek" menjadi "Kasir" agar sinkron dengan form st.selectbox di bawah
    "karyawan1@gmail.com": {"password": "karyawan1", "role": "Kasir", "name": "Karyawan 1 (Dian)"},
    "karyawan2@gmail.com": {"password": "karyawan2", "role": "Kasir", "name": "Karyawan 2 (Julia)"},
    "kasir123@gmail.com": {"password": "kasir12", "role": "Kasir", "name": "Kasir - Karyawan Apotek"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown(
        """
        <div style='max-width:380px; margin:80px auto 0 auto; padding:32px 36px;
                    border:1px solid #dde3ed; border-radius:12px;
                    box-shadow:0 4px 18px rgba(44,123,229,0.10); background:#fff;'>
            <div style='text-align:center; margin-bottom:18px;'>
                <img src='https://img.icons8.com/color/96/pharmacy-shop.png' width='64'/>
                <h2 style='margin:8px 0 2px 0; color:#2c7be5;'>Apotek Veteran Blitar</h2>
                <p style='color:#888; font-size:13px; margin:0;'>Silakan login untuk melanjutkan</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    with st.form("form_login"):
        st.markdown("<div style='max-width:380px; margin:0 auto;'>", unsafe_allow_html=True)
        role_pilih = st.selectbox("Login sebagai", ["Admin", "Kasir"])
        username   = st.text_input("Username")
        password   = st.text_input("Password", type="password")
        login_btn  = st.form_submit_button("🔐 Login", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if login_btn:
            uname = username.strip()
            if uname in USERS and USERS[uname]["password"] == password and USERS[uname]["role"] == role_pilih:
                st.session_state.logged_in = True
                st.session_state.role      = role_pilih
                st.session_state.username  = uname
                st.rerun()
            else:
                st.error("Username, password, atau role tidak sesuai.")
    st.stop()

# ── Session State (General & Shift) ───────────────────────────────────────────
if "retur_form_data" not in st.session_state:
    st.session_state.retur_form_data = {}
if "retur_items" not in st.session_state:
    st.session_state.retur_items = pd.DataFrame(columns=[
        "Pilih", "Kode", "Nama Obat", "Satuan", "No. Batch",
        "Tanggal Exp", "Ketentuan Retur", "Maks bln sblm ED",
        "Tersedia", "Jumlah Retur", "HPP", "Subtotal"
    ])
if "retur_history" not in st.session_state:
    st.session_state.retur_history = load_retur_history()
    if st.session_state.retur_history is None:
        st.session_state.retur_history = pd.DataFrame(columns=RETUR_HISTORY_COLUMNS)
if "edited_df_data" not in st.session_state:
    st.session_state.edited_df_data = pd.DataFrame(columns=[
        "Pilih", "Kode", "Nama Obat", "Satuan", "No. Batch",
        "Tanggal Exp", "Ketentuan Retur", "Maks bln sblm ED",
        "Tersedia", "Jumlah Retur", "HPP"
    ])
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

# ── Sidebar navigasi ──────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/pharmacy-shop.png", width=80)
st.sidebar.title("💊 Apotek Veteran Blitar")
st.sidebar.markdown("---")

_role = st.session_state.role
_name = USERS[st.session_state.username]["name"]
st.sidebar.markdown(f"👤 **{_name}** — *{_role}*")
st.sidebar.markdown("---")

if _role == "Admin":
    _menu_options = [
        "🏠 Beranda",
        "📋 Tampilkan Dan Ubah Stok Obat",
        "🖨️ Cetak & Print Stok Obat",
        "📦 Entri & Retur Pembelian",
        "🛒 Kasir Pembelian Obat",
        "🕒 Buka/Tutup Shift"
    ]
else:  
    _menu_options = [
        "🏠 Beranda",
        "📋 Tampilkan Dan Ubah Stok Obat",
        "🛒 Kasir Pembelian Obat",
        "🕒 Buka/Tutup Shift"
    ]

menu = st.sidebar.radio("Pilih Fitur", _menu_options, index=0)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.role      = None
    st.session_state.username  = ""
    # Reset Shift saat logout supaya safety
    st.session_state.shift_active = False
    st.session_state.active_shift_context = {
        "saldo_awal": 0.0, "accumulated_sales_expected": 0.0, "start_time": None, "user_name": "", "shift_name": "Pagi"
    }
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# BERANDA
# ══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Beranda":
    st.title("💊 Dashboard Apotek Veteran Blitar")
    st.markdown("Selamat datang! Pilih fitur di sidebar untuk mulai mengelola stok obat.")
    st.markdown("---")

    # ── PERBAIKAN: Memaksa reload dari file DatasetObat_ApotekVeteran.xlsx lokal agar perubahan eksternal selalu terbaca
    if os.path.exists(WORKBOOK_PATH):
        st.session_state.inventory_data_cache = load_inventory_workbook(DEFAULT_SOURCE_URL)

    all_items_df = build_inventory_print_dataframe()
    
    if all_items_df is None or all_items_df.empty:
        st.info("Dataset belum tersedia. Silakan upload dataset di menu **📋 Tampilkan Dan Ubah Stok Obat**.")
    else:
        # ── PERBAIKAN: Bersihkan data (hapus baris kosong/nan) yang membuat data stok menipis berantakan
        all_items_df["Nama produk"] = all_items_df["Nama produk"].astype(str).str.strip()
        all_items_df = all_items_df[
            (all_items_df["Nama produk"] != "") & 
            (all_items_df["Nama produk"].str.lower() != "nan") &
            (all_items_df["Nama produk"].notna())
        ]
        
        all_items_df["Stok Sisa"] = pd.to_numeric(all_items_df["Stok Sisa"], errors="coerce").fillna(0)
        all_items_df["Harga 1"] = pd.to_numeric(all_items_df["Harga 1"], errors="coerce").fillna(0)
        all_items_df["Tanggal Kadaluwarsa"] = pd.to_datetime(all_items_df["Tanggal Kadaluwarsa"], errors="coerce")
        
        total_jenis = all_items_df["Nama produk"].nunique()
        total_stok = all_items_df["Stok Sisa"].sum()
        
        tgl_batas = pd.Timestamp(date.today()) + pd.Timedelta(days=30)
        exp_soon_df = all_items_df[(all_items_df["Tanggal Kadaluwarsa"] <= tgl_batas) & (all_items_df["Stok Sisa"] > 0)]
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
            stok_summary = all_items_df.groupby(["Worksheet", "Nama produk"])["Stok Sisa"].sum().reset_index()
            stok_menipis = stok_summary[stok_summary["Stok Sisa"] <= 20].sort_values("Stok Sisa")
            
            if stok_menipis.empty:
                st.success("Tidak ada obat dengan stok menipis.")
            else:
                st.dataframe(
                    stok_menipis.rename(columns={"Nama produk": "Nama Obat", "Stok Sisa": "Total Stok"}),
                    use_container_width=True, hide_index=True
                )
        with col_exp:
            st.markdown("#### ⏰ Segera Kadaluarsa (≤30 hari)")
            if exp_soon_df.empty:
                st.success("Tidak ada obat yang mendekati tanggal kadaluarsa.")
            else:
                exp_show = exp_soon_df[["Nama produk", "Worksheet", "Tanggal Kadaluwarsa", "Stok Sisa"]].copy()
                exp_show["Tanggal Kadaluwarsa"] = exp_show["Tanggal Kadaluwarsa"].dt.strftime("%d-%m-%Y")
                st.dataframe(
                    exp_show.rename(columns={"Nama produk": "Nama Obat", "Tanggal Kadaluwarsa": "Tgl Expired"}),
                    use_container_width=True, hide_index=True
                )

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 1 — TAMPILKAN DAN UBAH STOK OBAT
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📋 Tampilkan Dan Ubah Stok Obat":
    st.title("📋 Tampilkan Dan Ubah Stok Obat")
    st.caption("Tampilan sederhana dan bisa diedit langsung per worksheet sesuai satuan: PCS, SACHET, BOTOL, TAB, BOX, STRIP.")

    if "inventory_source_url" not in st.session_state:
        st.session_state.inventory_source_url = DEFAULT_SOURCE_LABEL
    if "inventory_data_cache" not in st.session_state:
        st.session_state.inventory_data_cache = {}

    source_url = st.text_input(
        "Link Workbook / CSV Sumber",
        value=st.session_state.inventory_source_url,
        help="Contoh: link OneDrive, Google Drive, atau URL file Excel/CSV yang bisa di-download langsung."
    )
    if source_url != st.session_state.inventory_source_url:
        st.session_state.inventory_source_url = source_url
        if source_url.strip():
            st.session_state.inventory_data_cache = load_inventory_workbook(source_url)

    uploaded_inventory = st.file_uploader(
        "Upload file Excel/CSV langsung dari web",
        type=["xlsx", "xlsm", "csv"],
        key="upload_inventory_source"
    )

    if uploaded_inventory is not None:
        workbook_data = load_inventory_workbook(source_url, uploaded_inventory)
        st.session_state.inventory_data_cache = workbook_data
        st.success("✅ Data berhasil dimuat langsung dari file upload.")
    else:
        workbook_data = st.session_state.inventory_data_cache
        if not workbook_data:
            workbook_data = load_inventory_workbook(source_url)
            st.session_state.inventory_data_cache = workbook_data

    if not workbook_data:
        st.info("Sumber file belum bisa dibaca, jadi sistem akan membuat struktur default untuk sheet PCS, SACHET, BOTOL, TAB, BOX, dan STRIP.")

    sheet_name = st.selectbox(
        "Pilih Worksheet",
        INVENTORY_SHEETS,
        index=0,
        key="inventory_selected_sheet"
    )

    if sheet_name not in workbook_data:
        sheet_df = pd.DataFrame(columns=INVENTORY_COLUMNS)
        sheet_df = prepare_sheet_for_editor(sheet_df)
    else:
        sheet_df = prepare_sheet_for_editor(workbook_data[sheet_name].copy())

    st.info("Setiap kolom dalam tabel dapat diedit langsung dengan ikon ✏️. Anda juga dapat memfilter menggunakan kotak pencarian di bawah.")
    
    search_inv = st.text_input("🔍 Pencarian Baris (Nama, Batch, Faktur, PBF, dll di Worksheet ini)", placeholder="Ketik kata kunci...")
    if search_inv.strip():
        mask = sheet_df.astype(str).apply(lambda col: col.str.contains(search_inv.strip(), case=False, na=False)).any(axis=1)
        display_df = sheet_df[mask].copy()
    else:
        display_df = sheet_df.copy()

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
            st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    with st.expander("🕘 Riwayat Transaksi Stok Kasir (Pembelian & Penjualan)"):
        df = load_data()
        if df is None or df.empty:
            st.info("Belum ada riwayat transaksi Kasir.")
        else:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                bulan_list = sorted(df["Tanggal"].dt.to_period("M").unique().astype(str).tolist(), reverse=True)
                bulan_sel = st.selectbox("Pilih Bulan", ["Semua"] + bulan_list, key="riwayat_bulan")
            with col_r2:
                cari_riwayat = st.text_input("🔎 Cari Transaksi (Nama Obat, Kategori, Keterangan, dll)", key="riwayat_cari")

            df_riwayat = df.copy()
            if bulan_sel != "Semua":
                df_riwayat = df_riwayat[df_riwayat["Tanggal"].dt.to_period("M").astype(str) == bulan_sel]
                
            if cari_riwayat.strip():
                mask = df_riwayat.astype(str).apply(lambda col: col.str.contains(cari_riwayat.strip(), case=False, na=False)).any(axis=1)
                df_riwayat = df_riwayat[mask]

            riwayat_display = df_riwayat.sort_values("Tanggal", ascending=False).copy()
            riwayat_display["Tanggal"] = riwayat_display["Tanggal"].dt.strftime("%d-%m-%Y")
            riwayat_display["Tanggal Kadaluarsa"] = riwayat_display["Tanggal Kadaluarsa"].dt.strftime("%d-%m-%Y")
            riwayat_display["Harga Satuan (Rp)"] = riwayat_display["Harga Satuan (Rp)"].apply(format_rupiah)
            riwayat_display["Total Nilai (Rp)"] = riwayat_display["Total Nilai (Rp)"].apply(format_rupiah)
            st.dataframe(riwayat_display, use_container_width=True, height=350)
            st.caption(f"Menampilkan {len(df_riwayat)} baris riwayat transaksi")

        st.markdown("---")
        st.markdown("**📂 Import Riwayat Transaksi dari CSV (opsional — lewati saja jika data Anda sudah dicatat lewat Entri Pembelian & Kasir)**")
        uploaded = st.file_uploader("Pilih file CSV", type=["csv"], key="upload_riwayat")
        if uploaded:
            file_id_riwayat = f"{uploaded.name}_{uploaded.size}"

            if st.session_state.get("last_import_riwayat_id") == file_id_riwayat:
                st.info("✅ File ini sudah pernah diimpor. Hapus file dari kotak upload lalu upload file BARU jika ingin mengimpor lagi (supaya data tidak dobel).")
            else:
                try:
                    df_up = pd.read_csv(uploaded, parse_dates=["Tanggal", "Tanggal Kadaluarsa"])
                    missing = [c for c in KOLOM_WAJIB if c not in df_up.columns]
                    if missing:
                        st.error(f"Kolom berikut tidak ditemukan: {missing}")
                    else:
                        df_up = df_up[KOLOM_WAJIB]
                        df_current = load_data()
                        df_gabungan = pd.concat([df_current, df_up], ignore_index=True) if df_current is not None else df_up
                        save_data(df_gabungan)
                        st.session_state.last_import_riwayat_id = file_id_riwayat
                        st.success("Riwayat transaksi berhasil diimpor!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Gagal membaca file: {e}")

        if st.button("🗑️ Hapus Seluruh Riwayat Transaksi", type="secondary"):
            if os.path.exists(DATASET_PATH):
                os.remove(DATASET_PATH)
                st.success("Riwayat transaksi dihapus.")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 3 — CETAK & PRINT STOK OBAT
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🖨️ Cetak & Print Stok Obat":
    st.title("🖨️ Cetak & Print Stok Obat")

    df_inventory = build_inventory_print_dataframe()
    if df_inventory is None or df_inventory.empty:
        st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu di menu **📋 Tampilkan Dan Ubah Stok Obat**.")
        st.stop()

    st.subheader("Pilih Opsi Cetak")
    opsi = st.radio("Opsi Data yang Dicetak", ["Semua Komponen Obat", "Sebagian Komponen Obat (Pilih Manual)"])

    df_inventory["Tanggal"] = pd.to_datetime(df_inventory["Tanggal"], errors="coerce")
    if "Tanggal Kadaluwarsa" in df_inventory.columns:
        df_inventory["Tanggal Kadaluwarsa"] = pd.to_datetime(df_inventory["Tanggal Kadaluwarsa"], errors="coerce")

    st.markdown("---")
    st.subheader("🔍 Filter & Cari Sebelum Cetak")
    
    col_a, col_b = st.columns(2)
    with col_a:
        tgl_awal = st.date_input("Dari Tanggal", value=df_inventory["Tanggal"].dropna().min().date() if not df_inventory["Tanggal"].dropna().empty else date.today())
    with col_b:
        tgl_akhir = st.date_input("Sampai Tanggal", value=df_inventory["Tanggal"].dropna().max().date() if not df_inventory["Tanggal"].dropna().empty else date.today())

    search_print = st.text_input("🔍 Cari Spesifik (Nama Produk, Batch, Faktur, dll) - Opsional", placeholder="Ketik kata kunci untuk membatasi print out...")
    
    df_print = df_inventory[
        (df_inventory["Tanggal"] >= pd.Timestamp(tgl_awal)) &
        (df_inventory["Tanggal"] <= pd.Timestamp(tgl_akhir))
    ].copy()

    if search_print.strip():
        mask_print = df_print.astype(str).apply(lambda col: col.str.contains(search_print.strip(), case=False, na=False)).any(axis=1)
        df_print = df_print[mask_print]

    if opsi == "Sebagian Komponen Obat (Pilih Manual)":
        kolom_dipilih = st.multiselect(
            "Pilih Kolom yang Ingin Dicetak",
            options=df_print.columns.tolist(),
            default=["Worksheet", "Tanggal", "Nama produk", "Satuan", "Nomor Faktur", "Nomor Batch", "PBF", "Tanggal Kadaluwarsa", "Stok Masuk", "Stok Keluar", "Stok Sisa", "Harga 1", "Harga 2", "Keterangan"]
        )
        if kolom_dipilih:
            df_print = df_print[kolom_dipilih]
        else:
            st.warning("Pilih minimal satu kolom.")
            st.stop()

    st.markdown("---")
    st.subheader("👁️ Preview Data")
    preview_df = df_print.copy()
    if "Tanggal" in preview_df.columns:
        preview_df["Tanggal"] = preview_df["Tanggal"].dt.strftime("%d-%m-%Y")
    if "Tanggal Kadaluwarsa" in preview_df.columns:
        preview_df["Tanggal Kadaluwarsa"] = preview_df["Tanggal Kadaluwarsa"].dt.strftime("%d-%m-%Y")
    if "Harga 1" in preview_df.columns:
        preview_df["Harga 1"] = preview_df["Harga 1"].apply(lambda x: format_rupiah(x) if pd.notna(x) else x)
    if "Harga 2" in preview_df.columns:
        preview_df["Harga 2"] = preview_df["Harga 2"].apply(lambda x: format_rupiah(x) if pd.notna(x) else x)

    st.dataframe(preview_df, use_container_width=True, height=350)
    st.caption(f"{len(df_print)} baris data siap dicetak")

    st.markdown("---")
    st.subheader("⬇️ Unduh File")
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    csv_buf = df_print.copy()
    if "Tanggal" in csv_buf.columns:
        csv_buf["Tanggal"] = csv_buf["Tanggal"].dt.strftime("%d-%m-%Y")
    if "Tanggal Kadaluwarsa" in csv_buf.columns:
        csv_buf["Tanggal Kadaluwarsa"] = csv_buf["Tanggal Kadaluwarsa"].dt.strftime("%d-%m-%Y")
    csv_data = csv_buf.to_csv(index=False).encode("utf-8-sig")
    col_d1.download_button(
        label="📄 Unduh CSV",
        data=csv_data,
        file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.csv",
        mime="text/csv"
    )

    try:
        import openpyxl
        xlsx_buf = io.BytesIO()
        with pd.ExcelWriter(xlsx_buf, engine="openpyxl") as writer:
            excel_df = df_print.copy()
            if "Tanggal" in excel_df.columns:
                excel_df["Tanggal"] = excel_df["Tanggal"].dt.strftime("%d-%m-%Y")
            if "Tanggal Kadaluwarsa" in excel_df.columns:
                excel_df["Tanggal Kadaluwarsa"] = excel_df["Tanggal Kadaluwarsa"].dt.strftime("%d-%m-%Y")
            excel_df.to_excel(writer, index=False, sheet_name="Stok Obat")
        col_d2.download_button(
            label="📊 Unduh Excel (XLSX)",
            data=xlsx_buf.getvalue(),
            file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ImportError:
        col_d2.info("Install `openpyxl` untuk ekspor Excel.")

    rtf_bytes = build_rtf_export(preview_df)
    col_d3.download_button(
        label="📝 Unduh RTF (Word)",
        data=rtf_bytes,
        file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.rtf",
        mime="application/rtf"
    )

    col_d4.markdown("#### 🖨️ Print / PDF")
    html_rows = ""
    for _, row in preview_df.iterrows():
        html_rows += "<tr>" + "".join(f"<td>{v}</td>" for v in row.values) + "</tr>"
    html_headers = "".join(f"<th>{c}</th>" for c in preview_df.columns)

    html_content = f"""
    <html><head>
    <meta charset='utf-8'>
    <title>Stok Obat Apotek Veteran Blitar</title>
    <style>
      body {{ font-family: Arial, sans-serif; font-size: 11px; margin: 20px; }}
      h2 {{ text-align: center; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border: 1px solid #333; padding: 4px 8px; text-align: left; }}
      th {{ background: #2c7be5; color: white; }}
      tr:nth-child(even) {{ background: #f2f2f2; }}
      @media print {{ button {{ display: none; }} }}
    </style>
    </head><body>
    <h2>Laporan Stok Obat — Apotek Veteran Blitar</h2>
    <p>Periode: {tgl_awal} s/d {tgl_akhir} &nbsp;|&nbsp; Dicetak: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
    <table><thead><tr>{html_headers}</tr></thead><tbody>{html_rows}</tbody></table>
    <br><button onclick='window.print()' style='padding:8px 20px;background:#2c7be5;color:white;border:none;border-radius:4px;cursor:pointer;font-size:13px;'>🖨️ Print / Simpan PDF</button>
    </body></html>
    """

    html_bytes = html_content.encode("utf-8")
    col_d4.download_button(
        label="🖨️ Unduh HTML (Print/PDF)",
        data=html_bytes,
        file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.html",
        mime="text/html"
    )
    col_d4.caption("Buka file HTML → klik tombol Print → pilih 'Save as PDF'")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 4 — KASIR PEMBELIAN OBAT
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🛒 Kasir Pembelian Obat":
    st.title("🛒 Kasir Pembelian Obat")

    if "inventory_data_cache" not in st.session_state or not st.session_state.inventory_data_cache:
        st.warning("Dataset Excel belum tersedia. Silakan upload terlebih dahulu di menu **📋 Tampilkan Dan Ubah Stok Obat**.")
        st.stop()
        
    all_items_df = build_inventory_print_dataframe()
    if all_items_df is None or all_items_df.empty:
        st.warning("Data stok kosong.")
        st.stop()

    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "checkout_mode" not in st.session_state:
        st.session_state.checkout_mode = False
    if "bayar_tunai" not in st.session_state:
        st.session_state.bayar_tunai = 0
    if "nota_confirmed" not in st.session_state:
        st.session_state.nota_confirmed = False

    col_input, col_nota = st.columns([1, 1])

    with col_input:
        st.subheader("🛒 Input Penjualan")
        st.caption("Penjualan memotong stok secara real-time dari Dataset Excel berdasarkan Worksheet dan Batch.")

        available_items = all_items_df[all_items_df["Stok Sisa"].fillna(0) > 0].copy()
        if available_items.empty:
            st.info("Tidak ada obat dengan stok tersedia (>0).")
        else:
            available_items["Label"] = available_items.apply(
                lambda x: f"Nama: {str(x['Nama produk']).strip()} | Batch: {str(x['Nomor Batch']).strip() if pd.notna(x['Nomor Batch']) and str(x['Nomor Batch']).strip() != '' else '-'} | Faktur: {str(x['Nomor Faktur']).strip() if pd.notna(x['Nomor Faktur']) and str(x['Nomor Faktur']).strip() != '' else '-'} | Exp: {pd.to_datetime(x['Tanggal Kadaluwarsa']).strftime('%d-%m-%Y') if pd.notna(x['Tanggal Kadaluwarsa']) else '-'} | Sisa: {int(x['Stok Sisa'])} ({str(x['Worksheet']).strip()})",
                axis=1
            )

            if not st.session_state.checkout_mode:
                selected_label = st.selectbox("Pilih Obat (Bisa diketik untuk mencari)", available_items["Label"].unique().tolist(), key="kasir_pilih_obat")
                selected_row_display = available_items[available_items["Label"] == selected_label].iloc[0]
                
                satuan_display = str(selected_row_display["Satuan"]).strip() if pd.notna(selected_row_display["Satuan"]) and str(selected_row_display["Satuan"]).strip() != "" else str(selected_row_display["Worksheet"]).strip()

                with st.form("form_kasir"):
                    col_su, col_sh = st.columns(2)
                    with col_su:
                        st.text_input("Satuan Jual", value=satuan_display, disabled=True)
                    with col_sh:
                        skema_harga = st.selectbox("Skema Harga", ["Harga 1", "Harga 2"])

                    jumlah = st.number_input("Jumlah", min_value=1, value=1)
                    add_to_cart = st.form_submit_button("➕ Tambah ke Nota")

                    if add_to_cart:
                        selected_row = available_items[available_items["Label"] == selected_label].iloc[0]
                        nama_obat = selected_row["Nama produk"]
                        ws_target = selected_row["Worksheet"]
                        batch_target = selected_row["Nomor Batch"]
                        satuan_jual = satuan_display
                        
                        harga_per_satuan = float(selected_row["Harga 1"]) if skema_harga == "Harga 1" else float(selected_row["Harga 2"])
                        if pd.isna(harga_per_satuan): harga_per_satuan = 0.0
                        
                        subtotal = harga_per_satuan * jumlah
                        stok_tersedia = float(selected_row["Stok Sisa"])

                        if jumlah > stok_tersedia:
                            st.error(f"❌ Stok tidak cukup! Tersedia {stok_tersedia:.0f}, dibutuhkan {jumlah:.0f}.")
                        else:
                            st.session_state.cart.append({
                                "nama": nama_obat,
                                "worksheet": ws_target,
                                "batch": batch_target,
                                "satuan_jual": satuan_jual,
                                "qty": jumlah,
                                "skema_harga": skema_harga,
                                "harga_per_satuan": harga_per_satuan,
                                "subtotal": subtotal,
                                "tgl_exp": selected_row["Tanggal Kadaluwarsa"]
                            })
                            st.success(f"{nama_obat} ({jumlah} {satuan_jual}) ditambah ke nota!")

                if st.session_state.cart:
                    st.markdown("**🧾 Item dalam keranjang:**")
                    for i, item in enumerate(st.session_state.cart):
                        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                        c1.write(f"{item['nama']} ({item['skema_harga']})")
                        c2.write(f"x{item['qty']} {item['satuan_jual']}")
                        c3.write(format_rupiah(item['subtotal']))
                        with c4:
                            col_min, col_del = st.columns(2)
                            with col_min:
                                if st.button("➖", key=f"min_{i}", help="Kurangi 1"):
                                    if st.session_state.cart[i]["qty"] > 1:
                                        st.session_state.cart[i]["qty"] -= 1
                                        st.session_state.cart[i]["subtotal"] = (
                                            st.session_state.cart[i]["harga_per_satuan"] * st.session_state.cart[i]["qty"]
                                        )
                                    else:
                                        st.session_state.cart.pop(i)
                                    st.rerun()
                            with col_del:
                                if st.button("🗑️", key=f"del_{i}", help="Hapus item"):
                                    st.session_state.cart.pop(i)
                                    st.rerun()
                    st.markdown("")
                    if st.button("✅ Selesai Menambah Item", type="primary"):
                        st.session_state.checkout_mode = True
                        st.rerun()
            else:
                st.info(f"🛒 {len(st.session_state.cart)} item dalam keranjang. Masukkan nominal bayar.")
                bayar_input = st.number_input("Nominal Bayar (Rp)", min_value=0, step=500, value=st.session_state.bayar_tunai)
                st.session_state.bayar_tunai = bayar_input

                col_teliti, col_submit = st.columns(2)
                with col_teliti:
                    if st.button("🔍 Teliti Kembali", type="secondary", use_container_width=True):
                        st.session_state.checkout_mode = False
                        st.session_state.nota_confirmed = False
                        st.rerun()
                with col_submit:
                    if st.button("✅ Submit Pembayaran", type="primary", use_container_width=True):
                        if st.session_state.bayar_tunai <= 0:
                            st.error("Nominal bayar harus diisi!")
                        else:
                            st.session_state.nota_confirmed = True
                            st.rerun()

    with col_nota:
        st.subheader("📄 Preview Nota")

        if st.session_state.cart:
            total_belanja = sum(item["subtotal"] for item in st.session_state.cart)
            bayar_tunai = st.session_state.bayar_tunai if st.session_state.nota_confirmed else 0
            kembali = bayar_tunai - total_belanja
            tgl_nota = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            items_html = ""
            for item in st.session_state.cart:
                items_html += f"""
                <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                    <span style='flex: 2;'>{item['qty']} {item['nama']}</span>
                    <span style='flex: 1; text-align: center;'>{format_rupiah(item['harga_per_satuan'])}</span>
                    <span style='flex: 1; text-align: right;'>{format_rupiah(item['subtotal'])}</span>
                </div>
                """

            nota_html = f"""
            <div style="font-family: monospace; font-size: 13px; border: 1px solid #ccc;
                        padding: 16px; border-radius: 8px; max-width: 360px;">
                <div style="text-align: center; border-bottom: 1px dashed #000; padding-bottom: 10px;">
                    <b style="font-size: 15px;">APOTEK VETERAN SEHAT BLITAR</b><br>
                    Jl. Veteran no 64B Blitar Kota<br> 
                    (Sebelah Gang Srigading)<br> 
                    Blitar 66111<br>
                    <b>081331808585</b>
                </div>
                <div style="margin: 10px 0; font-size: 12px;">
                    {tgl_nota}<br>
                    -------------------------------------
                </div>
                {items_html}
                <div style="border-top: 1px dashed #000; margin-top: 10px; padding-top: 5px;">
                    <div style='display: flex; justify-content: space-between;'><b>Total</b> <b>{format_rupiah(total_belanja)}</b></div>
                    <div style='display: flex; justify-content: space-between;'>Bayar <span>{format_rupiah(bayar_tunai)}</span></div>
                    <div style='display: flex; justify-content: space-between;'>Kembali <span>{format_rupiah(max(0, kembali))}</span></div>
                </div>
                <div style="text-align: center; margin-top: 20px; font-size: 10px;">
                    - Belanja tanpa struk/nota gratis -<br>
                    - Harga sudah termasuk PPN -
                </div>
            </div>
            """
            st.markdown(nota_html, unsafe_allow_html=True)

            st.markdown("")
            if st.session_state.nota_confirmed:
                col_simpan, col_reset = st.columns(2)
                with col_simpan:
                    if st.button("💾 Simpan & Update Stok", type="primary", use_container_width=True):
                        workbook_data = st.session_state.inventory_data_cache
                        
                        df_history = load_data()
                        if df_history is None:
                            df_history = pd.DataFrame(columns=KOLOM_WAJIB)
                            
                        new_history_rows = []
                        
                        for item in st.session_state.cart:
                            ws_target = item["worksheet"]
                            if ws_target in workbook_data:
                                sheet_df = prepare_sheet_for_editor(workbook_data[ws_target].copy())
                                
                                mask = (
                                    (sheet_df["Nama produk"].fillna("").astype(str) == str(item["nama"])) &
                                    (sheet_df["Nomor Batch"].fillna("").astype(str) == str(item["batch"]))
                                )
                                
                                if mask.any():
                                    idx = sheet_df[mask].index[-1]
                                    sisa_lama = float(sheet_df.loc[idx, "Stok Sisa"]) if pd.notna(sheet_df.loc[idx, "Stok Sisa"]) else 0.0
                                    keluar_lama = float(sheet_df.loc[idx, "Stok Keluar"]) if pd.notna(sheet_df.loc[idx, "Stok Keluar"]) else 0.0
                                    
                                    sisa_baru = max(sisa_lama - item["qty"], 0)
                                    keluar_baru = keluar_lama + item["qty"]
                                    
                                    sheet_df.loc[idx, "Stok Sisa"] = sisa_baru
                                    sheet_df.loc[idx, "Stok Keluar"] = keluar_baru
                                    
                                    workbook_data[ws_target] = normalize_inventory_df(sheet_df)
                            
                            new_history_rows.append({
                                "Tanggal": pd.Timestamp(date.today()),
                                "Nama Obat": item["nama"],
                                "Kategori": ws_target, 
                                "Satuan": item["satuan_jual"],
                                "Stok Masuk": 0,
                                "Stok Keluar": item["qty"],
                                "Stok Akhir": sisa_baru if 'sisa_baru' in locals() else 0,
                                "Harga Satuan (Rp)": item["harga_per_satuan"],
                                "Total Nilai (Rp)": item["subtotal"],
                                "Tanggal Kadaluarsa": pd.Timestamp(item["tgl_exp"]) if pd.notna(item["tgl_exp"]) else pd.Timestamp(date.today()),
                                "Keterangan": f"Kasir Pembelian Obat ({item['skema_harga']})"
                            })
                            
                        if new_history_rows:
                            df_history = pd.concat([df_history, pd.DataFrame(new_history_rows)], ignore_index=True)
                            save_data(df_history)
                            
                        st.session_state.inventory_data_cache = workbook_data
                        save_inventory_workbook(workbook_data)
                        
                        # LOGIC SHIFT : Akumulasi otomatis hasil penjualan dari sistem 
                        if st.session_state.shift_active:
                            st.session_state.active_shift_context["accumulated_sales_expected"] += total_belanja
                        
                        st.session_state.cart = []
                        st.session_state.checkout_mode = False
                        st.session_state.bayar_tunai = 0
                        st.session_state.nota_confirmed = False
                        st.success("✅ Transaksi berhasil disimpan! Stok Excel dan Saldo Shift sudah diperbarui secara real-time.")
                        st.rerun()
                with col_reset:
                    if st.button("🗑️ Kosongkan Keranjang", type="secondary", use_container_width=True):
                        st.session_state.cart = []
                        st.session_state.checkout_mode = False
                        st.session_state.bayar_tunai = 0
                        st.session_state.nota_confirmed = False
                        st.rerun()
            else:
                if st.button("🗑️ Kosongkan Keranjang", type="secondary"):
                    st.session_state.cart = []
                    st.session_state.checkout_mode = False
                    st.session_state.bayar_tunai = 0
                    st.session_state.nota_confirmed = False
                    st.rerun()

        else:
            st.info("Keranjang kosong. Tambahkan obat dari form di sebelah kiri.")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR BERSAMA — ENTRI & RETUR PEMBELIAN
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📦 Entri & Retur Pembelian":
    st.markdown(
        "<h2 style='text-align: center; color: #333333;'>Entri & Retur Pembelian Obat</h2>",
        unsafe_allow_html=True
    )
    st.write("---")

    tab_retur, tab_entri = st.tabs(["🏥 Retur Pembelian", "🛍️ Entri Pembelian"])

    with tab_retur:
        st.markdown(
            """
            <div class='app-header'>
                <div class='app-title'>🏥 Retur Pembelian Obat</div>
                <div class='app-subtitle'>Pilih produk dari worksheet yang sudah diupload, lalu buat retur sesuai stok real-time.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if "inventory_data_cache" not in st.session_state or not st.session_state.inventory_data_cache:
            st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu di menu **📋 Tampilkan Dan Ubah Stok Obat**.")
            st.stop()

        workbook_data = st.session_state.inventory_data_cache
        sheet_name = st.selectbox("Pilih Worksheet", INVENTORY_SHEETS, index=0, key="retur_selected_sheet")
        if sheet_name not in workbook_data:
            st.warning(f"Worksheet **{sheet_name}** belum ada di dataset yang sedang aktif.")
            st.stop()

        sheet_df = prepare_sheet_for_editor(workbook_data[sheet_name].copy())
        sheet_df = sheet_df.sort_values(["Nama produk", "Nomor Batch"], na_position="last").reset_index(drop=True)

        col_meta_a, col_meta_b, col_meta_c = st.columns(3)
        with col_meta_a:
            st.metric("Worksheet Aktif", sheet_name)
        with col_meta_b:
            st.metric("Jumlah Baris", len(sheet_df))
        with col_meta_c:
            st.metric("Total Stok Sisa", int(sheet_df["Stok Sisa"].fillna(0).sum()))

        st.markdown("---")
        search_text = st.text_input("🔍 Cari Data Retur (Nama Produk, Batch, Faktur, PBF, dll)", placeholder="Ketik kata kunci pencarian...", key="retur_search_input")

        if search_text.strip():
            mask = sheet_df.astype(str).apply(lambda col: col.str.contains(search_text.strip(), case=False, na=False)).any(axis=1)
            filtered_df = sheet_df[mask].copy()
        else:
            filtered_df = sheet_df.copy()

        if filtered_df.empty:
            st.info("Data pada worksheet ini belum cocok dengan kata kunci yang Anda cari.")
            st.stop()

        st.subheader("📦 Pilih Produk untuk Retur")
        st.dataframe(
            filtered_df[["Nama produk", "Nomor Batch", "Satuan", "Tanggal Kadaluwarsa", "Stok Sisa", "Harga 1", "Keterangan"]].copy(),
            use_container_width=True,
            hide_index=True,
            height=260
        )

        product_options = filtered_df["Nama produk"].fillna("").astype(str).drop_duplicates().tolist()
        selected_product = st.selectbox("Pilih Produk", product_options, key="retur_product_select")
        product_rows = filtered_df[filtered_df["Nama produk"].fillna("").astype(str).str.lower() == selected_product.lower()].copy()
        selected_batch = st.selectbox(
            "Pilih Nomor Batch",
            product_rows["Nomor Batch"].fillna("-").astype(str).drop_duplicates().tolist(),
            key="retur_batch_select"
        )
        selected_row = product_rows[product_rows["Nomor Batch"].fillna("-").astype(str) == selected_batch].iloc[0]

        with st.form("form_retur_entry"):
            qty_retur = st.number_input(
                "Jumlah Retur (unit)",
                min_value=0.0,
                step=1.0,
                value=0.0,
                key="qty_retur_input"
            )
            selected_keterangan = sanitize_excel_value(selected_row["Keterangan"]) if "Keterangan" in selected_row.index else None
            keterangan_retur = st.text_area(
                "Keterangan Retur",
                value="" if selected_keterangan is None else str(selected_keterangan),
                placeholder="Masukkan alasan retur / catatan tambahan",
                height=90,
                key="keterangan_retur_input"
            )

            add_retur = st.form_submit_button("➕ Tambahkan ke Daftar Retur", type="primary")
            if add_retur:
                if qty_retur <= 0:
                    st.warning("Jumlah retur harus lebih dari 0.")
                else:
                    new_item = {
                        "Nama produk": selected_row["Nama produk"],
                        "Satuan": selected_row["Satuan"],
                        "Nomor Batch": selected_batch,
                        "Tanggal Kadaluwarsa": selected_row["Tanggal Kadaluwarsa"],
                        "Stok Sisa": float(selected_row["Stok Sisa"] if pd.notna(selected_row["Stok Sisa"]) else 0),
                        "Jumlah Retur": float(qty_retur),
                        "Harga 1": float(selected_row["Harga 1"] if pd.notna(selected_row["Harga 1"]) else 0),
                        "Keterangan": keterangan_retur
                    }
                    st.session_state.retur_items = pd.concat(
                        [st.session_state.retur_items, pd.DataFrame([new_item])],
                        ignore_index=True
                    )
                    st.success(f"Produk **{selected_product}** berhasil ditambahkan ke daftar retur.")
                    st.rerun()

        st.markdown("---")
        st.subheader("🧾 Daftar Item Retur")

        if st.session_state.retur_items.empty:
            st.info("Belum ada item retur. Pilih produk di panel atas untuk menambah daftar retur.")
            edited_df = st.session_state.retur_items
        else:
            edited_df = st.data_editor(
                st.session_state.retur_items,
                use_container_width=True,
                num_rows="dynamic",
                hide_index=True,
                column_config={
                    "Nama produk": st.column_config.TextColumn("Nama Produk", disabled=True, width="large"),
                    "Satuan": st.column_config.TextColumn("Satuan", disabled=True, width="small"),
                    "Nomor Batch": st.column_config.TextColumn("Nomor Batch", disabled=True, width="medium"),
                    "Tanggal Kadaluwarsa": st.column_config.DateColumn("Tanggal Kadaluwarsa", format="YYYY-MM-DD", disabled=True, width="medium"),
                    "Stok Sisa": st.column_config.NumberColumn("Stok Sisa", disabled=True, width="small"),
                    "Jumlah Retur": st.column_config.NumberColumn("Jumlah Retur", min_value=0.0, step=1.0, width="small"),
                    "Harga 1": st.column_config.NumberColumn("Harga 1", disabled=True, width="small"),
                    "Keterangan": st.column_config.TextColumn("Keterangan", width="large"),
                },
                key="data_editor_retur"
            )
            st.session_state.retur_items = edited_df

        total_retur = float((edited_df["Jumlah Retur"].fillna(0) * edited_df["Harga 1"].fillna(0)).sum()) if not edited_df.empty else 0.0

        col_save, col_reset = st.columns([1, 1])
        with col_save:
            if st.button("💾 Simpan Retur ke Worksheet", type="primary", use_container_width=True):
                if edited_df.empty or edited_df["Jumlah Retur"].fillna(0).sum() <= 0:
                    st.warning("Daftar retur masih kosong atau belum ada jumlah retur yang valid.")
                else:
                    workbook_data = st.session_state.inventory_data_cache
                    if sheet_name not in workbook_data:
                        st.error("Worksheet aktif tidak tersedia di data session.")
                    else:
                        active_df = workbook_data[sheet_name].copy()
                        active_df = prepare_sheet_for_editor(active_df)
                        for _, item in edited_df.iterrows():
                            qty_retur_item = float(item["Jumlah Retur"] or 0)
                            if qty_retur_item <= 0:
                                continue
                            mask = (
                                (active_df["Nama produk"].fillna("").astype(str).str.lower() == str(item["Nama produk"]).strip().lower()) &
                                (active_df["Nomor Batch"].fillna("").astype(str).str.lower() == str(item["Nomor Batch"]).strip().lower())
                            )
                            if not mask.any():
                                continue
                            idx = active_df[mask].index[-1]
                            stok_sisa_lama = float(active_df.loc[idx, "Stok Sisa"] if pd.notna(active_df.loc[idx, "Stok Sisa"]) else 0)
                            stok_baru = max(stok_sisa_lama - qty_retur_item, 0)
                            active_df.loc[idx, "Stok Sisa"] = stok_baru
                            active_df.loc[idx, "Stok Keluar"] = float(active_df.loc[idx, "Stok Keluar"] if pd.notna(active_df.loc[idx, "Stok Keluar"]) else 0) + qty_retur_item
                            active_df.loc[idx, "Keterangan"] = str(item["Keterangan"] or "") or active_df.loc[idx, "Keterangan"]

                        workbook_data[sheet_name] = normalize_inventory_df(active_df)
                        st.session_state.inventory_data_cache = workbook_data
                        save_inventory_workbook(workbook_data)

                        history_row = pd.DataFrame([{
                            "Nomor Faktur": str(selected_batch),
                            "Tanggal Retur": pd.Timestamp(date.today()),
                            "Jumlah Item": int(len(edited_df[edited_df["Jumlah Retur"].fillna(0) > 0])),
                            "Total Nilai Retur": total_retur,
                            "Tanggal Disimpan": datetime.now()
                        }])
                        st.session_state.retur_history = pd.concat([st.session_state.retur_history, history_row], ignore_index=True)
                        save_retur_history(st.session_state.retur_history)

                        st.success("✅ Retur berhasil disimpan ke worksheet aktif dan tercatat di riwayat retur.")
                        st.session_state.retur_items = pd.DataFrame(columns=st.session_state.retur_items.columns)
                        st.rerun()
        with col_reset:
            if st.button("🔄 Reset Daftar Retur", type="secondary", use_container_width=True):
                st.session_state.retur_items = pd.DataFrame(columns=st.session_state.retur_items.columns)
                st.rerun()

        st.markdown("---")
        st.subheader("📜 Riwayat Retur")
        if st.session_state.retur_history.empty:
            st.info("Belum ada riwayat retur. Setelah Anda menyimpan retur, riwayat akan tampil di sini.")
        else:
            history_display = st.session_state.retur_history.copy()
            history_display["Tanggal Retur"] = pd.to_datetime(history_display["Tanggal Retur"]).dt.strftime("%d-%m-%Y")
            history_display["Tanggal Disimpan"] = pd.to_datetime(history_display["Tanggal Disimpan"]).dt.strftime("%d-%m-%Y %H:%M")
            history_display["Total Nilai Retur"] = history_display["Total Nilai Retur"].apply(lambda x: f"Rp {x:,.2f}".replace(",", "."))
            st.dataframe(history_display, use_container_width=True, hide_index=True)


    with tab_entri:
        st.markdown(
            """
            <div class='app-header'>
                <div class='app-title'>🛍️ Entri Pembelian Obat</div>
                <div class='app-subtitle'>Catat pembelian secara ringkas, dan simpan langsung ke worksheet DatasetObat_ApotekVeteran.xlsx.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if "inventory_data_cache" not in st.session_state or not st.session_state.inventory_data_cache:
            st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu di menu **📋 Tampilkan Dan Ubah Stok Obat**.")
            st.stop()
            
        st.caption("Pencarian obat dilakukan dari seluruh worksheet. Entri pembelian ini akan langsung menambah riwayat pada worksheet tujuan masing-masing.")
        no_faktur = st.text_input("No. Faktur Pembelian", key="no_faktur_pembelian")
        pbf_default = st.text_input("PBF (Distributor) Default", key="pbf_pembelian")
        
        all_items_df = build_inventory_print_dataframe()
        
        cari_obat_input = st.text_input(
            label="🔍 Pencarian Produk (Semua Data: Nama, Batch, Faktur, dll)",
            placeholder="Ketik kata kunci pencarian...",
            key="cari_obat_pembelian_input"
        )
        
        if cari_obat_input.strip() and all_items_df is not None and not all_items_df.empty:
            mask = all_items_df.astype(str).apply(lambda col: col.str.contains(cari_obat_input.strip(), case=False, na=False)).any(axis=1)
            hasil = all_items_df[mask]
            
            if not hasil.empty:
                st.success(f"Ditemukan {len(hasil)} entri. Pilih salah satu baris di bawah, lalu klik Tambahkan:")
                
                tabel_cari_df = hasil[["Worksheet", "Nama produk", "Satuan", "Harga 1", "Stok Sisa"]].drop_duplicates(subset=["Worksheet", "Nama produk"]).reset_index(drop=True)
                
                event_beli = st.dataframe(
                    tabel_cari_df,
                    use_container_width=True,
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row",
                    key="table_hasil_pencarian_pembelian"
                )
                
                if event_beli.selection.rows:
                    idx = event_beli.selection.rows[0]
                    selected_row = tabel_cari_df.iloc[idx]
                    
                    if st.button(f"➕ Tambahkan '{selected_row['Nama produk']}' ke Tabel Pembelian", key="tambah_ke_pembelian"):
                        new_row = {
                            "No.": len(st.session_state.df_beli) + 1,
                            "Worksheet": selected_row["Worksheet"],
                            "Nama produk": selected_row["Nama produk"],
                            "Satuan": selected_row["Satuan"],
                            "Nomor Batch": "",
                            "Tanggal Kadaluwarsa": pd.Timestamp(date.today() + pd.Timedelta(days=365)),
                            "Stok Masuk": 0.0,
                            "Harga 1": float(selected_row["Harga 1"]) if pd.notna(selected_row["Harga 1"]) else 0.0,
                            "Harga 2": 0.0,
                            "Keterangan": ""
                        }
                        
                        df_existing = st.session_state.df_beli
                        if len(df_existing) == 1 and not str(df_existing.iloc[0]["Nama produk"]).strip():
                            st.session_state.df_beli = pd.DataFrame([new_row])
                        else:
                            st.session_state.df_beli = pd.concat([df_existing, pd.DataFrame([new_row])], ignore_index=True)
                        st.success(f"{selected_row['Nama produk']} ditambahkan ke tabel pembelian!")
                        st.rerun()

        st.markdown("---")
        st.subheader("📦 Rincian Item Pembelian")
        st.caption("Pilih worksheet tujuan. Stok baru akan dicatat sebagai entri baru yang menambah ketersediaan stok Anda di Dataset.")

        if "df_beli" not in st.session_state:
            st.session_state.df_beli = pd.DataFrame([
                {
                    "No.": 1,
                    "Worksheet": "TAB",
                    "Nama produk": "",
                    "Satuan": "TAB",
                    "Nomor Batch": "",
                    "Tanggal Kadaluwarsa": pd.Timestamp(date.today()),
                    "Stok Masuk": 0.0,
                    "Harga 1": 0.0,
                    "Harga 2": 0.0,
                    "Keterangan": ""
                }
            ])
            
        edited_df = st.data_editor(
            st.session_state.df_beli,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "No.": st.column_config.NumberColumn("No.", disabled=True, width="small"),
                "Worksheet": st.column_config.SelectboxColumn("Worksheet Tujuan", options=INVENTORY_SHEETS, width="small", required=True),
                "Nama produk": st.column_config.TextColumn("Nama Produk", width="large", required=True),
                "Satuan": st.column_config.TextColumn("Satuan", width="small"),
                "Nomor Batch": st.column_config.TextColumn("Batch", width="small"),
                "Tanggal Kadaluwarsa": st.column_config.DateColumn("Exp Date", format="YYYY-MM-DD"),
                "Stok Masuk": st.column_config.NumberColumn("Stok Masuk", min_value=0.0, width="small"),
                "Harga 1": st.column_config.NumberColumn("Harga 1", min_value=0.0, width="medium"),
                "Harga 2": st.column_config.NumberColumn("Harga 2", min_value=0.0, width="medium"),
                "Keterangan": st.column_config.TextColumn("Keterangan", width="medium"),
            },
            key="df_beli_editor"
        )
        
        edited_df["No."] = range(1, len(edited_df) + 1)
        st.session_state.df_beli = edited_df
        
        col_simpan_beli, col_reset_beli = st.columns([1, 1])
        with col_simpan_beli:
            if st.button("💾 Simpan Pembelian ke Excel Dataset", type="primary", use_container_width=True):
                if edited_df.empty or not edited_df["Nama produk"].astype(str).str.strip().any():
                    st.warning("Tabel pembelian kosong atau nama produk belum diisi.")
                else:
                    workbook_data = st.session_state.inventory_data_cache
                    jumlah_disimpan = 0
                    
                    for _, row in edited_df.iterrows():
                        nama = str(row["Nama produk"]).strip()
                        stok_masuk = float(row["Stok Masuk"]) if pd.notna(row["Stok Masuk"]) else 0
                        ws_target = str(row["Worksheet"])
                        
                        if not nama or stok_masuk <= 0 or ws_target not in workbook_data:
                            continue
                            
                        sheet_df = prepare_sheet_for_editor(workbook_data[ws_target].copy())
                        
                        new_buy = {
                            "Nama produk": nama,
                            "Satuan": row["Satuan"],
                            "Tanggal": pd.Timestamp(date.today()),
                            "Nomor Faktur": no_faktur,
                            "Nomor Batch": row["Nomor Batch"],
                            "PBF": pbf_default,
                            "Tanggal Kadaluwarsa": pd.Timestamp(row["Tanggal Kadaluwarsa"]),
                            "Stok Masuk": stok_masuk,
                            "Stok Keluar": 0.0,
                            "Stok Sisa": stok_masuk,
                            "Harga 1": float(row["Harga 1"]) if pd.notna(row["Harga 1"]) else 0.0,
                            "Harga 2": float(row["Harga 2"]) if pd.notna(row["Harga 2"]) else 0.0,
                            "Keterangan": row["Keterangan"]
                        }
                        
                        sheet_df = pd.concat([sheet_df, pd.DataFrame([new_buy])], ignore_index=True)
                        workbook_data[ws_target] = normalize_inventory_df(sheet_df)
                        jumlah_disimpan += 1
                        
                    if jumlah_disimpan > 0:
                        st.session_state.inventory_data_cache = workbook_data
                        save_inventory_workbook(workbook_data)
                        
                        st.session_state.df_beli = pd.DataFrame([
                            {
                                "No.": 1,
                                "Worksheet": "TAB",
                                "Nama produk": "",
                                "Satuan": "",
                                "Nomor Batch": "",
                                "Tanggal Kadaluwarsa": pd.Timestamp(date.today()),
                                "Stok Masuk": 0.0,
                                "Harga 1": 0.0,
                                "Harga 2": 0.0,
                                "Keterangan": ""
                            }
                        ])
                        st.success(f"✅ {jumlah_disimpan} entri pembelian berhasil disimpan langsung ke worksheet masing-masing!")
                        st.rerun()
                    else:
                        st.warning("Tidak ada item valid (Stok Masuk > 0) untuk disimpan.")

        with col_reset_beli:
            if st.button("🗑️ Reset Tabel Pembelian", type="secondary", use_container_width=True):
                st.session_state.df_beli = pd.DataFrame([
                    {
                        "No.": 1,
                        "Worksheet": "TAB",
                        "Nama produk": "",
                        "Satuan": "",
                        "Nomor Batch": "",
                        "Tanggal Kadaluwarsa": pd.Timestamp(date.today()),
                        "Stok Masuk": 0.0,
                        "Harga 1": 0.0,
                        "Harga 2": 0.0,
                        "Keterangan": ""
                    }
                ])
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# FITUR BARU — BUKA / TUTUP SHIFT KASIR
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🕒 Buka/Tutup Shift":

    def format_angka_erp(val):
        try:
            return f"{float(val):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return "0,00"

    def render_row_erp(label, val_num=0.0, disabled=True, widget="text", opts=None, val_str="", key_suffix=""):
        c1, c2 = st.columns([3, 7])
        k = f"ts_{key_suffix}_{re.sub(r'[^a-zA-Z0-9]', '_', label)}"
        with c1:
            st.markdown(f"<div style='text-align: right; padding-top: 8px; font-weight: 600; font-size: 13px; color: #e0e0e0;'>{label}</div>", unsafe_allow_html=True)
        with c2:
            if disabled:
                if widget == "number":
                    st.text_input(label, value=format_angka_erp(val_num), disabled=True, label_visibility="collapsed", key=k)
                    return val_num
                else:
                    st.text_input(label, value=val_str, disabled=True, label_visibility="collapsed", key=k)
                    return val_str
            else:
                if widget == "number":
                    # Disabled dilepas supaya bisa diedit kasir secara mandiri
                    return st.number_input(label, value=float(val_num), label_visibility="collapsed", key=k, step=1000.0, format="%.2f")
                elif widget == "select":
                    idx = 0
                    if opts and val_str in opts:
                        idx = opts.index(val_str)
                    return st.selectbox(label, options=opts, index=idx, label_visibility="collapsed", key=k)
                elif widget == "text":
                    return st.text_input(label, value=val_str, label_visibility="collapsed", key=k)

    # Logika filtering opsi kasir berdasarkan Role (Admin bisa melihat semua opsi)
    if st.session_state.role == "Admin":
        kasir_options = ["Ivonne", "Dian", "Julia"]
    else:
        kasir_options = ["Ivonne", "Dian", "Julia"]

    shift_options = ["Pagi", "Siang", "Sore", "Malam"]

    if not st.session_state.shift_active:
        st.markdown("<h2 style='text-align: center; margin-bottom: 40px; color: #e0e0e0;'>Buka Shift</h2>", unsafe_allow_html=True)
        st.info("Silakan masukkan saldo awal (modal uang receh/tunai di laci) sebelum mulai melayani penjualan.")
        
        default_name = USERS[st.session_state.username]["name"]
        default_str = default_name if default_name in kasir_options else kasir_options[0]

        with st.form("form_buka_shift"):
            nama_user_buka = render_row_erp("User Aktif (Nama Kasir)", disabled=False, widget="select", opts=kasir_options, val_str=default_str, key_suffix="buka")
            shift_pilih_buka = render_row_erp("Pilih Shift", disabled=False, widget="select", opts=shift_options, key_suffix="buka")
            saldo_awal_buka = render_row_erp("Saldo Awal", val_num=0.0, disabled=False, widget="number", key_suffix="buka")

            st.write("")
            c_btn1, c_btn2 = st.columns([3, 7])
            with c_btn2:
                col_b1, col_b2 = st.columns([1, 3])
                with col_b1:
                    submit_buka = st.form_submit_button("✔ Buka Shift", type="primary", use_container_width=True)

        if submit_buka:
            st.session_state.shift_active = True
            st.session_state.active_shift_context["saldo_awal"] = float(saldo_awal_buka)
            st.session_state.active_shift_context["accumulated_sales_expected"] = 0.0
            st.session_state.active_shift_context["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.active_shift_context["user_name"] = nama_user_buka
            st.session_state.active_shift_context["shift_name"] = shift_pilih_buka
            st.rerun()

    else:
        st.markdown("<h2 style='text-align: center; margin-bottom: 40px; color: #e0e0e0;'>Tutup Shift</h2>", unsafe_allow_html=True)

        nama_user = st.session_state.active_shift_context["user_name"]
        waktu_mulai = st.session_state.active_shift_context["start_time"]
        saldo_awal_context = st.session_state.active_shift_context["saldo_awal"]
        penjualan_sistem = st.session_state.active_shift_context["accumulated_sales_expected"]
        shift_context_name = st.session_state.active_shift_context.get("shift_name", "Pagi")

        retur_shift_default = 0.0
        if not st.session_state.retur_history.empty:
            df_retur = st.session_state.retur_history.copy()
            df_retur["Tanggal Disimpan"] = pd.to_datetime(df_retur["Tanggal Disimpan"], errors="coerce")
            waktu_mulai_dt = pd.to_datetime(waktu_mulai)
            mask_retur = df_retur["Tanggal Disimpan"] >= waktu_mulai_dt
            retur_shift_default = float(df_retur[mask_retur]["Total Nilai Retur"].sum())

        shift_in = render_row_erp("Pilih Shift", disabled=False, widget="select", opts=shift_options, val_str=shift_context_name, key_suffix="tutup")
        saldo_awal_in = render_row_erp("Saldo Awal", val_num=saldo_awal_context, disabled=False, widget="number", key_suffix="tutup")
        hasil_penjualan_in = render_row_erp("Hasil Penjualan Apotek", val_num=penjualan_sistem, disabled=False, widget="number", key_suffix="tutup")
        piutang_in = render_row_erp("Pembayaran Piutang Apotek", val_num=0.0, disabled=False, widget="number", key_suffix="tutup")
        pendapatan_jurnal_in = render_row_erp("Pendapatan Jurnal Keuangan Shift", val_num=0.0, disabled=False, widget="number", key_suffix="tutup")
        
        # LOGIC CALCULATION -> Total Pendapatan
        total_pendapatan_calc = hasil_penjualan_in + piutang_in + pendapatan_jurnal_in
        total_pendapatan_in = render_row_erp("Total Pendapatan", val_num=total_pendapatan_calc, disabled=False, widget="number", key_suffix="tutup")
        
        retur_penjualan_in = render_row_erp("Retur Penjualan Apotek", val_num=retur_shift_default, disabled=False, widget="number", key_suffix="tutup")
        pengeluaran_jurnal_in = render_row_erp("Pengeluaran Jurnal Keuangan Shift", val_num=0.0, disabled=False, widget="number", key_suffix="tutup")
        
        # LOGIC CALCULATION -> Total Pengeluaran
        total_pengeluaran_calc = retur_penjualan_in + pengeluaran_jurnal_in
        total_pengeluaran_in = render_row_erp("Total Pengeluaran", val_num=total_pengeluaran_calc, disabled=False, widget="number", key_suffix="tutup")
        
        # LOGIC CALCULATION -> Saldo Akhir
        saldo_akhir_calc = saldo_awal_in + total_pendapatan_in - total_pengeluaran_in
        saldo_akhir_in = render_row_erp("Saldo Akhir", val_num=saldo_akhir_calc, disabled=False, widget="number", key_suffix="tutup")
        
        saldo_kasir_in = render_row_erp("Saldo Kasir", val_num=0.0, disabled=False, widget="number", key_suffix="tutup")
        
        # LOGIC CALCULATION -> Selisih Saldo
        selisih_calc = saldo_kasir_in - saldo_akhir_in
        selisih_in = render_row_erp("Selisih Saldo", val_num=selisih_calc, disabled=False, widget="number", key_suffix="tutup")
        
        diserahkan_kepada_opsi = ["Ivonne", "Dian", "Julia"]
        diserahkan_kepada = render_row_erp("Di Serahkan Kepada", disabled=False, widget="select", opts=diserahkan_kepada_opsi, key_suffix="tutup")
        
        nama_penyerah = render_row_erp("Nama", disabled=False, widget="select", opts=kasir_options, val_str=nama_user, key_suffix="tutup")
        catatan = render_row_erp("Catatan", disabled=False, widget="text", key_suffix="tutup")

        st.markdown("---")
        st.markdown("#### ⚖️ Pengecekan Balance Saldo")
        if selisih_in < 0:
            st.error(f"⚠️ Peringatan: Terdapat Selisih Saldo (Minus) sebesar {format_rupiah(selisih_in)}. Cek kembali nominal di atas atau tambahkan catatan.")
        elif selisih_in > 0:
            st.warning(f"⚠️ Perhatian: Terdapat Selisih Saldo (Lebih) sebesar {format_rupiah(selisih_in)}. Cek kembali nominal di atas atau tambahkan catatan.")
        else:
            st.success(f"✅ Saldo Balance! Tidak ada selisih (Rp 0). Data siap diproses.")

        c1, c2 = st.columns([3, 7])
        with c2:
            st.markdown(
                "<div style='font-size: 12px; color: #a0a0a0; padding-top: 4px;'>"
                "Apabila ada <b>selisih saldo shift</b>, silakan isi kolom catatan untuk memberi penjelasan ke Admin agar tidak terjadi salah paham."
                "</div>", unsafe_allow_html=True
            )

        st.write("")
        st.write("")
        
        c_btn1, c_btn2 = st.columns([3, 7])
        with c_btn2:
            col_b1, col_b2 = st.columns([1, 4])
            with col_b1:
                submit_tutup = st.button("✔ Proses", type="primary", use_container_width=True)

        if submit_tutup:
            log_df = load_shift_log()
            new_log = pd.DataFrame([{
                "Waktu Buka": waktu_mulai,
                "Waktu Tutup": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Shift": shift_in,
                "Nama Kasir": nama_user,
                "Saldo Awal": saldo_awal_in,
                "Hasil Penjualan": hasil_penjualan_in,
                "Piutang": piutang_in,
                "Pendapatan Jurnal": pendapatan_jurnal_in,
                "Total Pendapatan": total_pendapatan_in,
                "Retur Penjualan": retur_penjualan_in,
                "Pengeluaran Jurnal": pengeluaran_jurnal_in,
                "Total Pengeluaran": total_pengeluaran_in,
                "Saldo Akhir": saldo_akhir_in,
                "Fisik Kasir": saldo_kasir_in,
                "Selisih": selisih_in,
                "Diserahkan Ke": diserahkan_kepada,
                "Nama Penyerah": nama_penyerah,
                "Catatan": catatan
            }])
            log_df = pd.concat([log_df, new_log], ignore_index=True)
            save_shift_log(log_df)

            st.session_state.shift_active = False
            st.session_state.active_shift_context = {
                "saldo_awal": 0.0,
                "accumulated_sales_expected": 0.0,
                "start_time": None,
                "user_name": "",
                "shift_name": "Pagi"
            }
            st.success("✅ Shift berhasil ditutup. Data tercatat dengan formal di database shift_log.csv.")
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("© Apotek Veteran Blitar")
