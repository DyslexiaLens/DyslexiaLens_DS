# 🧠 DyslexiaLens — Data Science Repository

> Bagian Data Science dari Capstone Project **DyslexiaLens**: Intelligent Handwriting Detection and Assistance for Dyslexia.
>
> Repositori ini berisi seluruh proses kerja Data Scientist, mulai dari eksplorasi dan audit dataset, pembersihan data, pembuatan pipeline preprocessing, hingga dataset final yang siap digunakan oleh tim AI Engineer untuk proses pelatihan model.

---

## 📌 Tentang Proyek

**DyslexiaLens** adalah sistem *early screening* disleksia berbasis analisis citra tulisan tangan. Sistem ini **bukan alat diagnosis medis**, melainkan alat bantu skrining awal yang dapat digunakan oleh orang tua dan pendidik sebelum pemeriksaan lebih lanjut oleh profesional.

| Detail | Keterangan |
|---|---|
| **Tema** | Accessible & Adaptive Learning |
| **Peran Repositori Ini** | Data Science — Dataset Preparation & Analysis |
| **Dataset Utama** | Gambo (Handwriting Dyslexia Dataset) |
| **Total Sampel Awal** | 208.372 gambar `.png` |
| **Total Sampel Bersih** | ~180.726 gambar (setelah drop kontaminasi label) |
| **Format Output** | `master_dataset_dyslexia.csv` |

---

## 🗂️ Struktur Repositori

```
Dataset Disleksia/
│
├── 📓 Dyslexia.ipynb               # Notebook utama preprocessing & CSV generation
├── 📊 master_dataset_dyslexia.csv  # Output dataset bersih (di-gitignore, generate lokal)
├── 🔒 .gitignore
│
├── 📁 Gambo/                       # Dataset asli (di-gitignore, unduh terpisah)
├── 📁 Gambo_Processed/             # Dataset hasil restrukturisasi awal (di-gitignore)
│
├── 📁 Python Stuff/                # Script Python helper
│   ├── dataset_stats_script.py     # Menghitung statistik dataset
│   ├── generate_csv.py             # Versi standalone dari CSV generator
│   ├── preprocess_gambo.py         # Script restrukturisasi dataset fisik
│   └── viz.py                      # Visualisasi sampel gambar di terminal
│
└── 📁 Dokumentasi/
    ├── Rainy/                      # Dokumentasi Data Scientist (penulis repo)
    |   ├── Checkpoint/             # Checkpoint Kerja
    |   |   ├── Checkpoint1.md      # Checkpoint 1
    │   ├── Analisis Dataset.md     # Laporan analisis & audit dataset lengkap
    │   ├── Koreksi Disleksia.md    # Temuan severity score & skema pelabelan
    │   ├── Penjelasan_Kelas_Dataset.md  # Penjelasan kelas & anomali visual
    │   └── Pipeline_Preprocessing_Data.md  # Dokumentasi pipeline teknis
    ├── Referensi/                  # Dokumen referensi tim
    │   ├── Project Plan.md         # Rencana proyek & milestone
    │   └── List Tugas.md           # Tech stack checklist (Main & Side Quest)
    └── w0pal/                      # Dokumentasi anggota tim lain
```

---

## 🔬 Alur Kerja Data Science

### Tahap 1 — Eksplorasi & Audit Dataset
Melakukan analisis mendalam pada dataset `Gambo` menggunakan script Python:
- Menghitung distribusi gambar per kelas dan per split.
- Memvalidasi konsistensi format file (resolusi, tipe warna, ekstensi).
- Melakukan inspeksi visual manual pada sampel gambar.

Temuan penting dapat dibaca di: [`Dokumentasi/Rainy/Analisis Dataset.md`](Dokumentasi/Rainy/Analisis%20Dataset.md)

---

### Tahap 2 — Data Auditing (Penemuan Kritis)
Selama proses audit, ditemukan dua anomali kritis:

**1. Sistem Severity Score (Temuan Utama)**
Folder numerik (`1, 4, 5, 6, 7, 8, 9`) di dalam kelas `Corrected` dan `Reversal` **bukan** merujuk pada karakter angka, melainkan merepresentasikan **Tingkat Keparahan Goresan (Severity Score)**. Dengan skala asli yang terbalik: `1` = Paling Parah, `9` = Paling Ringan.

**2. Kontaminasi Label (Label Noise)**
Ditemukan file bernama `NormalXXXX.png` yang terselip di dalam folder `Corrected` dan `Reversal`, namun isinya secara visual adalah goresan yang sangat cacat — bukan tulisan normal.

Detail selengkapnya: [`Dokumentasi/Rainy/Koreksi Disleksia.md`](Dokumentasi/Rainy/Koreksi%20Disleksia.md)

---

### Tahap 3 — Preprocessing & Normalisasi
Dua pendekatan preprocessing diterapkan:

**A. Physical Renaming (Opsional — Tahap 0 di Notebook)**
Mengganti nama file secara fisik menggunakan *Dictionary Mapping* agar skala keparahan menjadi konsisten:

| Skor Asli | → | Skor Baru | Keterangan |
|---|---|---|---|
| `9` | → | `1` | Paling Ringan |
| `8` | → | `2` | |
| `7` | → | `3` | |
| `6` | → | `4` | |
| `5` | → | `5` | |
| `4` | → | `6` | Corrected Paling Parah |
| `1` | → | `6` | Reversal (digabung ke puncak) |

**B. Logical Cleaning via CSV (Wajib — Tahap 1 di Notebook)**
Memfilter semua gambar kotor dan kontaminasi label langsung dari tabel `Pandas DataFrame` tanpa menghapus file fisik, menghasilkan `master_dataset_dyslexia.csv`.

Detail teknis: [`Dokumentasi/Rainy/Pipeline_Preprocessing_Data.md`](Dokumentasi/Rainy/Pipeline_Preprocessing_Data.md)

---

### Tahap 4 — Output: Master Dataset CSV
File `master_dataset_dyslexia.csv` adalah output final yang akan dikonsumsi oleh AI Engineer untuk proses training model CNN.

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `image_path` | String | Jalur lengkap lokasi file gambar |
| `split` | String | `Train` atau `Test` |
| `folder_category` | String | `Normal`, `Corrected`, atau `Reversal` |
| `severity_score` | Integer (0–6) | Skor keparahan disleksia |
| `target_class` | Integer (0/1) | Label biner: 0 = Normal, 1 = Disleksia |

---

## 🚀 Cara Menjalankan

### Prasyarat
```bash
pip install pandas Pillow
```

### Langkah-langkah
1. **Unduh dataset** `Gambo` dan letakkan di dalam folder root repositori ini.
2. **Buka** `Dyslexia.ipynb` menggunakan Jupyter Notebook atau Google Colab.
3. **Sesuaikan** variabel `root_dir` di setiap cell dengan path dataset Anda:
   - Lokal: `r'Gambo'`
   - Google Colab: `r'/content/drive/MyDrive/Gambo'`
4. **Jalankan** cell secara berurutan:
   - **Tahap 0** *(Opsional)*: Physical renaming file ke skala 1–6.
   - **Tahap 1** *(Wajib)*: Generate `master_dataset_dyslexia.csv`.

> [!WARNING]
> Jalankan **Tahap 0 hanya sekali**. Menjalankannya dua kali pada dataset yang sudah di-rename akan menyebabkan skala bergeser dan data menjadi kacau!

---

## 📊 Statistik Dataset Final

| Split | Normal | Corrected | Reversal | Total |
|---|---|---|---|---|
| Train | 39.334 | ~52.000* | ~40.000* | ~131.334 |
| Test | 19.557 | ~16.000* | ~14.000* | ~49.557 |
| **Total** | **58.891** | **~68.000*** | **~54.000*** | **~180.726** |

*\*Angka perkiraan setelah drop kontaminasi label.*

---

## 📋 Checklist Progres Data Scientist

- [x] Eksplorasi dan audit dataset `Gambo`
- [x] Identifikasi Severity Score (folder 1-9)
- [x] Deteksi kontaminasi label (`NormalXXXX.png`)
- [x] Normalisasi skala severity (Dictionary Mapping → 0–6)
- [x] Logical Cleaning via Pandas DataFrame
- [x] Generate `master_dataset_dyslexia.csv`
- [ ] Exploratory Data Analysis (EDA) lanjutan
- [ ] Visualisasi distribusi kelas & skor
- [ ] Dashboard Streamlit (EDA awal)
- [ ] Dokumentasi Data Dictionary formal
- [ ] Handover dataset ke AI Engineer

---

## 👤 Kontributor

| Nama | Role | Fokus |
|---|---|---|
| Rainy | Data Scientist | Dataset preparation, preprocessing, EDA |
| w0pal | *(Anggota Tim)* | *(sesuai pembagian tugas)* |

---

## 📄 Lisensi & Dataset
Dataset `Gambo` adalah dataset publik. Harap perhatikan lisensi asli dataset sebelum mendistribusikan ulang.
https://www.kaggle.com/datasets/drizasazanitaisa/dyslexia-handwriting-dataset
1. M. S. A. B. Rosli, I. S. Isa, S. A. Ramlan, S. N. Sulaiman and M. I. F. Maruzuki, "Development of CNN Transfer Learning for Dyslexia Handwriting Recognition," 2021 11th IEEE International Conference on Control System, Computing and Engineering (ICCSCE), 2021, pp. 194-199, doi: 10.1109/ICCSCE52189.2021.9530971.
2. N. S. L. Seman, I. S. Isa, S. A. Ramlan, W. Li-Chih and M. I. F. Maruzuki, "Notice of Removal: Classification of Handwriting Impairment Using CNN for Potential Dyslexia Symptom," 2021 11th IEEE International Conference on Control System, Computing and Engineering (ICCSCE), 2021, pp. 188-193, doi: 10.1109/ICCSCE52189.2021.9530989.
3. Isa, Iza Sazanita. CNN Comparisons Models On Dyslexia Handwriting Classification / Iza Sazanita Isa … [et Al.]. Universiti Teknologi MARA Cawangan Pulau Pinang, 2021.
4. Isa, I. S., Rahimi, W. N. S., Ramlan, S. A., & Sulaiman, S. N. (2019). Automated detection of dyslexia symptom based on handwriting image for primary school children. Procedia Computer Science, 163, 440-449.