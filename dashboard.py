import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
import os

st.set_page_config(page_title="Apotek Veteran Blitar", layout="wide", page_icon="💊")

# ── CSS Custom untuk Menyesuaikan Tampilan ERP ─────────────────────────────────
# Perubahan ini dilakukan untuk:
# 1. Mengatur navbar maroon di bagian atas
# 2. Mengatur layout desktop dengan background putih
# 3. Menyesuaikan styling form, tombol, dan tabel sesuai referensi ERP
# 4. Menggunakan font Arial/Helvetica dengan ukuran yang tepat
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

# Database Master Obat
# Kolom untuk database obat dengan sistem multi harga (Harga Beli -> Harga Jual 1/2/3)
KOLOM_DATABASE_OBAT = [
    "id_obat",
    "nama_obat",
    "kategori",
    "satuan",

    # Multi Harga
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
    "Tanggal Kadaluarsa", "Supplier", "Keterangan"
]

RETUR_HISTORY_COLUMNS = [
    "Nomor Faktur", "Tanggal Retur",
    "Jumlah Item", "Total Nilai Retur", "Tanggal Disimpan"
]

def load_data():
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH, parse_dates=["Tanggal", "Tanggal Kadaluarsa"])
        return df
    return None

def load_retur_history():
    if os.path.exists(RETUR_HISTORY_PATH):
        df = pd.read_csv(RETUR_HISTORY_PATH, parse_dates=["Tanggal Retur", "Tanggal Disimpan"])
        return df
    return None

def save_data(df):
    df.to_csv(DATASET_PATH, index=False)

def save_retur_history(df):
    df.to_csv(RETUR_HISTORY_PATH, index=False)

def format_rupiah(val):
    try:
        return f"Rp {int(val):,}".replace(",", ".")
    except:
        return val

def cari_obat(keyword):
    """
    Mencari obat berdasarkan kode maupun nama.
    """

    if keyword.strip() == "":
        return pd.DataFrame()

    df = st.session_state.database_obat.copy()

    hasil = df[
        df["id_obat"].str.contains(keyword, case=False, na=False) |
        df["nama_obat"].str.contains(keyword, case=False, na=False)
    ]

    return hasil.reset_index(drop=True)

# ══════════════════════════════════════════════════════════════════════════════
# UTILITY: DIALOG TAMBAH OBAT BARU
# ══════════════════════════════════════════════════════════════════════════════
@st.dialog("➕ Tambah Obat Baru", width="large")
def tambah_obat_baru():
    st.write("Masukkan data obat baru yang belum ada di database:")
    
    col1, col2 = st.columns(2)
    with col1:
        new_id = st.text_input("Kode Obat *", placeholder="Contoh: OB003")
        new_name = st.text_input("Nama Obat *", placeholder="Contoh: Paracetamol 500mg")
        new_kategori = st.text_input("Kategori", placeholder="Contoh: Analgesik")
    with col2:
        new_satuan = st.text_input("Satuan", placeholder="Contoh: Tablet")
        new_tgl_exp = st.date_input(
            "Tanggal Kadaluarsa",
            value=date.today()
        )
    
    st.write("---")
    st.write("### Harga Obat")
    col_h0, col_h1, col_h2, col_h3 = st.columns(4)
    with col_h0:
        harga_beli = st.number_input(
            "Harga Beli",
            min_value=0,
            value=0
        )
    with col_h1:
        harga_1 = st.number_input(
            "Harga Jual 1",
            min_value=0,
            value=0
        )
    with col_h2:
        harga_2 = st.number_input(
            "Harga Jual 2",
            min_value=0,
            value=0
        )
    with col_h3:
        harga_3 = st.number_input(
            "Harga Jual 3",
            min_value=0,
            value=0
        )
    
    if st.button("💾 Simpan ke Database", type="primary", use_container_width=True):
        if new_id and new_name:
            new_data = {
                "id_obat": new_id,
                "nama_obat": new_name,
                "kategori": new_kategori if new_kategori else "Lainnya",
                "satuan": new_satuan if new_satuan else "Lainnya",

                "harga_beli": harga_beli,
                "harga_1": harga_1,
                "harga_2": harga_2,
                "harga_3": harga_3,

                "stok_akhir": 0,
                "tanggal_kadaluarsa": pd.Timestamp(new_tgl_exp)
            }
            st.session_state.database_obat = pd.concat(
                [st.session_state.database_obat, pd.DataFrame([new_data])],
                ignore_index=True
            )
            st.success(f"✅ Obat **{new_name}** berhasil ditambahkan!")
            st.rerun()
        else:
            st.error("❌ Kode Obat dan Nama Obat wajib diisi!")

# ══════════════════════════════════════════════════════════════════════════════
# AUTENTIKASI — LOGIN
# ══════════════════════════════════════════════════════════════════════════════
USERS = {
    "admin123@gmail.com": {"password": "admin123", "role": "Admin"},
    "kasir123@gmail.com": {"password": "kasir123", "role": "Kasir"},
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

# ── Session State untuk Retur Pembelian ─────────────────────────────────────
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

# ── Session State untuk Database Obat (Database Master Obat, multi harga) ───
if "database_obat" not in st.session_state:
    st.session_state.database_obat = pd.DataFrame([
        {
            "id_obat": "OB001",
            "nama_obat": "Paracetamol 500 mg",
            "kategori": "Analgesik",
            "satuan": "Tablet",

            "harga_beli": 4000,
            "harga_1": 5000,
            "harga_2": 4800,
            "harga_3": 4500,

            "stok_akhir": 100,
            "tanggal_kadaluarsa": "2027-12-31"
        },
        {
            "id_obat": "OB002",
            "nama_obat": "Amoxicillin 500 mg",
            "kategori": "Antibiotik",
            "satuan": "Kapsul",

            "harga_beli": 8500,
            "harga_1": 10000,
            "harga_2": 9500,
            "harga_3": 9000,

            "stok_akhir": 50,
            "tanggal_kadaluarsa": "2027-10-30"
        }
    ])

# ── Session State untuk Database Supplier ─────────────────────────────────────
if "database_supplier" not in st.session_state:
    st.session_state.database_supplier = ["PT. Sanbe Farma", "PT. Kalbe Farma", "PT. Kimia Farma", "PT. Indofarma", "PT. Ferron Farma"]

# ===============================
# SESSION STATE PEMBELIAN
# ===============================
if "hasil_pencarian" not in st.session_state:
    st.session_state.hasil_pencarian = pd.DataFrame()

if "item_pembelian" not in st.session_state:
    st.session_state.item_pembelian = pd.DataFrame()

if "selected_obat" not in st.session_state:
    st.session_state.selected_obat = None

if "obat_baru" not in st.session_state:
    st.session_state.obat_baru = False

# ── Sidebar navigasi ──────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/pharmacy-shop.png", width=80)
st.sidebar.title("💊 Apotek Veteran Blitar")
st.sidebar.markdown("---")

_role = st.session_state.role
st.sidebar.markdown(f"👤 **{st.session_state.username.capitalize()}** — *{_role}*")
st.sidebar.markdown("---")

if _role == "Admin":
    _menu_options = [
        "🏠 Beranda",
        "📋 Tampilkan Stok Obat Hari Ini",
        "✏️ Ubah Stok Obat Hari Ini",
        "🖨️ Cetak & Print Stok Obat",
        "🛒 Update Stok & Kasir",
        "🏥 Retur Pembelian",
        "🛍️ Entri Pembelian"
    ]
else:  # Kasir
    _menu_options = [
        "🏠 Beranda",
        "✏️ Ubah Stok Obat Hari Ini",
        "🛒 Update Stok & Kasir"
    ]

menu = st.sidebar.radio("Pilih Fitur", _menu_options, index=0)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.role      = None
    st.session_state.username  = ""
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# BERANDA
# ══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Beranda":
    st.title("💊 Dashboard Apotek Veteran Blitar")
    st.markdown("Selamat datang! Pilih fitur di sidebar untuk mulai mengelola stok obat.")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    df = load_data()
    if df is not None:
        col1.metric("Total Jenis Obat", df["Nama Obat"].nunique())
        col2.metric("Total Stok Tersedia", int(df.groupby("Nama Obat")["Stok Akhir"].last().sum()))
        exp_soon = df[df["Tanggal Kadaluarsa"] <= pd.Timestamp(date.today()) + pd.Timedelta(days=30)]
        col3.metric("⚠️ Hampir Kadaluarsa (≤30 hari)", exp_soon["Nama Obat"].nunique())
    else:
        st.info("Belum ada dataset. Silakan upload dataset di menu **Tampilkan Obat Hari Ini**.")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 1 — TAMPILKAN OBAT HARI INI
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "📋 Tampilkan Stok Obat Hari Ini":
    st.title("📋 Tampilkan Stok Obat")

    df = load_data()

    # Upload dataset (hanya muncul jika belum ada)
    if df is None:
        st.subheader("📂 Upload Dataset Stok Obat")
        st.info("Upload file CSV dataset stok obat. Setelah upload, fitur ini tidak akan muncul lagi.")
        uploaded = st.file_uploader("Pilih file CSV", type=["csv"])
        if uploaded:
            try:
                df_up = pd.read_csv(uploaded, parse_dates=["Tanggal", "Tanggal Kadaluarsa"])
                # Validasi kolom
                missing = [c for c in KOLOM_WAJIB if c not in df_up.columns]
                if missing:
                    st.error(f"Kolom berikut tidak ditemukan: {missing}")
                else:
                    save_data(df_up)
                    st.success("Dataset berhasil diupload dan disimpan!")
                    st.rerun()
            except Exception as e:
                st.error(f"Gagal membaca file: {e}")
        st.markdown("---")
        st.markdown("**Format kolom yang diperlukan:**")
        st.code(", ".join(KOLOM_WAJIB))
        st.stop()

    # ── Filter ────────────────────────────────────────────────────────────────
    st.subheader("🔍 Filter Data")
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        bulan_list = sorted(df["Tanggal"].dt.to_period("M").unique().astype(str).tolist(), reverse=True)
        bulan_sel = st.selectbox("Pilih Bulan", ["Semua"] + bulan_list)

    with col_f2:
        kategori_list = ["Semua"] + sorted(df["Kategori"].dropna().unique().tolist())
        kategori_sel = st.selectbox("Kategori Obat", kategori_list)

    with col_f3:
        cari = st.text_input("🔎 Cari Nama Obat")

    df_filtered = df.copy()
    if bulan_sel != "Semua":
        df_filtered = df_filtered[df_filtered["Tanggal"].dt.to_period("M").astype(str) == bulan_sel]
    if kategori_sel != "Semua":
        df_filtered = df_filtered[df_filtered["Kategori"] == kategori_sel]
    if cari:
        df_filtered = df_filtered[df_filtered["Nama Obat"].str.contains(cari, case=False, na=False)]

    # ── Ringkasan ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📊 Ringkasan")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jenis Obat", df_filtered["Nama Obat"].nunique())
    c2.metric("Total Stok Masuk", int(df_filtered["Stok Masuk"].sum()))
    c3.metric("Total Stok Keluar", int(df_filtered["Stok Keluar"].sum()))
    c4.metric("Total Stok Akhir", int(df_filtered["Stok Akhir"].sum()))

    # ── Peringatan kadaluarsa ─────────────────────────────────────────────────
    exp_df = df_filtered[df_filtered["Tanggal Kadaluarsa"] <= pd.Timestamp(date.today()) + pd.Timedelta(days=30)]
    if not exp_df.empty:
        st.warning(f"⚠️ {len(exp_df)} item mendekati/melewati tanggal kadaluarsa!")
        with st.expander("Lihat detail kadaluarsa"):
            st.dataframe(exp_df[["Nama Obat", "Kategori", "Stok Akhir", "Tanggal Kadaluarsa"]], use_container_width=True)

    # ── Tabel utama ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Data Stok Obat")

    display_df = df_filtered.copy()
    display_df["Tanggal"] = display_df["Tanggal"].dt.strftime("%d-%m-%Y")
    display_df["Tanggal Kadaluarsa"] = display_df["Tanggal Kadaluarsa"].dt.strftime("%d-%m-%Y")
    display_df["Harga Satuan (Rp)"] = display_df["Harga Satuan (Rp)"].apply(format_rupiah)
    display_df["Total Nilai (Rp)"] = display_df["Total Nilai (Rp)"].apply(format_rupiah)

    st.dataframe(display_df, use_container_width=True, height=450)
    st.caption(f"Menampilkan {len(df_filtered)} baris data")

    # Tombol reset dataset
    st.markdown("---")
    if st.button("🗑️ Hapus Dataset (Upload Ulang)", type="secondary"):
        if os.path.exists(DATASET_PATH):
            os.remove(DATASET_PATH)
            st.success("Dataset dihapus. Silakan upload ulang.")
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 2 — UBAH STOK OBAT HARI INI
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "✏️ Ubah Stok Obat Hari Ini":
    st.title("✏️ Ubah Stok Obat Hari Ini")

    df = load_data()
    if df is None:
        st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu di menu **Tampilkan Obat Hari Ini**.")
        st.stop()

    tab1, tab2 = st.tabs(["➕ Tambah / Update Transaksi", "🗑️ Hapus Baris Data"])

    # ── Tab 1: Tambah / Update ────────────────────────────────────────────────
    with tab1:
        st.subheader("Input Transaksi Stok Obat")
        st.info("Isi form di bawah untuk menambah transaksi stok masuk atau stok keluar. Data akan langsung tersimpan ke dataset.")

        with st.form("form_update_stok"):
            with st.container():
                fc1, fc2, fc3 = st.columns(3)
                with fc1:
                    tgl = st.date_input("Tanggal Transaksi", value=date.today())
                with fc2:
                    nama_obat = st.text_input("Nama Obat *", placeholder="Contoh: Paracetamol 500mg")
                with fc3:
                    harga_satuan = st.number_input("Harga Satuan (Rp)", min_value=0, value=0, step=500)

            with st.container():
                fc4, fc5, fc6 = st.columns(3)
                with fc4:
                    kategori = st.selectbox("Kategori", ["Analgesik", "Antibiotik", "Antasida", "Vitamin", "Antihistamin", "Antihipertensi", "Antidiabetes", "Lainnya"])
                with fc5:
                    satuan = st.selectbox("Satuan", ["Tablet", "Kapsul", "Botol", "Ampul", "Sachet", "Strip", "Tube", "Lainnya"])
                with fc6:
                    tgl_exp = st.date_input("Tanggal Kadaluarsa", value=date.today())

            with st.container():
                fc7, fc8, fc9 = st.columns(3)
                with fc7:
                    stok_masuk = st.number_input("Stok Masuk", min_value=0, value=0)
                with fc8:
                    stok_keluar = st.number_input("Stok Keluar (Terjual)", min_value=0, value=0)
                with fc9:
                    supplier = st.text_input("Supplier", placeholder="Nama distributor/supplier")

            keterangan = st.text_area("Keterangan", placeholder="Opsional", height=68)

            submitted = st.form_submit_button("💾 Simpan Transaksi", type="primary", use_container_width=True)

        if submitted:
            if not nama_obat.strip():
                st.error("Nama Obat wajib diisi!")
            else:
                # Hitung stok akhir berdasarkan riwayat obat yang sama
                prev = df[df["Nama Obat"].str.lower() == nama_obat.strip().lower()]
                stok_sebelumnya = int(prev["Stok Akhir"].iloc[-1]) if not prev.empty else 0
                stok_akhir = stok_sebelumnya + stok_masuk - stok_keluar
                total_nilai = stok_akhir * harga_satuan

                baris_baru = {
                    "Tanggal": pd.Timestamp(tgl),
                    "Nama Obat": nama_obat.strip(),
                    "Kategori": kategori,
                    "Satuan": satuan,
                    "Stok Masuk": stok_masuk,
                    "Stok Keluar": stok_keluar,
                    "Stok Akhir": max(stok_akhir, 0),
                    "Harga Satuan (Rp)": harga_satuan,
                    "Total Nilai (Rp)": total_nilai,
                    "Tanggal Kadaluarsa": pd.Timestamp(tgl_exp),
                    "Supplier": supplier,
                    "Keterangan": keterangan
                }
                df = pd.concat([df, pd.DataFrame([baris_baru])], ignore_index=True)
                save_data(df)
                st.success(f"✅ Transaksi untuk **{nama_obat}** berhasil disimpan! Stok akhir: **{max(stok_akhir,0)} {satuan}**")
                st.rerun()

    # ── Tab 2: Hapus baris ────────────────────────────────────────────────────
    with tab2:
        st.subheader("Hapus Baris Data")
        st.warning("Pilih baris yang ingin dihapus dari dataset.")

        df_show = df.copy()
        df_show.index.name = "ID Baris"
        df_show["Tanggal"] = df_show["Tanggal"].dt.strftime("%d-%m-%Y")
        df_show["Tanggal Kadaluarsa"] = df_show["Tanggal Kadaluarsa"].dt.strftime("%d-%m-%Y")
        st.dataframe(df_show, use_container_width=True, height=300)

        if "idx_hapus_val" not in st.session_state:
            st.session_state.idx_hapus_val = 0

        idx_hapus = st.number_input(
            "Masukkan ID Baris yang akan dihapus",
            min_value=0,
            max_value=max(len(df)-1, 0),
            key="idx_hapus_widget"
        )
        if st.button("🗑️ Hapus Baris", type="secondary"):
            target = st.session_state["idx_hapus_widget"]
            if target in df.index:
                df = df.drop(index=target).reset_index(drop=True)
                save_data(df)
                st.success(f"Baris ID {target} berhasil dihapus.")
                st.rerun()
            else:
                st.error(f"ID Baris {target} tidak ditemukan.")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 3 — CETAK & PRINT STOK OBAT
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🖨️ Cetak & Print Stok Obat":
    st.title("🖨️ Cetak & Print Stok Obat")

    df = load_data()
    if df is None:
        st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu di menu **Tampilkan Obat Hari Ini**.")
        st.stop()

    st.subheader("Pilih Opsi Cetak")
    opsi = st.radio("Opsi Data yang Dicetak", ["Semua Komponen Obat", "Sebagian Komponen Obat (Pilih Manual)"])

    # ── Filter tanggal ────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔍 Filter Sebelum Cetak")
    col_a, col_b = st.columns(2)
    with col_a:
        tgl_awal = st.date_input("Dari Tanggal", value=df["Tanggal"].min().date())
    with col_b:
        tgl_akhir = st.date_input("Sampai Tanggal", value=df["Tanggal"].max().date())

    df_print = df[(df["Tanggal"] >= pd.Timestamp(tgl_awal)) & (df["Tanggal"] <= pd.Timestamp(tgl_akhir))].copy()

    # ── Pilih kolom (jika sebagian) ───────────────────────────────────────────
    if opsi == "Sebagian Komponen Obat (Pilih Manual)":
        kolom_dipilih = st.multiselect(
            "Pilih Kolom yang Ingin Dicetak",
            options=df_print.columns.tolist(),
            default=["Tanggal", "Nama Obat", "Stok Masuk", "Stok Keluar", "Stok Akhir", "Harga Satuan (Rp)"]
        )
        if kolom_dipilih:
            df_print = df_print[kolom_dipilih]
        else:
            st.warning("Pilih minimal satu kolom.")
            st.stop()

    # ── Preview ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("👁️ Preview Data")
    preview_df = df_print.copy()
    if "Tanggal" in preview_df.columns:
        preview_df["Tanggal"] = preview_df["Tanggal"].dt.strftime("%d-%m-%Y")
    if "Tanggal Kadaluarsa" in preview_df.columns:
        preview_df["Tanggal Kadaluarsa"] = preview_df["Tanggal Kadaluarsa"].dt.strftime("%d-%m-%Y")
    if "Harga Satuan (Rp)" in preview_df.columns:
        preview_df["Harga Satuan (Rp)"] = preview_df["Harga Satuan (Rp)"].apply(format_rupiah)
    if "Total Nilai (Rp)" in preview_df.columns:
        preview_df["Total Nilai (Rp)"] = preview_df["Total Nilai (Rp)"].apply(format_rupiah)

    st.dataframe(preview_df, use_container_width=True, height=350)
    st.caption(f"{len(df_print)} baris data siap dicetak")

    # ── Unduhan ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("⬇️ Unduh File")
    col_d1, col_d2, col_d3 = st.columns(3)

    # CSV
    csv_buf = df_print.copy()
    if "Tanggal" in csv_buf.columns:
        csv_buf["Tanggal"] = csv_buf["Tanggal"].dt.strftime("%d-%m-%Y")
    if "Tanggal Kadaluarsa" in csv_buf.columns:
        csv_buf["Tanggal Kadaluarsa"] = csv_buf["Tanggal Kadaluarsa"].dt.strftime("%d-%m-%Y")
    csv_data = csv_buf.to_csv(index=False).encode("utf-8-sig")
    col_d1.download_button(
        label="📄 Unduh CSV",
        data=csv_data,
        file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.csv",
        mime="text/csv"
    )

    # Excel (XLSX)
    try:
        import openpyxl
        xlsx_buf = io.BytesIO()
        with pd.ExcelWriter(xlsx_buf, engine="openpyxl") as writer:
            excel_df = df_print.copy()
            if "Tanggal" in excel_df.columns:
                excel_df["Tanggal"] = excel_df["Tanggal"].dt.strftime("%d-%m-%Y")
            if "Tanggal Kadaluarsa" in excel_df.columns:
                excel_df["Tanggal Kadaluarsa"] = excel_df["Tanggal Kadaluarsa"].dt.strftime("%d-%m-%Y")
            excel_df.to_excel(writer, index=False, sheet_name="Stok Obat")
        col_d2.download_button(
            label="📊 Unduh Excel (XLSX)",
            data=xlsx_buf.getvalue(),
            file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ImportError:
        col_d2.info("Install `openpyxl` untuk ekspor Excel.")

    # PDF via HTML print
    col_d3.markdown("#### 🖨️ Print / PDF")
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
    col_d3.download_button(
        label="🖨️ Unduh HTML (Print/PDF)",
        data=html_bytes,
        file_name=f"stok_obat_{tgl_awal}_{tgl_akhir}.html",
        mime="text/html"
    )
    col_d3.caption("Buka file HTML → klik tombol Print → pilih 'Save as PDF'")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 4 — UPDATE STOK & KASIR
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🛒 Update Stok & Kasir":
    st.title("✏️ Kasir & Update Stok Obat")

    df = load_data()
    if df is None:
        st.warning("Dataset belum tersedia. Silakan upload dataset terlebih dahulu di menu **Tampilkan Obat Hari Ini**.")
        st.stop()

    # State untuk menyimpan keranjang belanja sementara
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

        if not st.session_state.checkout_mode:
            with st.form("form_kasir"):
                list_obat = df["Nama Obat"].unique().tolist()
                nama_obat = st.selectbox("Pilih Obat", list_obat)
                jumlah = st.number_input("Jumlah Beli", min_value=1, value=1)
                add_to_cart = st.form_submit_button("➕ Tambah ke Nota")

                if add_to_cart:
                    data_obat = df[df["Nama Obat"] == nama_obat].iloc[-1]
                    subtotal = data_obat["Harga Satuan (Rp)"] * jumlah
                    st.session_state.cart.append({
                        "nama": nama_obat,
                        "qty": jumlah,
                        "harga": data_obat["Harga Satuan (Rp)"],
                        "subtotal": subtotal,
                        "kategori": data_obat["Kategori"],
                        "satuan": data_obat["Satuan"],
                        "supplier": data_obat["Supplier"],
                        "tgl_exp": data_obat["Tanggal Kadaluarsa"]
                    })
                    st.success(f"{nama_obat} ditambah ke nota!")

            if st.session_state.cart:
                st.markdown("**🧾 Item dalam keranjang:**")
                for i, item in enumerate(st.session_state.cart):
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                    c1.write(f"{item['nama']}")
                    c2.write(f"x{item['qty']}")
                    c3.write(format_rupiah(item['subtotal']))
                    with c4:
                        col_min, col_del = st.columns(2)
                        with col_min:
                            if st.button("➖", key=f"min_{i}", help="Kurangi 1"):
                                if st.session_state.cart[i]["qty"] > 1:
                                    st.session_state.cart[i]["qty"] -= 1
                                    st.session_state.cart[i]["subtotal"] = (
                                        st.session_state.cart[i]["qty"] * st.session_state.cart[i]["harga"]
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

        # ── Jam real-time via JavaScript (terupdate setiap detik) ─────────────
        st.markdown(
            """
            <div style="font-family: monospace; font-size: 14px; margin-bottom: 8px;">
            </div>
            <script>
                function updateClock() {
                    const now = new Date();
                    const pad = n => String(n).padStart(2, '0');
                    const str = pad(now.getDate()) + '/' + pad(now.getMonth()+1) + '/' + now.getFullYear()
                              + ' ' + pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
                    const el = document.getElementById('realtime-clock');
                    if (el) el.textContent = str;
                }
                updateClock();
                setInterval(updateClock, 1000);
            </script>
            """,
            unsafe_allow_html=True
        )

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
                    <span style='flex: 1; text-align: center;'>{(item['harga'])}</span>
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
                        new_rows = []
                        for item in st.session_state.cart:
                            prev_stock = df[df["Nama Obat"] == item["nama"]]["Stok Akhir"].iloc[-1]
                            stok_baru = max(int(prev_stock) - item["qty"], 0)
                            new_rows.append({
                                "Tanggal": pd.Timestamp(date.today()),
                                "Nama Obat": item["nama"],
                                "Kategori": item["kategori"],
                                "Satuan": item["satuan"],
                                "Stok Masuk": 0,
                                "Stok Keluar": item["qty"],
                                "Stok Akhir": stok_baru,
                                "Harga Satuan (Rp)": item["harga"],
                                "Total Nilai (Rp)": stok_baru * item["harga"],
                                "Tanggal Kadaluarsa": item["tgl_exp"],
                                "Supplier": item["supplier"],
                                "Keterangan": "Penjualan Kasir"
                            })
                        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
                        save_data(df)
                        st.session_state.cart = []
                        st.session_state.checkout_mode = False
                        st.session_state.bayar_tunai = 0
                        st.session_state.nota_confirmed = False
                        st.success("✅ Transaksi berhasil disimpan!")
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

            # ── Unduh Nota HTML untuk Print ───────────────────────────────────
            st.markdown("---")
            nota_print_html = f"""
            <html><head>
            <meta charset='utf-8'>
            <title>Nota Apotek Veteran Blitar</title>
            <style>
              body {{ font-family: monospace; font-size: 12px; margin: 20px; width: 300px; }}
              .center {{ text-align: center; }}
              .row {{ display: flex; justify-content: space-between; }}
              .dashed {{ border-top: 1px dashed #000; margin: 8px 0; }}
              @media print {{ button {{ display: none; }} }}
            </style>
            </head><body>
            <div class="center">
              <b>APOTEK VETERAN SEHAT BLITAR</b><br>
              Jl. Veteran no 64B Blitar Kota<br> 
              (Sebelah Gang Srigading)<br> 
              Blitar 66111<br>
              <b>081331808585</b>
            </div>
            <div class="dashed"></div>
            <div id="tgl-nota"></div>
            <div class="dashed"></div>
            {items_html}
            <div class="dashed"></div>
            <div class="row"><b>Total</b><b>{format_rupiah(total_belanja)}</b></div>
            <div class="row"><span>Bayar</span><span>{format_rupiah(bayar_tunai)}</span></div>
            <div class="row"><span>Kembali</span><span>{format_rupiah(max(0, kembali))}</span></div>
            <div class="dashed"></div>
            <div class="center" style="font-size:10px;">
              - Belanja tanpa struk/nota gratis -<br>
              - Harga sudah termasuk PPN -
            </div>
            <br>
            <button onclick='window.print()' style='padding:6px 16px;background:#2c7be5;color:white;
              border:none;border-radius:4px;cursor:pointer;font-size:12px;'>🖨️ Print Nota</button>
            <script>
              (function() {{
                var now = new Date();
                var pad = function(n) {{ return String(n).padStart(2, '0'); }};
                var str = pad(now.getDate()) + '/' + pad(now.getMonth()+1) + '/' + now.getFullYear()
                        + ' ' + pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
                document.getElementById('tgl-nota').textContent = str;
              }})();
            </script>
            </body></html>
            """
            st.download_button(
                label="🖨️ Unduh & Print Nota",
                data=nota_print_html.encode("utf-8"),
                file_name=f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html"
            )
            st.caption("Buka file HTML di browser → klik tombol Print → cetak atau simpan sebagai PDF")
        else:
            st.info("Keranjang kosong. Tambahkan obat dari form di sebelah kiri.")

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 5 — RETUR PEMBELIAN
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🏥 Retur Pembelian":
    # ── Header Utama ─────────────────────────────────────────────────────────
    st.markdown(
        "<h2 style='text-align: center; color: #333333;'>Retur Pembelian Obat</h2>",
        unsafe_allow_html=True
    )
    st.write("---")

    # ── Form Input Utama (disederhanakan - fokus hanya pada retur barang) ─────
    col1, col2 = st.columns(2)

    with col1:
        no_faktur = st.text_input("No. Faktur", value="", placeholder="Contoh: 2605/PDF.CC/1501", key="no_faktur_input")
        tgl_faktur = st.text_input("Tanggal Faktur", value="", placeholder="Contoh: 15 Mei 2026", key="tgl_faktur_input")

    with col2:
        tgl_retur = st.date_input("Tanggal Retur", value=date.today(), key="tgl_retur_input")

    # ── Pencarian Obat dari Database Master Obat ───────────────────────────────
    st.markdown(
        """
        <div class='form-container'>
            <div class='form-section-title'>🔍 Cari Obat</div>
        """,
        unsafe_allow_html=True
    )

    cari_obat_input_retur = st.text_input(
        "Cari Nama Obat atau Kode Obat",
        placeholder="Ketik nama obat atau kode obat untuk mencari...",
        key="cari_obat_retur"
    )

    if cari_obat_input_retur.strip():
        hasil_cari = cari_obat(cari_obat_input_retur.strip())

        if not hasil_cari.empty:
            st.success(f"Ditemukan {len(hasil_cari)} obat:")
            event_retur = st.dataframe(
                hasil_cari[["nama_obat", "kategori", "satuan", "stok_akhir"]],
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="table_obat_selection_retur"
            )

            if event_retur.selection.rows:
                idx = event_retur.selection.rows[0]
                selected_row = hasil_cari.iloc[idx]
                if st.button(f"➕ Tambah '{selected_row['nama_obat']}' ke Tabel Retur", key="tambah_ke_retur"):
                    new_item = {
                        "Pilih": True,
                        "Kode": selected_row["id_obat"],
                        "Nama Obat": selected_row["nama_obat"],
                        "Satuan": selected_row["satuan"],
                        "No. Batch": "",
                        "Tanggal Exp": "",
                        "Ketentuan Retur": "",
                        "Maks bln sblm ED": 0,
                        "Tersedia": float(selected_row["stok_akhir"]),
                        "Jumlah Retur": 0.00,
                        "HPP": float(selected_row["harga_beli"]) if "harga_beli" in selected_row else 0.00
                    }
                    st.session_state.retur_items = pd.concat(
                        [st.session_state.retur_items, pd.DataFrame([new_item])],
                        ignore_index=True
                    ).reset_index(drop=True)
                    st.success(f"{selected_row['nama_obat']} ditambahkan ke tabel retur!")
                    st.rerun()
        else:
            st.warning("Obat tidak ditemukan di database.")

    if st.button("➕ Tambah Manual", key="btn_tambah_manual_key"):
        new_item = {
            "Pilih": True,
            "Kode": "",
            "Nama Obat": "",
            "Satuan": "",
            "No. Batch": "",
            "Tanggal Exp": "",
            "Ketentuan Retur": "",
            "Maks bln sblm ED": 0,
            "Tersedia": 0.00,
            "Jumlah Retur": 0.00,
            "HPP": 0.00
        }
        st.session_state.retur_items = pd.concat(
            [st.session_state.retur_items, pd.DataFrame([new_item])],
            ignore_index=True
        ).reset_index(drop=True)
        st.success("Item baru ditambahkan ke tabel retur!")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tabel Item yang Akan Diretur ──────────────────────────────────────────
    st.write("##")
    st.markdown("### 📦 Daftar Item Retur")

    if st.session_state.retur_items.empty:
        st.info("Belum ada item. Cari obat di atas lalu klik tombol tambah, atau gunakan Tambah Manual.")
        edited_df = st.session_state.retur_items
    else:
        edited_df = st.data_editor(
            st.session_state.retur_items,
            column_config={
                "Pilih": st.column_config.CheckboxColumn(
                    "Pilih",
                    help="Centang untuk memilih obat yang akan diretur",
                    default=False,
                ),
                "Jumlah Retur": st.column_config.NumberColumn(
                    "Jumlah Retur",
                    min_value=0.0,
                    step=1.0,
                    format="%.2f",
                ),
                "Kode": st.column_config.TextColumn(disabled=True),
                "Nama Obat": st.column_config.TextColumn(disabled=True),
                "Satuan": st.column_config.TextColumn(disabled=True),
                "Tersedia": st.column_config.NumberColumn(disabled=True, format="%.2f"),
                "HPP": st.column_config.NumberColumn(format="%.2f"),
            },
            disabled=["Kode", "Nama Obat", "Satuan", "Tersedia"],
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic",
            key="data_editor_retur"
        )
        st.session_state.retur_items = edited_df

    total_retur = float((edited_df["Jumlah Retur"] * edited_df["HPP"]).sum()) if not edited_df.empty else 0.0

    # ── Total & Tombol Aksi ────────────────────────────────────────────────────
    st.write("##")
    action_col, total_col = st.columns([3, 1])

    with action_col:
        btn_simpan, btn_reset, _ = st.columns([1, 1, 5])
        with btn_simpan:
            if st.button("💾 Simpan Retur", type="primary", use_container_width=True, key="btn_simpan_form"):
                if edited_df.empty or total_retur == 0:
                    st.warning("⚠️ Belum ada item dengan jumlah retur yang diisi!")
                else:
                    new_history = pd.DataFrame([{
                        "Nomor Faktur": no_faktur,
                        "Tanggal Retur": tgl_retur,
                        "Jumlah Item": len(edited_df[edited_df["Jumlah Retur"] > 0]),
                        "Total Nilai Retur": total_retur,
                        "Tanggal Disimpan": datetime.now()
                    }])

                    st.session_state.retur_history = pd.concat(
                        [st.session_state.retur_history, new_history],
                        ignore_index=True
                    )
                    save_retur_history(st.session_state.retur_history)

                    st.success(f"✅ Retur pembelian berhasil disimpan! Total retur: Rp {total_retur:,.2f}".replace(",", "."))

                    st.session_state.retur_items = pd.DataFrame(columns=st.session_state.retur_items.columns)
                    st.rerun()
        with btn_reset:
            if st.button("🔄 Reset", key="btn_reset_form", use_container_width=True):
                st.session_state.retur_items = pd.DataFrame(columns=st.session_state.retur_items.columns)
                st.rerun()

    with total_col:
        st.markdown(
            f"<h2 style='text-align: right; margin: 0; color: #4F4F4F;'>{format_rupiah(total_retur)}</h2>",
            unsafe_allow_html=True
        )

    st.write("---")

    # ── Tabel Riwayat Retur ──────────────────────────────────────────────────
    if not st.session_state.retur_history.empty:
        st.markdown(
            """
            <div class='table-container'>
                <div class='table-title'>📜 Riwayat Retur</div>
            """,
            unsafe_allow_html=True
        )

        history_display = st.session_state.retur_history.copy()
        history_display["Tanggal Retur"] = pd.to_datetime(history_display["Tanggal Retur"]).dt.strftime("%d-%m-%Y")
        history_display["Tanggal Disimpan"] = pd.to_datetime(history_display["Tanggal Disimpan"]).dt.strftime("%d-%m-%Y %H:%M")
        history_display["Total Nilai Retur"] = history_display["Total Nilai Retur"].apply(
            lambda x: f"Rp {x:,.2f}".replace(",", ".")
        )

        st.dataframe(history_display, use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class='app-footer'>
            <p>All Rights Reserved</p>
            <p style='color: #e94560; font-weight: 600;'>Vmedis 1.8.0</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# FITUR 5 — ENTRI PEMBELIAN
# ══════════════════════════════════════════════════════════════════════════════
elif menu == "🛍️ Entri Pembelian":
    st.markdown(
        """
        <div class='app-header'>
            <div class='app-title'>🛍️ Entri Pembelian Obat</div>
            <div class='app-subtitle'>Formulir pencatatan pembelian obat dari supplier</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Session state untuk tabel pembelian ──────────────────────────────────
    if "df_beli" not in st.session_state:
        st.session_state.df_beli = pd.DataFrame([
            {
                "No.": 1,
                "Nama Obat": "",
                "Jumlah": 0.0,
                "Satuan": "BOX",
                "Harga Beli": 0.0,
                "Harga Jual": 0.0,
                "Subtotal": 0.0,
                "Batch": "",
                "Tanggal Expired": pd.Timestamp(date.today())
            }
        ])

    # ── Baris 1: Informasi Faktur & Supplier ──────────────────────────────────
    st.markdown(
        """
        <div class='form-container'>
            <div class='form-section-title'>📋 Informasi Faktur & Supplier</div>
        """,
        unsafe_allow_html=True
    )
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        supplier_terpilih = st.selectbox(
            "Pilih Supplier",
            options=st.session_state.database_supplier,
            key="supplier_pembelian"
        )
    with col_f2:
        no_faktur = st.text_input("No. Faktur", key="no_faktur_pembelian")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Baris 2: Pencarian obat ───────────────────────────────────────────────
    st.markdown(
        """
        <div class='form-container'>
            <div class='form-section-title'>🔍 Cari Obat</div>
        """,
        unsafe_allow_html=True
    )
    st.caption("Ketik Nama Obat / Scan Barcode Obat...")
    col_cari, col_obat_baru = st.columns([5, 1])
    with col_cari:
        cari_obat_input = st.text_input(
            label="Pencarian Obat",
            placeholder="Ketik Nama Obat / Scan Barcode Obat...",
            label_visibility="collapsed",
            key="cari_obat_input"
        )
    with col_obat_baru:
        # Tombol pintasan untuk menambah obat baru
        if st.button("➕ Obat Baru", use_container_width=True, key="btn_obat_baru"):
            tambah_obat_baru()  # Panggil fungsi dialog

    # Hasil pencarian — dicari langsung dari Database Master Obat.
    # Klik baris pada tabel hasil, lalu tekan tombol "Tambahkan" untuk
    # otomatis mengisi baris baru di tabel Rincian Item Pembelian di bawah.
    if cari_obat_input.strip():
        hasil = cari_obat(cari_obat_input.strip())
        if not hasil.empty:
            st.success(f"{len(hasil)} obat ditemukan. Klik salah satu baris lalu tekan tombol Tambahkan:")
            event_beli = st.dataframe(
                hasil[["nama_obat", "kategori", "satuan", "harga_beli", "harga_1", "stok_akhir"]],
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="table_hasil_pencarian_pembelian"
            )

            if event_beli.selection.rows:
                idx = event_beli.selection.rows[0]
                selected_row = hasil.iloc[idx]
                if st.button(f"➕ Tambahkan '{selected_row['nama_obat']}' ke Tabel Pembelian", key="tambah_ke_pembelian"):
                    new_row = {
                        "No.": len(st.session_state.df_beli) + 1,
                        "Nama Obat": selected_row["nama_obat"],
                        "Jumlah": 0.0,
                        "Satuan": selected_row["satuan"] if selected_row["satuan"] else "BOX",
                        "Harga Beli": float(selected_row["harga_beli"]),
                        "Harga Jual": float(selected_row["harga_1"]),
                        "Subtotal": 0.0,
                        "Batch": "",
                        "Tanggal Expired": pd.Timestamp(selected_row["tanggal_kadaluarsa"]) if selected_row["tanggal_kadaluarsa"] else pd.Timestamp(date.today())
                    }
                    # Buang baris kosong pertama (baris default yang belum diisi) jika masih ada
                    df_existing = st.session_state.df_beli
                    if len(df_existing) == 1 and not str(df_existing.iloc[0]["Nama Obat"]).strip():
                        st.session_state.df_beli = pd.DataFrame([new_row])
                    else:
                        st.session_state.df_beli = pd.concat(
                            [df_existing, pd.DataFrame([new_row])], ignore_index=True
                        )
                    st.success(f"{selected_row['nama_obat']} ditambahkan ke tabel pembelian!")
                    st.rerun()
        else:
            st.warning("Obat tidak ditemukan di database. Gunakan tombol ➕ Obat Baru untuk menambahkannya.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Tabel rincian item pembelian ──────────────────────────────────────────
    st.markdown(
        """
        <div class='table-container'>
            <div class='table-title'>📦 Rincian Item Pembelian</div>
        """,
        unsafe_allow_html=True
    )
    st.caption("Isi data pembelian. Kolom Jumlah, Satuan, Harga Beli, Harga Jual, Batch, dan Tanggal Expired dapat diedit.")

    SATUAN_OPTIONS = ["BOX", "BOTOL", "TABLET", "KAPSUL", "AMPUL", "SACHET", "STRIP", "TUBE", "LAINNYA"]

    edited_df = st.data_editor(
        st.session_state.df_beli,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "No.": st.column_config.NumberColumn(
                "No.", disabled=True, width="small"
            ),
            "Nama Obat": st.column_config.TextColumn(
                "Nama Obat", width="large"
            ),
            "Jumlah": st.column_config.NumberColumn(
                "Jumlah", min_value=0.0, format="%.2f", width="small"
            ),
            "Satuan": st.column_config.SelectboxColumn(
                "Satuan", options=SATUAN_OPTIONS, width="small"
            ),
            "Harga Beli": st.column_config.NumberColumn(
                "Harga Beli", min_value=0.0, format="%.2f", width="medium"
            ),
            "Harga Jual": st.column_config.NumberColumn(
                "Harga Jual", min_value=0.0, format="%.2f", width="medium"
            ),
            "Subtotal": st.column_config.NumberColumn(
                "Subtotal", disabled=True, format="%.2f", width="medium"
            ),
            "Batch": st.column_config.TextColumn(
                "Batch", width="small"
            ),
            "Tanggal Expired": st.column_config.DateColumn(
                "Tanggal Expired", min_value=date.today(), format="DD-MM-YYYY"
            ),
        },
        key="df_beli_editor"
    )

    # Hitung ulang Subtotal otomatis
    edited_df["Subtotal"] = (edited_df["Jumlah"].fillna(0) * edited_df["Harga Beli"].fillna(0)).round(2)
    # Perbarui nomor urut
    edited_df["No."] = range(1, len(edited_df) + 1)
    st.session_state.df_beli = edited_df

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Ringkasan total ───────────────────────────────────────────────────────
    st.markdown(
        """
        <div class='total-container'>
            <div class='action-buttons'>
                <button class='btn-custom btn-save' id='btn_simpan_beli'>
                    ✓ Simpan
                </button>
                <button class='btn-custom btn-reset' id='btn_reset_beli'>
                    ⟲ Reset
                </button>
            </div>
            <div>
                <div class='total-label'>Total Subtotal</div>
                <div class='total-value' id='total-subtotal-value'>Rp 0,00</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    total_subtotal = edited_df["Subtotal"].sum()
    st.markdown(
        f"<script>document.getElementById('total-subtotal-value').textContent = 'Rp {total_subtotal:,.2f}'.replace(',', '.');</script>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Tombol simpan ke dataset stok ─────────────────────────────────────────
    col_simpan_beli, col_reset_beli = st.columns([1, 1])
    with col_simpan_beli:
        if st.button("💾 Simpan Pembelian ke Stok", type="primary", use_container_width=True):
            df_stok = load_data()
            if df_stok is None:
                st.error("Dataset stok belum tersedia. Upload dataset terlebih dahulu di menu Tampilkan Stok Obat Hari Ini.")
            elif edited_df.empty:
                st.warning("Tabel pembelian kosong.")
            else:
                new_rows = []
                for _, row in edited_df.iterrows():
                    if not str(row["Nama Obat"]).strip():
                        continue
                    prev = df_stok[df_stok["Nama Obat"].str.lower() == str(row["Nama Obat"]).strip().lower()]
                    stok_sblm = int(prev["Stok Akhir"].iloc[-1]) if not prev.empty else 0
                    stok_akhir_baru = stok_sblm + int(row["Jumlah"])
                    new_rows.append({
                        "Tanggal": pd.Timestamp(date.today()),
                        "Nama Obat": str(row["Nama Obat"]).strip(),
                        "Kategori": "Lainnya",
                        "Satuan": row["Satuan"] if row["Satuan"] else "Lainnya",
                        "Stok Masuk": int(row["Jumlah"]),
                        "Stok Keluar": 0,
                        "Stok Akhir": stok_akhir_baru,
                        "Harga Satuan (Rp)": float(row["Harga Beli"]),
                        "Total Nilai (Rp)": float(row["Subtotal"]),
                        "Tanggal Kadaluarsa": pd.Timestamp(row["Tanggal Expired"]),
                        "Supplier": supplier_terpilih,
                        "Keterangan": f"Pembelian - Faktur {no_faktur}"
                    })
                if new_rows:
                    df_stok = pd.concat([df_stok, pd.DataFrame(new_rows)], ignore_index=True)
                    save_data(df_stok)
                    st.session_state.df_beli = pd.DataFrame([
                        {
                            "No.": 1, "Nama Obat": "",
                            "Jumlah": 0.0, "Satuan": "BOX", "Harga Beli": 0.0,
                            "Harga Jual": 0.0, "Subtotal": 0.0,
                            "Batch": "", "Tanggal Expired": pd.Timestamp(date.today())
                        }
                    ])
                    st.success(f"✅ {len(new_rows)} item berhasil disimpan ke stok!")
                    st.rerun()
    with col_reset_beli:
        if st.button("🗑️ Reset Tabel", type="secondary", use_container_width=True):
            st.session_state.df_beli = pd.DataFrame([
                {
                    "No.": 1, "Nama Obat": "",
                    "Jumlah": 0.0, "Satuan": "BOX", "Harga Beli": 0.0,
                    "Harga Jual": 0.0, "Subtotal": 0.0,
                    "Batch": "", "Tanggal Expired": pd.Timestamp(date.today())
                }
            ])
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class='app-footer'>
            <p>All Rights Reserved</p>
            <p style='color: #e94560; font-weight: 600;'>Vmedis 1.8.0</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("© Apotek Veteran Blitar")
