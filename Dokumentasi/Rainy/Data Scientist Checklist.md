# Checklist Data Scientist — DyslexiaLens

> Dokumen ini adalah operasionalisasi tugas Data Scientist dari **Project Plan** dan **List Tugas (Tech Stack)** Capstone DyslexiaLens.
> Status diperbarui per Checkpoint 3 (19 April 2026).
>
> **Simbol:** `[x]` = Selesai | `[~]` = Sedang dikerjakan | `[ ]` = Belum dikerjakan

---

## ⭐ MAIN QUEST (Wajib)

---

### 1. Persiapan & Pengumpulan Dataset

- [x] Menentukan satu solusi utama proyek yang akan dikembangkan *(DyslexiaLens: Early Screening Disleksia)*
- [x] Mengidentifikasi dan memilih dataset publik yang relevan *(Gambo — Dyslexia Handwriting Dataset dari Kaggle)*
- [x] Memvalidasi lisensi dan sumber dataset serta mencantumkan referensi ilmiahnya
- [x] Mengunduh dan menyimpan dataset ke dalam repositori lokal

---

### 2. Mendefinisikan Pertanyaan Bisnis

- [x] Mendefinisikan pertanyaan bisnis utama yang terukur:
  - *"Dapatkah pola goresan tulisan tangan digunakan sebagai indikator awal disleksia?"*
  - *"Seberapa parah tingkat gejala disleksia berdasarkan keparahan coretan (Severity Score 0–6)?"*
- [x] Mendefinisikan target variabel yang jelas:
  - `target_class` (0 = Normal, 1 = Disleksia)
  - `severity_score` (0 = Sehat, 1–6 = Ringan hingga Parah)

---

### 3. Data Wrangling (End-to-End)

#### A. Gathering Data
- [x] Mengumpulkan dataset dari sumber publik (Kaggle)
- [x] Memverifikasi integritas file (total 208.372 file `.png`, nol file corrupt)
- [x] Mencatat statistik dasar: jumlah per kelas, resolusi, format warna

#### B. Assessing Data
- [x] Mengaudit hierarki dan struktur folder dataset (`Train/Test → Corrected/Normal/Reversal`)
- [x] Mengidentifikasi bahwa folder numerik `1, 4, 5, 6, 7, 8, 9` = **Severity Score** (bukan karakter angka)
- [x] Memvalidasi skala keparahan bawaan yang terbalik (1 = Parah, 9 = Ringan)
- [x] Mendeteksi **Kontaminasi Label** (*Label Noise*): file `NormalXXXX.png` terselip di kelas non-Normal
- [x] Memvalidasi secara visual bahwa kelas `Normal` asli juga mengandung sampel bergoresan tidak wajar
- [x] Mendokumentasikan seluruh temuan audit dalam file Markdown

#### C. Cleaning Data
- [x] Memfilter semua file `NormalXXXX.png` yang terselip menggunakan *Logical Cleaning* (Pandas DataFrame)
- [x] Membuang baris bermasalah dari tabel tanpa menghapus file fisik aslinya
- [x] Mengoreksi skala Severity Score menggunakan *Dictionary Mapping* ke rentang `0–6`:
  - Skor asli `9` → Skor AI `1` (Paling Ringan)
  - Skor asli `4` & `1` → Skor AI `6` (Paling Parah, digabung)
- [x] Mengimplementasikan Physical Renaming *(Opsional)* untuk mengganti nama file secara fisik sesuai skala baru
- [x] Menghasilkan `master_dataset_dyslexia.csv` sebagai output data bersih (~180.726 baris)

---

### 4. Exploratory Data Analysis (EDA)

- [x] Membuat visualisasi distribusi kelas (`Normal`, `Corrected`, `Reversal`) per split (Train/Test)
- [x] Membuat visualisasi distribusi Severity Score (0–6) dalam bentuk bar chart
- [x] Menampilkan sampel gambar representatif per kelas dan per skor keparahan
- [x] Menganalisis potensi *class imbalance* antara kelas Normal vs Disleksia
- [x] Menganalisis pola kesalahan tulisan:
  - [x] Pola *letter reversal* (terutama pada kelas `Reversal`)
  - [x] Tingkat *scribbling* berdasarkan Severity Score
- [x] Mendokumentasikan setiap temuan EDA awal (Temuan 1-3) dalam notebook dan file Markdown

---

### 5. Visualisasi Data & Explanatory Analysis

- [x] Membuat visualisasi yang menjawab pertanyaan bisnis:
  - [x] *"Apakah perbedaan distribusi visual antara kelas Normal dan Disleksia signifikan?"* → Heatmap + sampel visual
  - [x] *"Apakah Severity Score 6 secara visual jauh berbeda dari Severity Score 1?"* → Heatmap + sampel visual
- [x] Memastikan setiap grafik disertai narasi/insight dalam format Markdown
- [x] Menarik kesimpulan dari visualisasi yang mendukung hipotesis awal

---

### 6. Kesiapan Data untuk Pemodelan

- [x] Memastikan dataset tidak mengandung informasi target di dalam fitur (*no data leakage*)
- [x] Memastikan format output (`master_dataset_dyslexia.csv`) siap dibaca oleh pipeline model
- [x] Membuat **Data Dictionary** formal yang mendefinisikan setiap kolom CSV secara eksplisit → Sel 6A
- [x] Memvalidasi split Train/Test yang sudah ada → Sel 6B (proporsi + distribusi per split)
- [x] Membuat split validasi tambahan dari data Train:
  - [x] Rasio: 80% Train aktual + 20% Validation (stratified by severity_score)
  - [x] Distribusi kelas seimbang di setiap split → Verified di sel 6D
  - [x] Output: `master_dataset_final.csv` (Train/Validation/Test)
- [x] Mendokumentasikan strategi augmentasi yang disarankan untuk AI Engineer:
  - [x] Rotasi kecil (±10°) → Diimplementasikan di Tahap 5
  - [x] Scaling (0.9×–1.1×) → Diimplementasikan di Tahap 5 (menggantikan shear)
  - [x] **JANGAN** Horizontal Flip (akan merusak label Reversal) → Didokumentasikan
- [x] Menyiapkan format handover dataset ke tim AI Engineer → `master_dataset_augmented.csv` + class weights

---

### 7. Dashboard Streamlit

- [ ] Merancang layout dashboard (halaman apa saja yang diperlukan)
- [ ] Membangun halaman **Overview Distribusi Dataset** (bar chart, statistik ringkas)
- [ ] Membangun halaman **Visualisasi Sampel** (tampilkan gambar per kelas dan skor)
- [ ] Membangun halaman **Insight EDA** (grafik explanatory + narasi)
- [ ] Menjalankan dashboard secara lokal dan melakukan pengujian fungsional

---

### 8. Dokumentasi

- [x] `Analisis Dataset.md` — Laporan analisis dan audit dataset (Update: Temuan 3)
- [x] `Koreksi Disleksia.md` — Temuan Severity Score dan skema pelabelan
- [x] `Penjelasan_Kelas_Dataset.md` — Penjelasan kelas dan anomali visual
- [x] `Pipeline_Preprocessing_Data.md` — Dokumentasi teknis pipeline (Update: Dual-Path Logic)
- [x] `Temuan_EDA.md` — Dokumentasi lengkap temuan EDA + hasil augmentasi + class weights
- [x] `README.md` (root) — Dokumentasi repositori utama
- [x] `Checkpoint1.md` — Rekam jejak progres Checkpoint 1
- [x] `Checkpoint2.md` — Rekam jejak progres Checkpoint 2
- [x] `DATA_SCIENTIST_CHECKLIST.md` — *(file ini sendiri, terus disinkronkan)*
- [x] Dokumentasi hasil EDA dalam format Markdown dengan narasi lengkap

---

## 🌟 SIDE QUEST (Nilai Tambah / Opsional)

---

- [ ] **Feature Engineering** — Menghasilkan fitur turunan yang lebih informatif dari data gambar (misalnya: kepadatan piksel per kuadran, rasio hitam-putih, dll.)
- [ ] **Deployment Dashboard Streamlit Cloud** — Mempublikasikan dashboard agar dapat diakses secara online
- [ ] **A/B Testing** — Membandingkan dua pendekatan preprocessing/augmentasi menggunakan metode A/B Testing dengan Python
- [ ] **Laporan Teknis Komprehensif (PDF)** — Menyusun laporan dari tahap *Problem Discovery* hingga hasil akhir dalam format PDF

---

## 🔗 Catatan & Dependensi

### Ke AI Engineer
| Kebutuhan AI Engineer | Tanggung Jawab DS | Status |
|---|---|---|
| File dataset bersih siap training | `master_dataset_dyslexia.csv` | ✅ Selesai |
| Kolom `image_path`, `target_class`, `severity_score` | Sudah ada di CSV | ✅ Selesai |
| Strategi augmentasi yang aman | Dokumentasi di Pipeline_Preprocessing_Data.md | ✅ Selesai |
| Split train/validation/test yang jelas | Stratified split dari CSV | ⏳ Belum dikerjakan |
| Data Dictionary formal | Belum dibuat | ⏳ Belum dikerjakan |

### Ke Full-Stack Developer / Backend
| Kebutuhan Backend | Tanggung Jawab DS | Status |
|---|---|---|
| Format input gambar yang diharapkan model | Didefinisikan setelah model siap (AI Engineer) | 🔗 Dependensi AI |
| Insight untuk halaman hasil prediksi | Dari hasil EDA dan output model | ⏳ Menunggu EDA |

### Larangan Keras (Dari List Tugas)
> ❌ Menggunakan dataset yang sudah siap pakai tanpa proses pembersihan manual — **DILANGGAR JIKA**: tidak ada bukti audit/cleaning *(sudah mitigasi: ada Pipeline_Preprocessing_Data.md)*
>
> ❌ Melakukan analisis data tanpa penjelasan teks/Markdown — **Wajib**: setiap EDA harus disertai narasi
>
> ❌ Menarik kesimpulan tanpa visualisasi — **Wajib**: semua insight harus didukung grafik
>
> ❌ Format dataset akhir belum siap digunakan untuk modeling — **Sudah mitigasi**: `master_dataset_dyslexia.csv` ✅
>
> ❌ Data Leakage (informasi target masuk ke fitur training) — **Sudah mitigasi**: kolom `target_class` terpisah ✅
