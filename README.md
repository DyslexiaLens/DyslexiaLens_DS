# 🧠 DyslexiaLens — Data Science & XAI Repository

> Bagian Data Science dari Capstone Project **DyslexiaLens**: Intelligent Handwriting Detection and Assistance for Dyslexia.
>
> Repositori ini berisi seluruh proses kerja Data Scientist, mulai dari eksplorasi dan audit dataset, pembersihan data (*Data Wrangling*), pemecahan masalah *Class Imbalance* menggunakan injeksi eksternal (**EMNIST**), perumusan fitur *Explainable AI* (XAI), hingga pembuatan *Streamlit Executive Dashboard*.

---

## 📌 Tentang Proyek

**DyslexiaLens** adalah sistem *early screening* disleksia berbasis analisis citra tulisan tangan. Sistem ini **bukan alat diagnosis medis**, melainkan alat bantu skrining awal yang dapat digunakan oleh orang tua dan pendidik sebelum pemeriksaan klinis lebih lanjut.

Pada repositori ini, fokus utama adalah membangun **Pondasi Data yang Kokoh** dan memastikan AI yang dibangun nantinya tidak menjadi *"Black Box"* (memiliki kapabilitas dapat dijelaskan/diinterpretasi).

| Detail | Keterangan |
|---|---|
| **Tema** | Accessible & Adaptive Learning |
| **Fokus Utama** | Data Engineering, Feature Engineering (XAI), & Dashboarding |
| **Dataset Primer** | Gambo (Handwriting Dyslexia Dataset) |
| **Dataset Sekunder** | EMNIST (Digunakan untuk injeksi ekuilibrium kelas Normal) |
| **Total Sampel (Balanced)** | ~273.000 gambar (Rasio 1:1 Normal vs Disleksia) |
| **Aplikasi Presentasi** | Streamlit Interactive Dashboard (`app.py`) |

---

## 🗂️ Struktur Repositori Terkini

```text
Dataset Disleksia/
│
├── 📊 app.py                       # Streamlit Executive Dashboard (UI/UX)
├── 📁 assets/                      # Aset visual EDA untuk Streamlit
│   ├── EMNIST/                     # Grafik dataset augmentasi
│   └── noAugmentation/             # Grafik dataset murni
│
├── 📁 csv_metadata/                # Output tabular final (Siap Training!)
│   ├── Dataset_Dyslexia_EMNIST_FeatureEngineering.csv
│   └── dyslexialens_test_EMNIST.csv.gz (Compressed Pixel Viewer)
│
├── 📁 notebooks/
│   ├── 📓 Dyslexia_EMNIST.ipynb    # Notebook utama pipeline EMNIST
│   ├── 📓 Dyslexia_NoAugment.ipynb # Notebook utama pipeline murni
│
├── 📁 Python Stuff/                # Script utilitas Python (Legacy)
└── 📁 Dokumentasi/                 # Catatan diskusi dan audit historis
```

---

## 🔬 Alur Kerja Data Science (Pipeline)

### Tahap 1 — Audit Kritis & Normalisasi
Ditemukan dua anomali kritis pada dataset publik Gambo:
1. **Sistem Severity Score Terbalik:** Folder numerik (`1-9`) ternyata bukan karakter angka, melainkan skala keparahan tulisan. Kami menormalisasinya menjadi skala linear `0` (Normal) hingga `6` (Paling Parah).
2. **Kontaminasi Label:** Ditemukan file `NormalXXXX.png` yang terselip di dalam folder disleksia. Masalah ini diselesaikan melalui *Logical Cleaning* menggunakan metode *Boolean Masking* di Pandas.

### Tahap 2 — Resolusi "Class Imbalance"
Dataset murni Gambo memiliki ketimpangan ekstrem di mana kelas *Disleksia* jauh lebih banyak dari *Normal*.
*   **Solusi:** Kami melakukan injeksi data dari dataset eksternal (**EMNIST**) secara deterministik menggunakan algoritma *Fair Pruning* (Top-Down Indexing).
*   **Hasil:** Tercapai titik ekuilibrium **1:1** (~142.000 Disleksia vs ~131.000 Normal), sehingga mencegah model AI dari kerentanan *Majority Class Bias*.

### Tahap 3 — Feature Engineering (Membangun XAI)
Untuk memastikan arsitektur *Late Fusion CNN* kelak memiliki kemampuan **Explainable AI (XAI)**, kami mengekstrak 5 fitur matematis-geometri dari setiap matriks 28x28 piksel:
1.  `ink_density`: Mendeteksi indikasi *Over-tracing* (coretan ragu-ragu/berulang).
2.  `center_of_mass_x` & `y`: Mendeteksi pergeseran spasial ekstrem.
3.  `bounding_box_ratio`: Mendeteksi distorsi proporsi dimensi huruf.
4.  `stroke_transitions`: Menghitung frekuensi getaran/tremor motorik saat menulis.
5.  `horizontal_symmetry`: Indikator pendeteksi utama untuk *Reversal* (tulisan terbalik).

### Tahap 4 — Executive Dashboarding
Membuat aplikasi *Streamlit* untuk menjawab 4 Pertanyaan Bisnis utama secara interaktif dan mempresentasikan hasil *Computer Vision Analytics* (Heatmap) serta Profil Klinis (KDE Plots) kepada *stakeholders*.

---

## 🚀 Cara Menjalankan Dashboard

Untuk mempresentasikan hasil pipeline ini secara interaktif, jalankan perintah berikut di terminal:

```bash
pip install streamlit pandas numpy matplotlib
streamlit run app.py
```
*Gunakan toggle di sidebar untuk melihat perbedaan analitik antara dataset Murni (No Augmentation) dan dataset Augmentasi (EMNIST).*

---

## 📋 Checklist Progres Akhir Data Scientist

- [x] Eksplorasi dan audit anomali dataset `Gambo`
- [x] Logical Cleaning & Normalisasi Skala Keparahan (1-6)
- [x] Injeksi EMNIST & Algoritma Fair Pruning untuk Balancing (Rasio 1:1)
- [x] Computer Vision Analytics (Variance & Difference Heatmaps)
- [x] Feature Engineering 5 Variabel Matematis Geometri (XAI)
- [x] Stratified Split Dataset (Train, Test) untuk mencegah Data Leakage
- [x] Ekspor *Compressed Pixel CSV* (`.csv.gz`) untuk *viewer* statis
- [x] Pembuatan Executive Dashboard interaktif dengan Streamlit
- [x] Standardisasi Dokumentasi Markdown (*Handover Ready*)

**Status: 100% COMPLETE. SIAP DISERAHKAN KE TIM AI ENGINEER.**

---

## 👤 Kontributor

| Nama | Role | Fokus |
|---|---|---|
| Rainy | Data Scientist | Dataset Auditing, Data Wrangling, Stratified Splitting, XAI Feature Engineering, & Dashboarding Streamlit |
| w0pal | Data Scientist | EMNIST-GAMBO Integration (Balancing), Metadata Construction, & Pipeline Automation |

---

## 📄 Lisensi & Referensi Dataset
*   Dataset **Gambo**: Publik (https://www.kaggle.com/datasets/drizasazanitaisa/dyslexia-handwriting-dataset)
*   Dataset **EMNIST**: Publik (https://www.kaggle.com/datasets/crawford/emnist)

*(Hak cipta dan kredit penelitian asli tetap mengacu pada author paper Gambo dan EMNIST).*