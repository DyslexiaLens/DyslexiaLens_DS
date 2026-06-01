# 📋 Dokumen Konteks Handover — DyslexiaLens Data Science Pipeline
**Dibuat:** 1 Juni 2026  
**Tujuan:** Memberikan konteks penuh kepada AI Agent berikutnya terkait seluruh pekerjaan yang telah diselesaikan oleh tim Data Scientist (Rainy & w0pal) pada proyek Capstone DyslexiaLens.  
**Status Proyek:** ✅ FASE DATA SCIENCE — 100% COMPLETE & DELIVERED

---

## 🗂️ Profil Proyek

**Nama Proyek:** DyslexiaLens  
**Jenis:** Capstone Project Dicoding Semester 6  
**Tujuan Produk:** Aplikasi web berbasis AI untuk *early screening* (bukan diagnosis medis) indikasi disleksia pada tulisan tangan anak. Sistem ini memberikan skor keparahan (Severity 0–6) pada tiap karakter tulisan.  
**Disclaimer Klinis (WAJIB DIKETAHUI):** Sistem ini adalah alat bantu skrining awal. **BUKAN** alat diagnosis medis. Tidak menggantikan evaluasi psikolog atau dokter.

**Pembagian Tim (Data Science):**
- **Rainy** — Lead Data Scientist: Dataset Auditing, Data Wrangling, Feature Engineering (XAI), Stratified Splitting, Dashboard Development, A/B Testing, Laporan Teknis.
- **w0pal** — Data Engineer: EMNIST-Gambo Integration (inisiatif awal), Metadata Construction, Pipeline Automation.

---

## 🗃️ Sumber Dataset

### Dataset Primer: Gambo
- **Sumber:** Kaggle (dataset tulisan tangan disleksia "Gambo")
- **Struktur asli:** Folder `Train/` dan `Test/` → sub-folder `Normal/`, `Corrected/`, `Reversal/` → sub-folder numerik `1, 4, 5, 6, 7, 8, 9` (bukan angka, melainkan kode keparahan)
- **Format:** File `.png`, resolusi 28×28 atau 29×29 piksel, Grayscale/Binary
- **Jumlah awal:** 208.372 gambar total
- **Tiga Kelas Utama:**
  - `Normal` — tulisan tangan tanpa indikasi disleksia
  - `Corrected` — tulisan dengan koreksi berlebihan (coretan ulang)
  - `Reversal` — tulisan dengan pembalikan huruf (b↔d, p↔q), indikasi medis utama disleksia

### Dataset Sekunder: EMNIST ByClass
- **Sumber:** NIST (EMNIST dataset, subset ByClass)
- **Konten:** Karakter digital A–Z dan a–z (data karakter "normal sehat")
- **Fungsi dalam proyek:** Penyeimbang kelas untuk mengatasi Class Imbalance ekstrem di Gambo

---

## ⚠️ Temuan Kritis & Keputusan Arsitektural (PENTING DIBACA)

### 1. Sistem Severity Score yang Terbalik
- Folder numerik di Gambo (1, 4, 5, 6, 7, 8, 9) **BUKAN** representasi karakter angka, melainkan kode **Tingkat Keparahan Goresan (Severity Score)**.
- Skala asli **terbalik**: `1` = Paling Parah, `9` = Paling Ringan.
- **Koreksi yang diterapkan:** Skala dinormalisasi menjadi **0 (Normal/Sehat) → 6 (Paling Parah)**

| Skor Asli | Skor AI Final | Makna |
|---|---|---|
| `Normal` | **0** | Bebas Disleksia |
| `9` | **1** | Paling Ringan |
| `8` | **2** | |
| `7` | **3** | |
| `6` | **4** | |
| `5` | **5** | |
| `4` | **6** | Corrected Paling Parah |
| `1` | **6** | Reversal Paling Parah (digabung dengan Corrected di skor 6) |

### 2. Paradoks OCR (CRITICAL — Baca Sebelum Training Model)
- Model DyslexiaLens yang dilatih dari dataset Gambo **TIDAK BERTUGAS meng-OCR atau menerjemahkan abjad**.
- Jika OCR biasa dipakai: tulisan Reversal "b" yang mirip "d" akan dilabeli "d" secara salah, merusak training.
- **Output model:** Murni sebagai **Diagnostic Tool** — menilai Severity Score (0–6) dari pola goresan, bukan mengenali abjad.
- Untuk fitur translasi abjad di aplikasi, tim AI Engineer harus memilih salah satu dari dua arsitektur:
  - **Opsi A (Golden MVP):** Grid kertas terstruktur — OpenCV potong koordinat absolut, model hanya evaluasi kotak per kotak. (Cepat, Aman)
  - **Opsi B (Tandem Pipeline):** Google Vision OCR + NLP AutoCorrect → model DyslexiaLens beri label merah. (Kompleks, nilai plus)

### 3. Larangan Augmentasi Spasial (DILARANG KERAS)
- **DILARANG:** Rotasi, flip horizontal/vertikal, atau transformasi spasial apapun pada gambar training.
- **Alasan:** Augmentasi spasial akan menghancurkan sinyal *Reversal Error* (huruf terbalik b↔d, p↔q) yang merupakan indikasi medis utama disleksia. Model akan kehilangan kemampuan mendeteksi pembalikan huruf.
- Augmentasi yang **DIIZINKAN** (opsional, on-the-fly di training): brightness adjustment, noise ringan.

### 4. Metrik Training yang WAJIB Digunakan
- **GUNAKAN:** `Weighted F1-Score` sebagai metrik utama.
- **JANGAN:** Gunakan `Accuracy` semata — menyesatkan karena data tetap memiliki kemiringan distribusi.
- **JANGAN:** Gunakan `MSE Loss` untuk target ordinal Severity Score. Gunakan `Cross-Entropy` atau `Ordinal Loss`.

---

## 📅 Perjalanan Checkpoint 1–11

### ✅ Checkpoint 1 — Audit & Logical Cleaning (18 April 2026)
**Pencapaian utama:**
- Audit menyeluruh seluruh 208.372 file: 0 file corrupt, format 100% konsisten PNG grayscale 28×28.
- Penemuan sistem Severity Score yang terbalik → merancang Dictionary Mapping koreksi.
- Penemuan *Label Noise* dua arah: file `NormalXXXX.png` tersesat di folder Disleksia, dan kelas Normal juga mengandung sampel bergoresan anomali.
- Implementasi *Logical Cleaning* via Pandas Boolean Masking (filter berdasarkan nama file, tanpa hapus fisik).
- Generate `master_dataset_dyslexia.csv` dengan ~180.726 baris data bersih.
- Membuat `Dyslexia.ipynb` sebagai notebook preprocessing utama dengan *Dual-Path Logic* (berjalan dengan atau tanpa rename fisik).
- **Artefak:** `master_dataset_dyslexia.csv`, `Dyslexia.ipynb`, berbagai dokumentasi MD.

### ✅ Checkpoint 2 — Refinement & Integrity Sync (18 April 2026)
**Pencapaian utama:**
- Restrukturisasi notebook menjadi tahapan naratif logis (Header Bisnis → Audit → Cleaning → EDA).
- Implementasi *Dual-Path Logic* untuk reproducibility di Google Colab.
- Konfirmasi temuan *Two-Way Label Noise* dan penetapan CSV sebagai satu-satunya sumber kebenaran.
- Sinkronisasi penuh `DATA_SCIENTIST_CHECKLIST.md` dengan implementasi nyata.

### ✅ Checkpoint 3 — EDA, Explanatory Analysis & Stratified Split (19 April 2026)
**Pencapaian utama:**
- Seluruh visualisasi EDA selesai: distribusi kelas, Severity Score, class imbalance (rasio 1:2.07 Normal:Disleksia).
- Dua pertanyaan bisnis terjawab dengan bukti kuantitatif via **Mean Pixel Heatmap**:
  - Normal vs Disleksia berbeda visual: selisih piksel **15.88/255** ✅
  - Severity 6 vs Severity 1 berbeda: selisih piksel **16.57/255** ✅
- Keputusan final: augmentasi fisik (rotasi offline) **DIBATALKAN** → diserahkan ke AI Engineer on-the-fly.
- Stratified Split awal: Train 60.6% / Validation 15.2% / Test 24.2% (by severity_score).
- **Dua versi notebook tersedia:** `Dyslexia.ipynb` (versi final, no augmentasi) & `Dyslexia_OfflineAugmentation.ipynb` (backup).
- **Artefak:** `master_dataset_final.csv` (180.726 baris, 3-split), Class Weights (binary & severity).

### ✅ Checkpoint 4 — Finalisasi Arsitektur Translasi & OCR Paradox (21 April 2026)
**Pencapaian utama:**
- Perumusan dan dokumentasi **Paradoks OCR** secara formal.
- Pembedahan dua opsi arsitektur sistem translasi (Opsi A: Grid PDF & Opsi B: Tandem Pipeline OCR+NLP).
- Sweeping dokumentasi anti-augmentasi fisik di seluruh file repositori.
- Penetapan `class_weight` (Scikit-Learn) sebagai satu-satunya cara mengatasi class imbalance.
- **Artefak:** `Diskusi_Paradoks_OCR_dan_Translasi.md`, `Pilihan.md`.

### ✅ Checkpoint 5 — Unifikasi Dashboard & Optimasi Data Interaktif (26 April 2026)
**Pencapaian utama:**
- Pembuatan `app.py` (Streamlit) sebagai dashboard interaktif pertama.
- Sidebar toggle dinamis antara **Dataset Tanpa Augmentasi (Gambo)** vs **Dataset Dengan Augmentasi (Gambo+EMNIST)**.
- Semua visualisasi EDA bereaksi dinamis sesuai pilihan dataset.
- Optimasi memori: test set dikompresi menjadi `dyslexialens_test_rainy.csv.gz` (~10MB) untuk analisis piksel luring.
- Fix bug pathing gambar aset.
- **Artefak:** `app.py`, `dyslexialens_test_rainy.csv.gz`, `assets/*_rainy.png`.

### ✅ Checkpoint 6 — Standardisasi EMNIST, Memory Leak Fix & Pipeline Baru (4 Mei 2026)
**Pencapaian utama:**
- Rekonstruksi total pipeline integrasi EMNIST via `notebooks/Dyslexia_EMNIST.ipynb` (menggantikan script lama w0pal).
- Ekstraksi & filter EMNIST (buang numerik 0–9), injeksi sekuensial selaras skema Gambo.
- Implementasi **Algoritma Fair Pruning (Binary Search)**: memangkas EMNIST yang berlebih, berlabuh pada rasio **~1:1** (~142.000 Disleksia vs ~131.000 Normal).
- **Memory Leak Fix Gelombang 1:** Semua figure matplotlib dibungkus `try/finally plt.close(fig)`, migrasi ke OOP Plotting, cache `@st.cache_data` dipindahkan ke global scope.
- **Memory Leak Fix Gelombang 2 (Crash Tab Viewer):** Ganti `row.values[1:]` dengan `row.drop('label').values.astype(np.float64)`, turunkan sampel 500→300, eksplisit `del` array besar, tambahkan `try/except` error boundary.
- Standarisasi nomenklatur aset: `*_rainy.*` → `*_noAugmentation.*`, `*_emnist.*` → `*_EMNIST.*`.
- Generate `dyslexialens_test_EMNIST.csv.gz` (~23.1 MB, 94.671 sampel).
- **Artefak:** `Dyslexia_EMNIST.ipynb`, `dyslexialens_test_EMNIST.csv.gz`, `dyslexialens_test_noAugmentation.csv.gz`.

### ✅ Checkpoint 7 — Dataset Integrity Hardening (11 Mei 2026)
**Pencapaian utama:**
- Evolusi filosofi: dari "dataset cukup bersih" → **"dataset harus steril secara statistik dan visual"**.
- Eksperimen *auto inversion* untuk normalisasi polaritas gambar → **GAGAL** (gambar noisy, stroke rusak).
- Keputusan final: gambar berpolaritas anomali **DIHAPUS**, bukan diaugmentasi paksa.
- *Full dataset re-audit*: penghapusan duplicate lineage, visual duplication, file placeholder, regex nama rusak.
- Rekalibrasi fitur `ink_density` dengan foreground isolation + threshold-aware extraction (tidak lagi dipengaruhi background color).
- Standardisasi total: grayscale consistency, polarity consistency, foreground normalization, structural validation.
- **Dampak:** CNN dipaksa belajar pola stroke & severity, **BUKAN** warna background atau artefak dataset.

### ✅ Checkpoint 8 — Strategi Shape-Agnostic & Arsitektur Late Fusion (11 Mei 2026)
**Pencapaian utama:**
- Standarisasi penamaan file lintas OS: format `[Split]_[Class]_[Case]_[Char]_[Index].png` (contoh: `Train_Normal_Upper_A_00470.png`). Menghapus risiko file collision di Windows yang case-insensitive.
- Penetapan **Arsitektur Shape-Agnostic (Plan A):**
  - Preservasi "Golden Feature" medis: huruf b, d, p, q di kelas Reversal tetap dipertahankan.
  - Pembuangan ~3.000 gambar ber-artefak blok putih pojok.
  - **Late Fusion Architecture:** CNN (ekstrak pola spasial 28×28) + Model Tabular (5 Fitur XAI) → digabung (concatenation) → layer klasifikasi final.
  - **Dua jalur terpisah:** Translasi OCR (seluruh abjad EMNIST A–Z, a–z) vs Diagnosa Klinis (Gambo + EMNIST seimbang).
- Keputusan: dataset final tetap di **28×28 grayscale** (tidak di-upscale). Enhancement/upscaling canggih diserahkan ke pipeline AI Engineer jika diperlukan.
- **Artefak:** Dokumentasi `01_Strategi_Fitur_dan_Arsitektur.md`, `Hasil_Kerja_EMNIST_to_Gambo.md`.

### ✅ Checkpoint 9 — XAI Feature Engineering, Finalisasi Dashboard Eksekutif (17 Mei 2026)
**Pencapaian utama:**
- Perumusan dan ekstraksi **5 Fitur Geometri Matematis (XAI)** dari matriks piksel 28×28:
  1. `ink_density`: Rasio tinta hitam → deteksi penekanan pena berlebih (over-tracing).
  2. `center_of_mass_x` & `center_of_mass_y`: Pergeseran gravitasi tarikan garis → deteksi ketidakstabilan spasial.
  3. `bounding_box_ratio`: Rasio panjang-lebar kotak imajiner → deteksi proporsi huruf terdistorsi.
  4. `horizontal_symmetry`: **Golden Feature** utama → menangkap anomali pencerminan huruf (Reversal/efek cermin).
  5. `stroke_transitions`: Frekuensi perubahan warna (putih→hitam) → memetakan Tremor atau keraguan saat menulis.
- Pembangunan strategi *Pre-calculated Assets*: Heatmap, KDE Plot, Boxplot di-generate via Notebook dan disimpan sebagai `.png` (menghindari server crash saat real-time computation >273.000 sampel).
- Perombakan `app.py` menjadi **Executive Dashboard** 5 Tab: Dataset Summary, Computer Vision, XAI Profiling, Stratification, Interactive Viewer.
- Implementasi *Data Storytelling UI*: kotak pesan interaktif menyandingkan grafik dengan jawaban 4 Pertanyaan Bisnis.
- Sterilisasi 3 Notebook utama: `Dyslexia_EMNIST.ipynb`, `Dyslexia_NoAugmentation.ipynb`, `EMNIST_to_Gambo.ipynb`.
- Penulisan ulang total `README.md` (menegaskan rasio 1:1, batas kerja Rainy vs w0pal).
- **Pembagian kontribusi final (tercatat di README.md):**
  - Rainy: Dataset Auditing, Data Wrangling, Stratified Splitting, XAI Feature Engineering, Dashboarding.
  - w0pal: EMNIST-Gambo Integration (Balancing), Metadata Construction, Pipeline Automation.
- **Artefak:** `Dataset_Dyslexia_EMNIST_FeatureEngineering.csv`, `Dataset_Dyslexia_NoAugmentation_FeatureEngineering.csv`, `assets/EMNIST/`, `assets/noAugmentation/`.

### ✅ Checkpoint 10 — A/B Testing Validation & SLA Handover (31 Mei 2026)
**Pencapaian utama:**
- Eksekusi **Mann-Whitney U Test** untuk membandingkan distribusi 6 fitur XAI antara dataset Gambo asli vs Gambo+EMNIST. Ditemukan fenomena *Large N Effect* (p-value selalu <0.05 karena sampel >150.000 — tidak bisa diandalkan).
- Penyelamatan klinis via **Cohen's d (Effect Size)**: seluruh 6 fitur XAI menunjukkan status **Negligible** (|d| < 0.2).
- **Kesimpulan A/B Testing:** Augmentasi EMNIST terbukti secara saintifik **100% aman klinis**, tidak mengubah DNA asli pola tulisan disleksia.
- Penyusunan **Laporan Teknis Komprehensif Final (SLA Handover)** 8 Bab — 51 Halaman:
  - Bab 1: Audit & Logical Cleaning
  - Bab 2: Image Preprocessing & Standardization
  - Bab 3: EMNIST Integration & Fair Pruning
  - Bab 4: XAI Feature Engineering
  - Bab 5: A/B Testing Validation
  - Bab 6: Stratified Split
  - Bab 7: Constraints & SLA (Larangan Mutlak untuk AI Engineer)
  - Bab 8: Executive Handover
- Tambahan Tab 5 khusus di Dashboard: *A/B Testing Validation* dengan visualisasi KDE Overlay.
- Perumusan strategi presentasi *Elevator Pitch* untuk Advisor.
- **Artefak:** `Final.md`, `Laporan Teknis Komprehensif Final.pdf` (51 hal), `Pertanyaan_Advisor_Revisi.md`.

### ✅ Checkpoint 11 — Dashboard Polish, Clean Code & Final Delivery (31 Mei 2026)
**Pencapaian utama (UI/UX & Refactoring):**
- Rename `app.py` → `Dashboard.py` sebagai pusat kendali final.
- Ekstraksi CSS ke `Assets/Styles.css`, dimuat via `load_custom_css()`.
- Abstraksi fungsi `render_section_header(subtitle, title, description)` menggantikan 6+ blok HTML berulang.
- Dictionary `DATASET_OPTIONS` + fungsi `get_dataset_assets(choice)` menggantikan if/else berulang.
- Penerapan prinsip **DRY (Don't Repeat Yourself)** & **Separation of Concerns** secara menyeluruh.
- Desain ulang visual: centering semua komponen (Stat Cards, Business Question Cards, Kesimpulan Cards).
- Perbaikan grid 10 Sampel Acak: dari 1×10 → **2 baris × 5 kolom**, dibungkus `st.columns([1,4,1])` agar simetris.
- Perbaikan Ghost Image: `st.columns([1, 1.2, 1])` untuk centering.
- Perbaikan bullet list `<ul>/<li>` → `<div>` dengan simbol manual agar benar-benar terpusat.
- Ukuran figure matplotlib disesuaikan proporsional terhadap container Streamlit.
- Pembuatan `Konteks_Handover_AI_Agent.md` (dokumen ini) sebagai warisan pengetahuan proyek.

---

## 📁 Struktur Repositori Final

```
Dataset Disleksia/
├── Dashboard.py                    # Pusat kendali dashboard Streamlit (FINAL)
├── Assets/
│   ├── Styles.css                  # Semua CSS kustom (dark theme, cards, navbar)
│   ├── noAugmentation/             # Aset PNG visualisasi dataset Gambo murni
│   │   ├── class_distribution.png, severity_distribution.png, heatmap.png, dll.
│   ├── EMNIST/                     # Aset PNG visualisasi dataset Gambo+EMNIST
│   │   ├── class_distribution.png, severity_distribution.png, heatmap.png, dll.
│   └── Logo DyslexiaLens.png
├── Data/
│   ├── Dataset_Dyslexia_NoAugmentation_FeatureEngineering.csv  # Dataset CSV dengan 6 fitur XAI (Gambo murni)
│   ├── Dataset_Dyslexia_EMNIST_FeatureEngineering.csv          # Dataset CSV dengan 6 fitur XAI (Gambo+EMNIST)
│   ├── Testset_Dyslexia_EMNIST.csv.gz                    # Pixel matrix test set, compressed (~10MB)
│   └── Testset_Dyslexia_NoAugmentation.csv.gz                 # Pixel matrix test set EMNIST, compressed (~23MB)
└── Dokumentasi/
    └── Rainy/
        ├── Checkpoint/             # CP 1–11 (riwayat lengkap per sesi)
        ├── Final.md                # Laporan Teknis Master (SLA Handover, 8 Bab)
        ├── Data Scientist Checklist.md
        └── Konteks_Handover_AI_Agent.md  # Dokumen ini
```

---

## 🔒 SLA Constraints untuk AI Engineer (LARANGAN MUTLAK)

| # | Larangan | Alasan |
|---|---|---|
| 1 | **JANGAN** gunakan augmentasi rotasi/flip/spasial | Menghancurkan sinyal Reversal Error |
| 2 | **JANGAN** gunakan Accuracy sebagai metrik utama | Menyesatkan karena distribusi tetap tidak seimbang |
| 3 | **JANGAN** gunakan MSE Loss untuk Severity Score | Severity bersifat ordinal, gunakan Cross-Entropy atau Ordinal Loss |
| 4 | **JANGAN** klaim sebagai alat diagnosis medis | Hanya alat bantu early screening |
| 5 | **JANGAN** gunakan data EMNIST tanpa proses Fair Pruning | Menyebabkan Class Imbalance arah sebaliknya |
| 6 | **JANGAN** upscale gambar dengan interpolasi biasa | Merusak integritas stroke asli 28×28 |

---

## 📊 Statistik Dataset Final

| Dataset | Kelas Disleksia | Kelas Normal | Total | Rasio |
|---|---|---|---|---|
| Gambo (No Augmentation) | ~120.463 | ~35.990 | ~156.453 | ≈ 3.3:1 |
| Gambo + EMNIST (Augmented) | ~142.000 | ~131.000 | ~273.000 | ≈ 1.08:1 |

**Split Final (Dataset Augmented):**
- Train: 70% (~191.100 gambar)
- Test: 15% (~40.950 gambar)  
- Validation: 15% (~40.950 gambar)

---

## 🧠 Catatan Akhir untuk AI Agent Berikutnya

1. **File of Truth untuk Data:** `Data/Dataset_Dyslexia_EMNIST_FeatureEngineering.csv` adalah dataset siap latih dengan 6 fitur XAI. Gunakan ini sebagai input utama model tabular.
2. **File of Truth untuk Dashboard:** `Dashboard.py` adalah satu-satunya file yang perlu dimodifikasi untuk perubahan UI. Periksa `Assets/Styles.css` untuk perubahan visual.
3. **Konteks Teknis Lengkap:** Baca `Dokumentasi/Rainy/Final.md` untuk semua justifikasi keputusan teknis secara mendetail sebelum memulai pekerjaan modeling.
4. **Semua keputusan arsitektur sudah final** — tidak perlu mengulang eksperimen yang sudah dilakukan (polarity, augmentasi, scaling, dsb.).
