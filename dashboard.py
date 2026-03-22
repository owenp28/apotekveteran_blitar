import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
import os

st.set_page_config(page_title="Apotek Veteran Blitar", layout="wide", page_icon="💊")

# ── CSS Custom untuk Menyesuaikan Tampilan ───────────────────────────────────
# Perubahan ini dilakukan untuk:
# 1. Menghilangkan margin dan padding default di bagian atas sidebar dan main.
# 2. Mengatur elemen agar rapat ke sisi kiri.
# 3. Memberikan kontrol penuh atas penempatan logo dan teks agar sesuai dengan mockup.
st.markdown(
    """
    <style>
    /* Mengurangi padding di bagian atas sidebar agar elemen lebih rapat ke atas */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem !important; 
    }
    /* Mengurangi margin di bagian atas konten utama agar header rapat ke atas */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }
    /* Memastikan teks "Apotek Veteran Blitar" di sidebar sejajar kiri */
    [data-testid="stMarkdownContainer"] {
        text-align: left !important;
    }
    /* Memastikan teks title "Dashboard..." di konten utama sejajar kiri */
    h1 {
        text-align: left !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ─────────────────────────────────────────────────────────────────────────────

DATASET_PATH = os.path.join(os.path.dirname(__file__), "stok_obat.csv")

KOLOM_WAJIB = [
    "Tanggal", "Nama Obat", "Kategori", "Satuan",
    "Stok Masuk", "Stok Keluar", "Stok Akhir",
    "Harga Satuan (Rp)", "Total Nilai (Rp)",
    "Tanggal Kadaluarsa", "Supplier", "Keterangan"
]

def load_data():
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH, parse_dates=["Tanggal", "Tanggal Kadaluarsa"])
        return df
    return None

def save_data(df):
    df.to_csv(DATASET_PATH, index=False)

def format_rupiah(val):
    try:
        return f"Rp {int(val):,}".replace(",", ".")
    except:
        return val

# ── Sidebar navigasi ──────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/pharmacy-shop.png", width=80)
st.sidebar.title("💊 Apotek Veteran Blitar")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Pilih Fitur",
    ["🏠 Beranda", "📋 Tampilkan Stok Obat Hari Ini", "✏️ Ubah Stok Obat Hari Ini", "🖨️ Cetak & Print Stok Obat"],
    index=0
)

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
            col1, col2 = st.columns(2)
            with col1:
                tgl = st.date_input("Tanggal Transaksi", value=date.today())
                nama_obat = st.text_input("Nama Obat *", placeholder="Contoh: Paracetamol 500mg")
                kategori = st.selectbox("Kategori", ["Analgesik", "Antibiotik", "Antasida", "Vitamin", "Antihistamin", "Antihipertensi", "Antidiabetes", "Lainnya"])
                satuan = st.selectbox("Satuan", ["Tablet", "Kapsul", "Botol", "Ampul", "Sachet", "Strip", "Tube", "Lainnya"])
            with col2:
                stok_masuk = st.number_input("Stok Masuk", min_value=0, value=0)
                stok_keluar = st.number_input("Stok Keluar (Terjual)", min_value=0, value=0)
                harga_satuan = st.number_input("Harga Satuan (Rp)", min_value=0, value=0, step=500)
                tgl_exp = st.date_input("Tanggal Kadaluarsa", value=date.today())
                supplier = st.text_input("Supplier", placeholder="Nama distributor/supplier")
                keterangan = st.text_area("Keterangan", placeholder="Opsional")

            submitted = st.form_submit_button("💾 Simpan Transaksi", type="primary")

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

        idx_hapus = st.number_input("Masukkan ID Baris yang akan dihapus", min_value=0, max_value=max(len(df)-1, 0), value=0)
        if st.button("🗑️ Hapus Baris", type="secondary"):
            df = df.drop(index=idx_hapus).reset_index(drop=True)
            save_data(df)
            st.success(f"Baris ID {idx_hapus} berhasil dihapus.")
            st.rerun()

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

# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("© Apotek Veteran Blitar")
