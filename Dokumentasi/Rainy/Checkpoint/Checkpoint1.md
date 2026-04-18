# ✅ Checkpoint 1 — Persiapan Dataset & Preprocessing

**Tanggal:** 18 April 2026  
**Peran:** Data Scientist  
**Periode Milestone:** 13 – 19 April (sesuai Project Plan)  
**Status:** 🟡 Dalam Progres

---

## 📋 Ringkasan Eksekutif

Checkpoint ini menandai selesainya fase pertama pekerjaan Data Scientist pada proyek DyslexiaLens: **Eksplorasi, Audit, dan Preprocessing Dataset**. Fase ini menghasilkan `master_dataset_dyslexia.csv` yang siap dikonsumsi oleh tim AI Engineer untuk proses training model CNN.

---

## ✅ Hal yang Sudah Diselesaikan

### 1. Eksplorasi Struktur Dataset
- [x] Memeriksa hierarki folder dataset `Gambo` secara menyeluruh
- [x] Mengidentifikasi split bawaan: `Train` dan `Test`
- [x] Mengidentifikasi tiga kelas utama: `Normal`, `Corrected`, `Reversal`
- [x] Menjalankan script statistik (`dataset_stats_script.py`) untuk menghitung distribusi gambar

**Hasil:**
| Split | Corrected | Normal | Reversal | Total |
|---|---|---|---|---|
| Train | 65.534 | 39.334 | 46.781 | 151.649 |
| Test | 19.284 | 19.557 | 17.882 | 56.723 |
| **Total** | **84.818** | **58.891** | **64.663** | **208.372** |

---

### 2. Kompatibilitas & Format Data
- [x] Seluruh 208.372 file berformat `.png` — konsistensi 100%
- [x] Resolusi sangat seragam: **28x28** dan **29x29** piksel (identik dengan MNIST/EMNIST)
- [x] Format warna: Grayscale (`L`) atau Binary (`1`) — tidak ada RGB
- [x] **Nol file rusak (corrupt)** ditemukan

---

### 3. Data Auditing & Penemuan Kritis

#### 🔍 Temuan 1: Sistem Severity Score (Kunci Keberhasilan Proyek)
- [x] Mengidentifikasi bahwa folder numerik `1, 4, 5, 6, 7, 8, 9` **bukan** merepresentasikan karakter angka
- [x] Membuktikan melalui inspeksi visual bahwa folder tersebut berisi hampir seluruh abjad huruf
- [x] Menyimpulkan angka folder = **Tingkat Keparahan Coretan (Severity Score)**
- [x] Memvalidasi skala asli yang terbalik: `1` = Paling Parah, `9` = Paling Ringan

> **Dampak:** Asumsi awal *Data Leakage* terbukti GUGUR. Dataset tidak cacat secara arsitektur — model tidak akan hanya belajar mengenali karakter, melainkan dipaksa belajar **pola goresan tulisan disleksia**.

#### 🔍 Temuan 2: Kontaminasi Label (Label Noise)
- [x] Menemukan file `NormalXXXX.png` terselip di dalam folder `Corrected` dan `Reversal`
- [x] Memvalidasi secara visual bahwa file tersebut berisi goresan cacat (bukan tulisan normal)
- [x] Menemukan kelas `Normal` asli pun mengandung sampel bergoresan tidak wajar
- [x] Memutuskan untuk melakukan **Drop Data** via Logical Cleaning

---

### 4. Normalisasi Skala Severity (Preprocessing Kritis)
- [x] Merancang sistem *Dictionary Mapping* untuk mengoreksi skala terbalik
- [x] Memutuskan skala final: **0 (Normal/Sehat) → 6 (Paling Parah)**
- [x] Menggabungkan `Reversal` skor asli `1` dan `Corrected` skor asli `4` ke pucak **Skor 6** (menghilangkan gap kosong di 7 dan 8)

**Tabel Pemetaan Final:**
| Skor Asli | Skor AI Baru | Makna |
|---|---|---|
| `9` | **1** | Paling Ringan |
| `8` | **2** | |
| `7` | **3** | |
| `6` | **4** | |
| `5` | **5** | |
| `4` | **6** | Corrected Paling Parah |
| `1` | **6** | Reversal Paling Parah (digabung) |
| Normal | **0** | Bebas Disleksia |

---

### 5. Pengembangan Pipeline Preprocessing (`Dyslexia.ipynb`)
- [x] Membuat notebook `Dyslexia.ipynb` sebagai pipeline preprocessing utama
- [x] **Tahap 0 — Physical Renaming (Opsional):**
  - Mengganti nama file gambar secara fisik menggunakan Dictionary Mapping
  - Sistem dua fase (`.TEMP` → final) untuk menghindari konflik nama
  - Sistem *Retry* (10x + `time.sleep(0.1)`) untuk mengatasi `PermissionError WinError 32` Windows
- [x] **Tahap 1 — Logical Cleaning & CSV Generation (Wajib):**
  - Scan semua 208.372 jalur file ke dalam Pandas DataFrame
  - Filter `NormalXXXX.png` yang tersesat secara logis (tanpa hapus file fisik)
  - Ekstrak Severity Score dari nama file
  - Generate `master_dataset_dyslexia.csv` dengan ~180.726 baris data bersih

---

### 6. Restrukturisasi Awal Dataset (Eksplorasi)
- [x] Membuat `preprocess_gambo.py` untuk restrukturisasi dataset secara fisik awal
- [x] Menghasilkan folder `Gambo_Processed/` dengan format `[Karakter]/[Kelas]`
- [x] Mengidentifikasi bahwa pendekatan restrukturisasi fisik tidak diperlukan (digantikan CSV)

---

### 7. Dokumentasi
- [x] `Analisis Dataset.md` — Laporan analisis & audit dataset lengkap (revisi dari asumsi awal)
- [x] `Koreksi Disleksia.md` — Temuan severity score, skema pelabelan, dan kontaminasi label
- [x] `Penjelasan_Kelas_Dataset.md` — Penjelasan kelas Normal/Corrected/Reversal & anomali visual
- [x] `Pipeline_Preprocessing_Data.md` — Dokumentasi teknis pipeline lengkap dengan tabel & diagram
- [x] `README.md` (root) — README standar GitHub mencakup seluruh alur kerja Data Scientist

---

### 8. Manajemen Repositori
- [x] Mengatur `.gitignore` untuk mengecualikan `Gambo/`, `Gambo_Processed/`, `*.zip`, `*.rar`, `*.csv`
- [x] Menyusun struktur direktori yang rapi: `Dokumentasi/Rainy/`, `Python Stuff/`, `Referensi/`
- [x] Memisahkan script helper ke folder `Python Stuff/`

---

## 🔴 Hal yang Belum Selesai (Target Berikutnya)

- [ ] **Exploratory Data Analysis (EDA) Lanjutan**
  - Distribusi kelas dan skor visualisasi (bar chart, pie chart)
  - Analisis sampel gambar per kelas & skor (menampilkan contoh tiap kategori)
  - Deteksi *class imbalance* antara Train vs Test
- [ ] **Data Dictionary Formal**
  - Mendefinisikan setiap kolom di `master_dataset_dyslexia.csv` secara formal
- [ ] **Dashboard Streamlit (EDA Awal)**
  - Membangun dashboard interaktif untuk visualisasi distribusi dataset
- [ ] **Validasi Hipotesis**
  - Apakah pola visual tulisan kelas `Reversal` dan `Corrected` cukup berbeda secara statistik dari kelas `Normal`?
- [ ] **Handover ke AI Engineer**
  - Menyiapkan format input yang dibutuhkan tim AI untuk training CNN

---

## 📁 Artefak yang Dihasilkan

| Artefak | Lokasi | Keterangan |
|---|---|---|
| `Dyslexia.ipynb` | `/` (root) | Notebook preprocessing utama |
| `master_dataset_dyslexia.csv` | `/` (root, gitignored) | Dataset bersih siap training |
| `Analisis Dataset.md` | `Dokumentasi/Rainy/` | Laporan analisis dataset |
| `Koreksi Disleksia.md` | `Dokumentasi/Rainy/` | Skema pelabelan & score |
| `Penjelasan_Kelas_Dataset.md` | `Dokumentasi/Rainy/` | Penjelasan kelas & anomali |
| `Pipeline_Preprocessing_Data.md` | `Dokumentasi/Rainy/` | Dokumentasi pipeline teknis |
| `README.md` | `/` (root) | Dokumentasi repositori utama |
| `preprocess_gambo.py` | `Python Stuff/` | Script restrukturisasi fisik |
| `dataset_stats_script.py` | `Python Stuff/` | Script statistik dataset |
| `generate_csv.py` | `Python Stuff/` | Script standalone CSV generator |
| `viz.py` | `Python Stuff/` | Script visualisasi ASCII gambar |
