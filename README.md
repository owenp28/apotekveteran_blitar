# Dashboard Stok Obat — Apotek Veteran Blitar 💊

## 📊 Deskripsi Proyek

Dashboard interaktif berbasis **Streamlit** untuk mengelola stok obat di **Apotek Veteran Blitar**. Dashboard ini memudahkan pengelolaan stok obat secara real-time langsung melalui web, mulai dari menampilkan data stok, memperbarui transaksi masuk/keluar, hingga mencetak laporan dalam berbagai format file.

---

## 📑 Table of Contents

- [Deskripsi Fitur](#-deskripsi-fitur)
- [Struktur Folder](#-struktur-folder)
- [Dataset](#-dataset)
- [Setup Environment](#-setup-environment)
- [Cara Menjalankan Dashboard](#-cara-menjalankan-dashboard)
- [Panduan Penggunaan](#-panduan-penggunaan)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Deskripsi Fitur

Dashboard ini terdiri dari **4 menu utama** yang dapat diakses langsung melalui sidebar. Setiap menu membawa pengguna ke tampilan yang sesuai dengan fitur yang dipilih.

---

### 🏠 Beranda

Halaman utama yang menampilkan ringkasan kondisi stok apotek secara keseluruhan:
- Total jenis obat yang tersedia
- Total stok akhir seluruh obat
- Jumlah obat yang mendekati atau melewati tanggal kadaluarsa (≤ 30 hari)

---

### 📋 Fitur 1 — Tampilkan Obat Hari Ini

Fitur untuk menampilkan seluruh data stok obat sesuai dataset yang telah diunggah.

**Alur penggunaan:**
1. **Langkah pertama (sekali saja):** Pengguna wajib mengunggah file CSV dataset stok obat melalui web. Setelah dataset berhasil diunggah dan tersimpan, form upload tidak akan muncul lagi pada kunjungan berikutnya — dashboard langsung menampilkan data stok.
2. **Jika ingin mengganti dataset:** Gunakan tombol *Hapus Dataset* di bagian bawah halaman, lalu upload ulang file baru.

**Informasi yang ditampilkan (sesuai kolom dataset):**
| Kolom | Keterangan |
|---|---|
| Tanggal | Tanggal transaksi |
| Nama Obat | Jenis/nama obat |
| Kategori | Kategori obat (Analgesik, Antibiotik, dll.) |
| Satuan | Satuan obat (Tablet, Kapsul, Botol, dll.) |
| Stok Masuk | Jumlah obat yang masuk/diterima |
| Stok Keluar | Jumlah obat yang terjual/keluar |
| Stok Akhir | Sisa stok setelah transaksi |
| Harga Satuan (Rp) | Harga per satuan obat |
| Total Nilai (Rp) | Total nilai stok akhir |
| Tanggal Kadaluarsa | Tanggal expired obat |
| Supplier | Nama distributor/supplier |
| Keterangan | Catatan tambahan transaksi |

**Fitur tambahan:**
- Filter berdasarkan **bulan**, **kategori obat**, dan **pencarian nama obat**
- Ringkasan otomatis: total stok masuk, keluar, dan stok akhir
- **Peringatan otomatis** untuk obat yang mendekati atau melewati tanggal kadaluarsa (≤ 30 hari)

---

### ✏️ Fitur 2 — Ubah Stok Obat Hari Ini

Fitur untuk memperbarui data stok obat secara langsung melalui web tanpa perlu upload ulang dataset.

**Cara kerja:**
- Pengguna mengisi form transaksi (stok masuk, stok keluar, harga, supplier, dll.) sesuai komponen yang ada di dataset
- Setelah disimpan, data **langsung terupdate di dataset awal** (`stok_obat.csv`) secara otomatis
- Stok akhir dihitung otomatis berdasarkan riwayat stok obat sebelumnya: `Stok Akhir = Stok Sebelumnya + Stok Masuk - Stok Keluar`
- Perubahan langsung tercermin di fitur **Tampilkan Obat Hari Ini** tanpa perlu upload ulang

**Tab yang tersedia:**
1. **Tambah / Update Transaksi** — Input transaksi baru (penjualan, restock, dll.)
2. **Hapus Baris Data** — Hapus baris data tertentu berdasarkan ID baris

---

### 🖨️ Fitur 3 — Cetak & Print Stok Obat Hari Ini

Fitur untuk mencetak dan mengunduh laporan stok obat setelah data diperbarui.

**Opsi cetak yang tersedia:**

| Opsi | Keterangan |
|---|---|
| **Semua Komponen Obat** | Mencetak seluruh kolom data stok obat yang telah diupdate |
| **Sebagian Komponen Obat** | Pengguna memilih sendiri kolom mana saja yang ingin dicetak secara manual |

**Filter sebelum cetak:**
- Pilih rentang tanggal (dari tanggal — sampai tanggal) untuk menentukan periode laporan

**Format unduhan yang tersedia:**

| Format | Keterangan |
|---|---|
| 📄 **CSV** | File spreadsheet universal, bisa dibuka di Excel/Google Sheets |
| 📊 **Excel (XLSX)** | File Microsoft Excel siap pakai |
| 🖨️ **HTML (Print/PDF)** | Buka file di browser → klik tombol **Print** → pilih **Save as PDF** atau langsung cetak ke printer |

> **Catatan Print:** Saat file HTML dibuka di browser dan tombol Print diklik, tampilan akan langsung menyesuaikan ke dialog print komputer seperti pada umumnya — bisa memilih printer fisik atau menyimpan sebagai PDF.

---

## 📁 Struktur Folder

```
submission/
├── dashboard/
│   ├── stok_obat.csv      # Dataset stok obat Apotek Veteran Blitar
│   └── dashboard.py       # File utama dashboard Streamlit
├── README.md              # Dokumentasi proyek (file ini)
├── requirements.txt       # Dependencies Python
└── url.txt                # URL Streamlit Cloud
```

---

## 📊 Dataset

**File:** `dashboard/stok_obat.csv`

**Deskripsi:** Dataset stok obat Apotek Veteran Blitar yang mencatat seluruh transaksi masuk dan keluar obat per tanggal.

**Kolom dataset:**

| Kolom | Tipe Data | Keterangan |
|---|---|---|
| Tanggal | Date | Tanggal transaksi (YYYY-MM-DD) |
| Nama Obat | String | Nama dan dosis obat |
| Kategori | String | Kategori obat |
| Satuan | String | Satuan obat |
| Stok Masuk | Integer | Jumlah obat masuk |
| Stok Keluar | Integer | Jumlah obat keluar/terjual |
| Stok Akhir | Integer | Sisa stok setelah transaksi |
| Harga Satuan (Rp) | Integer | Harga per satuan |
| Total Nilai (Rp) | Integer | Total nilai stok akhir |
| Tanggal Kadaluarsa | Date | Tanggal expired obat |
| Supplier | String | Nama distributor/supplier |
| Keterangan | String | Catatan transaksi |

**Periode data:** Juli 2026 — Agustus 2026

**Kategori obat yang tersedia:** Analgesik, Antibiotik, Antasida, Vitamin, Antihistamin, Antihipertensi, Antidiabetes

---

## 🛠️ Setup Environment

### Prasyarat

Pastikan sudah menginstall:
- **Python 3.8+** — [Download Python](https://www.python.org/downloads/)
- **pip** (sudah terinstall bersama Python)

### Langkah 1: Clone atau Download Repository

```bash
git clone https://github.com/owenp28/project_analisisdata.git
cd project_analisisdata/submission
```

### Langkah 2: Buat Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

### Langkah 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies yang diinstall:**

| Library | Fungsi |
|---|---|
| `streamlit` | Framework dashboard web |
| `pandas` | Manipulasi dan pengolahan data |
| `openpyxl` | Ekspor file Excel (XLSX) |

---

## 🚀 Cara Menjalankan Dashboard

1. Pastikan virtual environment sudah aktif
2. Masuk ke folder dashboard:
   ```bash
   cd dashboard
   ```
3. Jalankan Streamlit:
   ```bash
   streamlit run dashboard.py
   ```
4. Dashboard otomatis terbuka di browser, atau akses manual di:
   [http://localhost:8501](http://localhost:8501)
5. Untuk menghentikan: tekan `Ctrl + C` di terminal

---

## 📖 Panduan Penggunaan

### Pertama Kali Menggunakan

1. Jalankan dashboard → pilih menu **📋 Tampilkan Obat Hari Ini**
2. Upload file CSV dataset stok obat
3. Setelah upload berhasil, tabel stok obat langsung ditampilkan
4. Form upload tidak akan muncul lagi pada kunjungan berikutnya

### Mencatat Transaksi Penjualan / Restock

1. Pilih menu **✏️ Ubah Stok Obat Hari Ini**
2. Isi form: nama obat, tanggal, stok masuk/keluar, harga, supplier
3. Klik **Simpan Transaksi** — data langsung tersimpan ke dataset
4. Cek hasilnya di menu **📋 Tampilkan Obat Hari Ini**

### Mencetak Laporan

1. Pilih menu **🖨️ Cetak & Print Stok Obat**
2. Pilih opsi: semua kolom atau sebagian kolom (pilih manual)
3. Tentukan rentang tanggal laporan
4. Klik tombol unduh sesuai format yang diinginkan (CSV / Excel / HTML)
5. Untuk print langsung: unduh file HTML → buka di browser → klik tombol **Print**

---

## 🔧 Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'`
```bash
pip install -r requirements.txt
```

### `FileNotFoundError: stok_obat.csv`
Pastikan menjalankan dashboard dari folder `dashboard/`:
```bash
cd dashboard
streamlit run dashboard.py
```

### Ekspor Excel tidak tersedia
```bash
pip install openpyxl
```

### Port 8501 sudah digunakan
```bash
streamlit run dashboard.py --server.port 8502
```

### Virtual environment tidak aktif
**Windows:** `env\Scripts\activate`
**Linux/Mac:** `source env/bin/activate`

---

## 👤 Author

**Apotek Veteran Blitar**

---

**Dibuat dengan ❤️ menggunakan Streamlit**
