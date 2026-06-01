# 🧠 DyslexiaLens — Data Science & XAI Repository

> Bagian Data Science dari Capstone Project **DyslexiaLens**: Intelligent Handwriting Detection and Assistance for Dyslexia.
>
> Repositori ini berisi seluruh proses kerja Data Scientist: dari audit & *wrangling* dataset, pemecahan *Class Imbalance* via injeksi **EMNIST**, validasi keamanan melalui **A/B Testing** (Mann-Whitney & Cohen's d), perumusan 6 fitur **Explainable AI (XAI)**, hingga pembuatan *Streamlit Executive Dashboard* dan penyusunan **Laporan Teknis 51 Halaman** sebagai SLA Handover untuk tim AI Engineer.
>
> **🏁 Status: 100% COMPLETE — Fase Data Science resmi ditutup dan diserahterimakan.**

---

## 📌 Tentang Proyek

**DyslexiaLens** adalah sistem *early screening* disleksia berbasis analisis citra tulisan tangan. Sistem ini **bukan alat diagnosis medis**, melainkan alat bantu skrining awal yang dapat digunakan oleh orang tua dan pendidik sebelum pemeriksaan klinis lebih lanjut.

Pada repositori ini, fokus utama adalah membangun **Pondasi Data yang Kokoh** dan memastikan AI yang dibangun nantinya tidak menjadi *"Black Box"* (memiliki kapabilitas dapat dijelaskan/diinterpretasi).

| Detail | Keterangan |
|---|---|
| **Tema** | Accessible & Adaptive Learning |
| **Fokus Utama** | Data Engineering, Feature Engineering (XAI), MLOps Preparation & Dashboarding |
| **Dataset Primer** | Gambo (Handwriting Dyslexia Dataset) |
| **Dataset Sekunder** | EMNIST (Digunakan untuk injeksi ekuilibrium kelas Normal) |
| **Total Sampel (Balanced)** | ~204.833 gambar (Rasio 1:1 Normal vs Disleksia) |
| **Aplikasi Presentasi** | Streamlit Interactive Dashboard (`app.py`) |
| **Dokumentasi Final** | Laporan Teknis/Final.md (SLA Handover to AI Engineer) |

---

## 🗂️ Struktur Repositori Terkini

```text
Dataset Disleksia/
│
├── 📊 app.py                       # Streamlit Executive Dashboard (UI/UX)
├── 📁 Assets/                      # Aset visual EDA untuk Streamlit & Laporan
│   ├── EMNIST/                     # Grafik dataset augmentasi & A/B Testing
│   └── noAugmentation/             # Grafik dataset murni
│
├── 📁 Data/                                 # Output tabular final (Siap Training!)
│   ├── Dataset_Dyslexia_EMNIST_FeatureEngineering.csv
│   └── Testset_Dyslexia_EMNIST.csv.gz (Compressed Pixel Viewer)
│
├── 📁 Notebooks/
│   ├── 📓 AB_Testing.ipynb                    # Notebook validasi A/B Testing (Mann-Whitney & Cohen's d)
│   ├── 📓 Dyslexia_EMNIST.ipynb               # Notebook utama pipeline EMNIST
│   ├── 📓 Dyslexia_NoAugment.ipynb            # Notebook utama pipeline murni
│   ├── 📓 EMNIST_to_Gambo.ipynb               # Notebook penggabungan dataset EMNIST dan Gambo
│
├── 📁 Dokumentasi/Laporan Teknis/             # 🌟 SINGLE SOURCE OF TRUTH DOKUMENTASI
│   └── 📑 Laporan Teknis Komprehensif Final.pdf  # Versi PDF siap sidang (51 Halaman)
```

---

## 🔬 Alur Kerja Data Science (Berdasarkan Laporan Teknis)

Seluruh pengerjaan pada repositori ini terdokumentasi rapi di dalam file **`Dokumentasi/Laporan Teknis/Final.md`** yang memuat 8 Bab utama:

### Bab 2 & 3 — Audit & Logical Cleaning
Ditemukan 3 anomali kritis pada dataset publik Gambo:
1. **Class Imbalance:** Rasio 3.35:1 (Disleksia sangat mendominasi).
2. **Label Noise:** Ratusan data Normal tersesat di folder Disleksia (dan sebaliknya) yang dibersihkan via Pandas.
3. **Sistem Severity Score Cacat:** Skala asli (9=Ringan, 1=Parah) dibalik, dan skor ekstrem (4 dan 1) digabungkan menjadi skor **6 (Paling Parah)** guna menjaga kontinuitas Ordinal (0=Normal, 1-6=Ringan-Parah).

### Bab 4 — Feature Engineering (Membangun 6 Fitur XAI)
Untuk memastikan arsitektur *Late Fusion CNN* kelak memiliki kemampuan **Explainable AI (XAI)**, kami mengekstrak 6 fitur matematis secara *stateless* (per gambar) agar terhindar dari *Data Leakage*:
1. `stroke_density`: Mendeteksi *Over-tracing* (coretan ragu-ragu/berulang).
2. `center_of_mass_x`: Distorsi spasial horizontal.
3. `center_of_mass_y`: Distorsi spasial vertikal.
4. `bounding_box_ratio`: Inkonsistensi proporsi huruf akibat kontrol motorik lemah.
5. `stroke_transitions`: Menghitung frekuensi getaran (*tremor*) berupa garis bergerigi.
6. `horizontal_symmetry`: Indikator klinis terkuat untuk disleksia orientasi (*Reversal/Mirroring*).

### Bab 5 — EDA & Dashboarding
Membuktikan secara empiris (menggunakan *Variance Heatmap* dan *KDE Plot*) bahwa pola visual disleksia benar-benar nyata (inkonsistensi spasial tinggi) dan mampu membedakan sub-tipe disleksia (Corrected vs Reversal). Di-deploy dalam bentuk Streamlit.

### Bab 6 — Strategi Augmentasi & A/B Testing
Augmentasi spasial (seperti rotasi dan flip) **diharamkan** karena mengubah orientasi adalah gejala penyakit itu sendiri (huruf 'b' dirotasi jadi 'p').
* **Solusi:** Injeksi data **EMNIST** dikombinasi algoritma *Fair Pruning* untuk men-*downgrade* mayoritas.
* **Hasil:** Ekuilibrium rasio **1.00:1** (~102.394 Disleksia vs ~102.439 Normal) dari sebelumnya 3.35:1.
* **Validasi (A/B Testing):** Walaupun *Mann-Whitney U Test* mendeteksi perbedaan statistik (akibat *Large N Effect* pada >150k sampel), evaluasi **Cohen's d** membuktikan seluruh 6 fitur memiliki |d| < 0.2 (*Negligible*). Ini membuktikan injeksi EMNIST aman secara klinis dan tidak merusak "DNA" asli tulisan disleksia. Hasil ini divisualisasikan melalui *KDE Overlay* di **Tab 5 Dashboard**.

### Bab 7 & 8 — Penyiapan Data & Action Items
* Melakukan **Stratified Splitting (70/15/15)**.
* Membangun **Data Dictionary**.
* Merumuskan 3 Aturan Mutlak (*MUST NOT*) untuk AI Engineer (misal: dilarang menggunakan *MSE Loss* untuk memprediksi Severity Score karena sifatnya *Ordinal*).

---

## 🚀 Cara Menjalankan Dashboard

Untuk mempresentasikan hasil pipeline ini secara interaktif, jalankan perintah berikut di terminal:

```bash
pip install streamlit pandas numpy matplotlib
streamlit run app.py
```
*Gunakan toggle di sidebar untuk melihat perbedaan analitik antara dataset Murni (Gambo) dan dataset Augmentasi yang tervalidasi (Gambo + EMNIST).*

---

## 📋 Checklist Progres Akhir Data Scientist

- [x] Eksplorasi dan audit anomali dataset `Gambo` (Bab 2)
- [x] Logical Cleaning & Normalisasi Skala Keparahan Ordinal (Bab 3)
- [x] Feature Engineering **6 Fitur** Matematis Geometri XAI (Bab 4)
- [x] Computer Vision Analytics (Variance & Difference Heatmaps) (Bab 5)
- [x] Injeksi EMNIST & Algoritma Fair Pruning untuk Balancing (Bab 6)
- [x] Validasi Keamanan Augmentasi via **A/B Testing** (Mann-Whitney U & Cohen's d) (Bab 6)
- [x] Stratified Split (70/15/15) bebas Data Leakage (Bab 7)
- [x] Ekspor *Compressed Pixel CSV* (`.csv.gz`) untuk memori dashboard efisien
- [x] Pembuatan Executive Dashboard interaktif dengan Streamlit (Tab 1-6 termasuk Tab A/B Testing)
- [x] Standardisasi Dokumentasi MLOps & SLA Kontrak (*Final.md*) (Bab 8)
- [x] Penyusunan Laporan Teknis Komprehensif PDF siap sidang (51 Halaman)

**🏁 Status: 100% COMPLETE — SLA KONTRAK DATA RESMI DISERAHKAN KE TIM AI ENGINEER.**

---

## 👤 Kontributor

| Nama | Role | Fokus Utama |
|---|---|---|
| Rainy | Data Scientist | Dataset Auditing, Logical Cleaning, Stratified Splitting, XAI Feature Engineering, A/B Testing & Dashboarding Streamlit |
| w0pal | Data Scientist | EMNIST-GAMBO Integration (Fair Pruning Balancing), Metadata Construction, Pipeline Automation, & Dashboarding Streamlit |

---

## 📄 Lisensi & Referensi Dataset
* Dataset **Gambo**: Publik — [Kaggle: Dyslexia Handwriting Dataset](https://www.kaggle.com/datasets/drizasazanitaisa/dyslexia-handwriting-dataset)
* Dataset **EMNIST**: Publik — [Kaggle: EMNIST](https://www.kaggle.com/datasets/crawford/emnist)

*(Hak cipta dan kredit penelitian asli tetap mengacu pada author paper Gambo dan EMNIST).*