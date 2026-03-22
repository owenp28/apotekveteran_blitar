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
    ["🏠 Beranda", "📋 Tampilkan Obat Hari Ini", "✏️ Ubah Stok Obat Hari Ini", "🖨️ Cetak & Print Stok Obat", "🛒 Update Stok & Kasir"],
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

    col_input, col_nota = st.columns([1, 1])

    with col_input:
        st.subheader("🛒 Input Penjualan")
        with st.form("form_kasir"):
            list_obat = df["Nama Obat"].unique().tolist()
            nama_obat = st.selectbox("Pilih Obat", list_obat)
            jumlah = st.number_input("Jumlah Beli", min_value=1, value=1)
            bayar_tunai = st.number_input("Nominal Bayar (Rp)", min_value=0, step=500)

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

    with col_nota:
        st.subheader("📄 Preview Nota")
        if st.session_state.cart:
            total_belanja = sum(item["subtotal"] for item in st.session_state.cart)
            kembali = bayar_tunai - total_belanja
            tgl_nota = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            items_html = ""
            for item in st.session_state.cart:
                items_html += f"""
                <div style='display: flex; justify-content: space-between;'>
                    <span>{item['qty']} {item['nama']}</span>
                    <span>{format_rupiah(item['subtotal'])}</span>
                </div>
                <div style='font-size: 10px; margin-bottom: 5px;'>&nbsp;&nbsp;@{format_rupiah(item['harga'])}</div>
                """

            nota_html = f"""
            <div style="font-family: monospace; font-size: 13px; border: 1px solid #ccc;
                        padding: 16px; border-radius: 8px; max-width: 360px;">
                <div style="text-align: center; border-bottom: 1px dashed #000; padding-bottom: 10px;">
                    <b style="font-size: 15px;">PT. SUMBER SEHAT MEDICA FARMA</b><br>
                    Jl. Cepaka 16A RT 01/10 Sukorejo BLT<br>
                    Npwp : 061.096.980.0-653.000<br>
                    <b>VETERAN SEHAT</b>
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
            col_simpan, col_reset = st.columns(2)

            with col_simpan:
                if st.button("💾 Simpan Transaksi & Update Stok", type="primary"):
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
                    st.success("✅ Stok berhasil diupdate! Transaksi tersimpan.")
                    st.rerun()

            with col_reset:
                if st.button("🗑️ Kosongkan Keranjang", type="secondary"):
                    st.session_state.cart = []
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
              Jl. Veteran no 64B Blitar Kota (Sebelah Gang Srigading), Blitar 66111<br>
              Npwp : 061.096.980.0-653.000<br>
              <b>VETERAN SEHAT</b>
            </div>
            <div class="dashed"></div>
            <div>{tgl_nota}</div>
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("© Apotek Veteran Blitar")
