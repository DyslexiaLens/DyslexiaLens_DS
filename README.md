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
| **Format Output Final** | `master_dataset_final.csv` (Train, Val, Test) |

---

## 🗂️ Struktur Repositori

```
Dataset Disleksia/
│
├── 📓 Dyslexia.ipynb               # Notebook utama preprocessing & CSV generation
├── 📊 master_dataset_final.csv     # Output dataset siap training (di-gitignore)
├── 🔒 .gitignore
│
├── 📁 Gambo/                       # Dataset asli (di-gitignore, unduh terpisah)
│
├── 📁 Python Stuff/                # Script Python helper
│   ├── dataset_stats_script.py     
│   ├── generate_csv.py             
│   ├── preprocess_gambo.py         
│   └── viz.py                      
│
└── 📁 Dokumentasi/
    ├── Rainy/                      # Dokumentasi Data Scientist (penulis repo)
    |   ├── Checkpoint/             
    |   |   ├── Checkpoint3.md      # Rekap progres terkini
    |   ├── Pembahasan Pembagian Dataset / Todo/
    |   |   ├── Diskusi_Binary_vs_Severity.md
    |   |   ├── Rangkuman_Opsi_Dataset_Training.md
    |   |   └── todo.md             # Rencana Sistem Translasi OCR 
    │   ├── Analisis Dataset.md     
    │   ├── Data Scientist Checklist.md
    │   ├── Koreksi Disleksia.md    
    │   ├── Penjelasan_Kelas_Dataset.md  
    │   ├── Pipeline_Preprocessing_Data.md  
    │   ├── Explanatory_Analysis.md 
    │   └── Temuan_EDA.md           # Parameter class_weight AI Engineer
    └── Referensi/                  # Dokumen referensi tim
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

**A. Physical Renaming (Tahap 2 Notebook)**
Mengkoreksi nama file menjadi skala keparahan numerik 1-6 agar linear (1=Ringan, 6=Terparah).
*Catatan: Digabungnya Reversal (1) dan Corrected Terparah (4) membentuk puncak skor di 6.*

**B. Logical Cleaning via CSV (Tahap 3 Notebook)**
Membuang gambar cacat label (`NormalXXXX.png`) dari metadata tanpa merusak file Windows aslinya.

**C. Stratified Validation Split & Class Weights (Tahap 5 Notebook)**
* Dataset dipecah menjadi **Train (60.6%), Validation (15.2%), Test (24.2%)** tanpa *Data Leakage*.
* **Augmentasi Offline Dibatalkan** agar dataset tetap alami (180.726).
* Ketidakseimbangan data ditangani murni menggunakan nilai **`class_weight`** yang dikalkulasi menggunakan Scikit-Learn.

---

### Tahap 4 — Output: Final Dataset & Handover
File `master_dataset_final.csv` adalah output akhir *pipeline* yang akan di-training oleh ***AI Engineer***.

| Kolom | Deskripsi |
|---|---|
| `image_path` | Jalur absolut lokasi file gambar |
| `split` | `Train`, `Validation`, atau `Test` |
| `folder_category` | Kategori sumber: `Normal`, `Corrected`, `Reversal` |
| `severity_score` | Skor keparahan disleksia regresif (0 Sehat — 6 Ekstrem) |
| `target_class` | Target KLASIFIKASI BINER (0 Normal vs 1 Disleksia) |

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
- [x] Identifikasi Severity Score & Skala Asli
- [x] Deteksi kontaminasi label (`NormalXXXX.png`)
- [x] Logical Cleaning via Pandas DataFrame
- [x] Normalisasi skala severity (Dictionary Mapping → 0–6)
- [x] Generate `master_dataset_dyslexia.csv`
- [x] Exploratory Data Analysis & Explanatory Analysis Visual
- [x] Stratified Split Dataset (Train, Val, Test) tanpa *Leakage*
- [x] Kalkulasi Parameter `class_weight` Murni (Zero Data Loss)
- [x] Dokumentasi Data Dictionary & Strategy Blueprint
- [x] Handover Endpoint CSV: `master_dataset_final.csv`

Status keseluruhan dapat dilihat di file `Data Scientist Checklist.md`.
---

## 👤 Kontributor

| Nama | Role | Fokus |
|---|---|---|
| Rainy | Data Scientist | Dataset preparation, preprocessing, EDA |
| w0pal | *(Anggota Tim)* | *(sesuai pembagian tugas)* |

---

## 📄 Lisensi & Dataset
Dataset `Gambo` adalah dataset publik. Harap perhatikan lisensi asli dataset sebelum mendistribusikan ulang.
https://www.kaggle.com/datasets/drizasazanitaisa/dyslexia-handwriting-dataset\\
Dataset `EMNIST` adalah dataset publik.
https://www.kaggle.com/datasets/crawford/emnist
1. M. S. A. B. Rosli, I. S. Isa, S. A. Ramlan, S. N. Sulaiman and M. I. F. Maruzuki, "Development of CNN Transfer Learning for Dyslexia Handwriting Recognition," 2021 11th IEEE International Conference on Control System, Computing and Engineering (ICCSCE), 2021, pp. 194-199, doi: 10.1109/ICCSCE52189.2021.9530971.
2. N. S. L. Seman, I. S. Isa, S. A. Ramlan, W. Li-Chih and M. I. F. Maruzuki, "Notice of Removal: Classification of Handwriting Impairment Using CNN for Potential Dyslexia Symptom," 2021 11th IEEE International Conference on Control System, Computing and Engineering (ICCSCE), 2021, pp. 188-193, doi: 10.1109/ICCSCE52189.2021.9530989.
3. Isa, Iza Sazanita. CNN Comparisons Models On Dyslexia Handwriting Classification / Iza Sazanita Isa … [et Al.]. Universiti Teknologi MARA Cawangan Pulau Pinang, 2021.
4. Isa, I. S., Rahimi, W. N. S., Ramlan, S. A., & Sulaiman, S. N. (2019). Automated detection of dyslexia symptom based on handwriting image for primary school children. Procedia Computer Science, 163, 440-449.
