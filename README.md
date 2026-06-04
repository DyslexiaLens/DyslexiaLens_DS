<div align="center">
  <img src="Assets/Logo DyslexiaLens.png" alt="DyslexiaLens Logo" width="120"/>

  # 🧠 DyslexiaLens Data Science & XAI Repository

  [![Python](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/streamlit-1.45+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![Pandas](https://img.shields.io/badge/pandas-2.0+-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
  [![NumPy](https://img.shields.io/badge/numpy-1.24+-013243.svg?logo=numpy&logoColor=white)](https://numpy.org/)
  [![SciPy](https://img.shields.io/badge/scipy-1.10+-0C55A5.svg?logo=scipy&logoColor=white)](https://scipy.org/)
</div>

> Bagian Data Science dari Capstone Project **DyslexiaLens**: Intelligent Handwriting Detection and Assistance for Dyslexia.
>
> Repositori ini berisi seluruh proses kerja Data Scientist: dari audit & *wrangling* dataset, pemecahan *Class Imbalance* via injeksi **EMNIST**, validasi keamanan melalui **A/B Testing** (Mann-Whitney & Cohen's d), perumusan 6 fitur **Explainable AI (XAI)**, hingga pembuatan *Streamlit Executive Dashboard* dan penyusunan **Laporan Teknis 51 Halaman** sebagai SLA Handover untuk tim AI Engineer.
>
> **🏁 Status: 100% COMPLETE! Fase Data Science resmi ditutup dan diserahterimakan.**

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
| **Aplikasi Presentasi** | Streamlit Interactive Dashboard (`Dashboard.py`) |
| **Dokumentasi Final** | `Laporan Teknis/Laporan Teknis Komprehensif Final.md` |

---

## 🗂️ Struktur Repositori

```text
Dataset Disleksia/
│
├── 📊 Dashboard.py                  # Streamlit Executive Dashboard (Entry Point)
├── 📄 requirements.txt              # Daftar dependency Python
├── 📄 .gitignore                    # Konfigurasi file yang diabaikan Git
├── 📄 README.md                     # Dokumentasi utama repositori (file ini)
│
├── 📁 Assets/                       # Aset visual EDA untuk Streamlit & Laporan
│   ├── Styles.css                   # Custom CSS untuk Dashboard
│   ├── EMNIST/                      # Grafik dataset augmentasi & A/B Testing
│   └── noAugmentation/              # Grafik dataset murni
│
├── 📁 Data/                         # Output tabular final (Siap Training!)
│   ├── Dataset_Dyslexia_NoAugmentation_FeatureEngineering.csv
│   ├── Dataset_Dyslexia_EMNIST_FeatureEngineering.csv
│   ├── Testset_Dyslexia_NoAugmentation.csv.gz
│   └── Testset_Dyslexia_EMNIST.csv.gz
│
├── 📁 Laporan Teknis/               # 🌟 Dokumen Final & SLA Handover
│   └── Laporan Teknis Komprehensif - CC26-PSU052.pdf
│
├── 📁 Notebooks/                    # Notebook Eksperimen & Pipeline
│   ├── 📓 AB_Testing.ipynb          # Validasi A/B Testing (Mann-Whitney & Cohen's d)
│   ├── 📓 Dyslexia_EMNIST.ipynb     # Pipeline EMNIST
│   ├── 📓 Dyslexia_NoAugment.ipynb  # Pipeline murni (tanpa augmentasi)
│   └── 📓 EMNIST_to_Gambo.ipynb     # Penggabungan EMNIST dan Gambo
│
└── 📁 Dokumentasi/                  # Log & Catatan Kerja Tim
    ├── 📁 Rainy/                    # Checkpoint sesi & Data Scientist Checklist
    └── 📁 w0pal/                    # Dokumen Handover Data Scientist
```

> **Catatan:** Proyek ini tidak memerlukan file environment variables (`.env`). Semua konfigurasi bersifat statis dan tidak mengandung credential rahasia.

---

## 🚀 Setup Environment & Cara Menjalankan

### Prasyarat
- **Python** 3.10 atau lebih baru
- **pip** (Python package manager)

### Langkah-langkah

**1. Clone repositori ini**
```bash
git clone https://github.com/<username>/DyslexiaLens-DataScience.git
cd DyslexiaLens-DataScience
```

**2. Buat dan aktifkan virtual environment**
```bash
# Membuat virtual environment
python -m venv .venv

# Aktivasi (Windows)
.venv\Scripts\activate

# Aktivasi (macOS/Linux)
source .venv/bin/activate
```

**3. Install seluruh dependency**
```bash
pip install -r requirements.txt
```

**4. Jalankan Dashboard**
```bash
streamlit run Dashboard.py
```

> 💡 Gunakan **toggle di sidebar** untuk membandingkan analitik antara dataset **Murni (Gambo)** dan dataset **Augmentasi yang tervalidasi (Gambo + EMNIST)**.

> 📓 **Notebook:** Seluruh notebook di folder `Notebooks/` dijalankan secara lokal menggunakan **Jupyter Notebook** dengan library tambahan: `seaborn` dan `scipy`.

---

## 🔬 Alur Kerja Data Science (Berdasarkan Laporan Teknis)

Seluruh pengerjaan pada repositori ini terdokumentasi rapi di dalam file **`Laporan Teknis/Laporan Teknis Komprehensif Final.md`** yang memuat 8 Bab utama:

### Bab 2 & 3: Audit & Logical Cleaning
Ditemukan 3 anomali kritis pada dataset publik Gambo:
1. **Class Imbalance:** Rasio 3.35:1 (Disleksia sangat mendominasi).
2. **Label Noise:** Ratusan data Normal tersesat di folder Disleksia (dan sebaliknya) yang dibersihkan via Pandas.
3. **Sistem Severity Score Cacat:** Skala asli (9=Ringan, 1=Parah) dibalik, dan skor ekstrem (4 dan 1) digabungkan menjadi skor **6 (Paling Parah)** guna menjaga kontinuitas Ordinal (0=Normal, 1-6=Ringan-Parah).

### Bab 4:  Feature Engineering (Membangun 6 Fitur XAI)
Untuk memastikan arsitektur *Late Fusion CNN* kelak memiliki kemampuan **Explainable AI (XAI)**, kami mengekstrak 6 fitur matematis secara *stateless* (per gambar) agar terhindar dari *Data Leakage*:
1. `stroke_density`: Mendeteksi *Over-tracing* (coretan ragu-ragu/berulang).
2. `center_of_mass_x`: Distorsi spasial horizontal.
3. `center_of_mass_y`: Distorsi spasial vertikal.
4. `bounding_box_ratio`: Inkonsistensi proporsi huruf akibat kontrol motorik lemah.
5. `stroke_transitions`: Menghitung frekuensi getaran (*tremor*) berupa garis bergerigi.
6. `horizontal_symmetry`: Indikator klinis terkuat untuk disleksia orientasi (*Reversal/Mirroring*).

### Bab 5: EDA & Dashboarding
Membuktikan secara empiris (menggunakan *Variance Heatmap* dan *KDE Plot*) bahwa pola visual disleksia benar-benar nyata (inkonsistensi spasial tinggi) dan mampu membedakan sub-tipe disleksia (Corrected vs Reversal). Di-deploy dalam bentuk Streamlit.

### Bab 6: Strategi Augmentasi & A/B Testing
Augmentasi spasial (seperti rotasi dan flip) **diharamkan** karena mengubah orientasi adalah gejala penyakit itu sendiri (huruf 'b' dirotasi jadi 'p').
* **Solusi:** Injeksi data **EMNIST** dikombinasi algoritma *Fair Pruning* untuk men-*downgrade* mayoritas.
* **Hasil:** Ekuilibrium rasio **1.00:1** (~102.394 Disleksia vs ~102.439 Normal) dari sebelumnya 3.35:1.
* **Validasi (A/B Testing):** Walaupun *Mann-Whitney U Test* mendeteksi perbedaan statistik (akibat *Large N Effect* pada >150k sampel), evaluasi **Cohen's d** membuktikan seluruh 6 fitur memiliki |d| < 0.2 (*Negligible*). Ini membuktikan injeksi EMNIST aman secara klinis dan tidak merusak "DNA" asli tulisan disleksia. Hasil ini divisualisasikan melalui *KDE Overlay* di **Tab 5 Dashboard**.

### Bab 7 & 8: Penyiapan Data & Action Items
* Melakukan **Stratified Splitting (70/15/15)**.
* Membangun **Data Dictionary**.
* Merumuskan 3 Aturan Mutlak (*MUST NOT*) untuk AI Engineer (misal: dilarang menggunakan *MSE Loss* untuk memprediksi Severity Score karena sifatnya *Ordinal*).

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
- [x] Standardisasi Dokumentasi MLOps & SLA Kontrak (Bab 8)
- [x] Penyusunan Laporan Teknis Komprehensif PDF siap sidang (51 Halaman)

**🏁 Status: 100% COMPLETE! SLA KONTRAK DATA RESMI DISERAHKAN KE TIM AI ENGINEER.**

---

## 👤 Kontributor

| Nama | Role | Fokus Utama |
|---|---|---|
| Rainy | Data Scientist | Dataset Auditing, Logical Cleaning, Stratified Splitting, XAI Feature Engineering, A/B Testing & Dashboarding Streamlit |
| w0pal | Data Scientist | EMNIST-GAMBO Integration (Fair Pruning Balancing), Metadata Construction, Pipeline Automation, & Dashboarding Streamlit |

---

## 📄 Sitasi & Referensi Dataset

Sesuai dengan lisensi publikasi dataset asli, penggunaan data pada proyek ini memberikan kredit penuh kepada para peneliti berikut:

**Dataset Gambo (Dyslexia Handwriting Dataset):**
* 🔗 **Sumber:** [Kaggle: Dyslexia Handwriting Dataset](https://www.kaggle.com/datasets/drizasazanitaisa/dyslexia-handwriting-dataset)
1. M. S. A. B. Rosli, I. S. Isa, S. A. Ramlan, S. N. Sulaiman and M. I. F. Maruzuki, *"Development of CNN Transfer Learning for Dyslexia Handwriting Recognition,"* 2021 11th IEEE International Conference on Control System, Computing and Engineering (ICCSCE), 2021, pp. 194-199, doi: 10.1109/ICCSCE52189.2021.9530971.
2. N. S. L. Seman, I. S. Isa, S. A. Ramlan, W. Li-Chih and M. I. F. Maruzuki, *"Notice of Removal: Classification of Handwriting Impairment Using CNN for Potential Dyslexia Symptom,"* 2021 11th IEEE International Conference on Control System, Computing and Engineering (ICCSCE), 2021, pp. 188-193, doi: 10.1109/ICCSCE52189.2021.9530989.
3. Isa, Iza Sazanita. *"CNN Comparisons Models On Dyslexia Handwriting Classification / Iza Sazanita Isa … [et Al.]."* Universiti Teknologi MARA Cawangan Pulau Pinang, 2021.
4. Isa, I. S., Rahimi, W. N. S., Ramlan, S. A., & Sulaiman, S. N. (2019). *"Automated detection of dyslexia symptom based on handwriting image for primary school children."* Procedia Computer Science, 163, 440-449.

**Dataset EMNIST:**
* 🔗 **Sumber:** [Kaggle: EMNIST](https://www.kaggle.com/datasets/crawford/emnist)
1. Cohen, G., Afshar, S., Tapson, J., & van Schaik, A. (2017). *"EMNIST: an extension of MNIST to handwritten letters."* Retrieved from http://arxiv.org/abs/1702.05373

*(Repositori ini adalah implementasi akademik turunan (Capstone Project) dan bukan pemilik properti intelektual dari dataset raw di atas).*