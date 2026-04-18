# Checkpoint 2 — Refinement & Integrity Sync
**Tanggal:** 18 April 2026  
**Role:** Data Scientist  
**Status Notebook:** `Dyslexia.ipynb` (Tahap 1, 2, 3 Selesai)

---

## 🎯 Pencapaian Sesi Ini
Sesi ini berfokus pada sinkronisasi antara **DATA_SCIENTIST_CHECKLIST.md** dengan implementasi nyata di dalam notebook utama. Kami telah merombak struktur notebook agar lebih profesional, auditable, dan siap untuk tahap EDA lanjutan.

### 1. Re-Strukturisasi Notebook (`Dyslexia.ipynb`)
Notebook telah diorganisir ulang menjadi tahapan yang logis dan naratif:
- **Header & Bisnis:** Penambahan sel Judul, Pertanyaan Bisnis, Hipotesis, dan Definisi Variabel Target (Binary & Severity).
- **Sumber & Referensi:** Penambahan sel identitas dataset (Link Kaggle) dan referensi sitasi ilmiah untuk kredibilitas akademik.
- **Tahap 1 (Assessing Data):** Penambahan audit algoritmik untuk menghitung distribusi serta audit integritas via **Sampling Verify** (Mengecek format, resolusi, dan kemungkinan file corrupt).
- **Tahap 2 (Physical Renaming):** Kode opsional untuk menata ulang folder fisik.
- **Tahap 3 (Cleaning & CSV):** Implementasi *Logical Cleaning* final.

### 2. Inovasi Teknis: Dual-Path Logic
Kami mengimplementasikan algoritma ekstraksi skor yang cerdas (*Dual-Path Logic*) pada Tahap 3. Kode ini secara otomatis mendeteksi apakah dataset sudah di-rename (Tahap 2) atau belum. 
- Sistem ini menjamin notebook tetap jalan 100% (reproducible) di Google Colab tanpa harus menjalankan penamaan ulang fisik yang memakan waktu I/O lama.

### 3. Temuan Audit Baru: "Two-Way Label Noise"
Melalui inspeksi visual manual yang lebih mendalam, kami menemukan bahwa kontaminasi label terjadi dua arah:
- Bukan hanya file `NormalXXXX.png` yang tersesat di folder Disleksia.
- Tetapi kelas `Normal` asli juga mengandung sampel yang secara visual memiliki karakteristik coretan disleksia.
- **Keputusan:** Kami mencatat ini sebagai risiko residual dan tetap menggunakan CSV sebagai satu-satunya sumber kebenaran data untuk training.

---

## 📊 Status Checklist Terkini
- **Persiapan Dataset:** [x] 100% Selesai
- **Pertanyaan Bisnis:** [x] 100% Selesai
- **Data Wrangling:** [x] 100% Selesai (Assessing, Gathering, Cleaning)
- **EDA & Visualisasi:** [~] In Progress (Kerangka sudah siap)

---

## 📂 Artefak Dokumentasi yang Diperbarui
1. [Analisis Dataset.md](file:///d:/Tugas/Kuliah/Semester%206/Dicoding/Capstone%20Project/Dataset%20Disleksia/Dokumentasi/Rainy/Analisis%20Dataset.md) — Ditambahkan temuan Anomali Visual Normal.
2. [Pipeline_Preprocessing_Data.md](file:///d:/Tugas/Kuliah/Semester%206/Dicoding/Capstone%20Project/Dataset%20Disleksia/Dokumentasi/Rainy/Pipeline_Preprocessing_Data.md) — Sinkronisasi penomoran Tahap 1-4 dan penjelasan Dual-Path Logic.
3. [DATA_SCIENTIST_CHECKLIST.md](file:///d:/Tugas/Kuliah/Semester%206/Dicoding/Capstone%20Project/Dataset%20Disleksia/Dokumentasi/Rainy/Data%20Scientist%20Checklist.md) — Sinkronisasi status progres.

---

## 🚀 Rencana Sesi Berikutnya
- Mengeksekusi **Tahap 4: EDA** di notebook.
- Melakukan visualisasi distribusi kelas dan keparahan secara grafis (Matplotlib/Seaborn).
- Membuat plot perbandingan visual sampel antar skor (1 vs 6).
- Validasi statistik untuk menjawab pertanyaan bisnis.
