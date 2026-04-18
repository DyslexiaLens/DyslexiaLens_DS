# Checkpoint 3 — EDA, Explanatory Analysis, Stratified Split & Kesiapan Handover
**Tanggal:** 19 April 2026  
**Role:** Data Scientist  
**Status Notebook:** `Dyslexia.ipynb` (Tahap 1–6 Selesai)

---

## 🎯 Pencapaian Sesi Ini
Sesi ini menyelesaikan **seluruh pipeline Data Scientist** — dari EDA hingga kesiapan handover ke AI Engineer. Fokus utama:

### 1. Exploratory Data Analysis (Tahap 4)
Seluruh visualisasi EDA telah diimplementasikan dan didokumentasikan:
- **4B:** Distribusi kelas (Normal/Corrected/Reversal) per split Train/Test
- **4C:** Distribusi Severity Score 0–6 dalam bar chart
- **4D:** Analisis binary class imbalance (Normal vs Disleksia) — rasio 1:2.07
- **4E:** Sampel gambar representatif per kelas (5 gambar × 3 kelas)
- **4F:** Sampel per severity (skor 1 vs 3 vs 6) — menunjukkan progresivitas *scribbling*
- **4G:** Distribusi severity di Corrected vs Reversal — Reversal terkonsentrasi di skor 6

### 2. Explanatory Analysis (Tahap 4 lanjutan)
Menjawab **dua pertanyaan bisnis utama** menggunakan teknik **Mean Pixel Heatmap**:

| Pertanyaan Bisnis | Jawaban | Selisih Piksel |
|---|---|---|
| Apakah Normal vs Disleksia berbeda secara visual? | ✅ Ya | 15,88 / 255 |
| Apakah Severity Score 6 berbeda dari Score 1? | ✅ Ya | 16,57 / 255 |

- Kedua hipotesis awal **TERBUKTI didukung data**
- Angka selisih konservatif karena di-rata-ratakan termasuk background; perbedaan aktual pada zona goresan jauh lebih besar

### 3. Stratified Split & Keputusan Arsitektural
Kami membuat **keputusan arsitektural penting** terkait augmentasi:

- **Awalnya:** Implementasi augmentasi offline (rotasi ±10°, scaling 0.9–1.1×) pada skor 2–5
- **Masalah ditemukan:** Distribution shift antara Train dan Validation/Test + risiko data leakage
- **Keputusan final:** Menyediakan **data bersih tanpa augmentasi fisik**, augmentasi diserahkan ke AI Engineer secara on-the-fly

**Dua versi notebook tersedia:**

| File | Pendekatan |
|---|---|
| `Dyslexia.ipynb` | ✅ Versi utama — data bersih, stratified split, tanpa augmentasi |
| `Dyslexia_OfflineAugmentation.ipynb` | Alternatif — augmentasi offline skor 2–5 (backup) |

### 4. Kesiapan Data untuk Pemodelan (Tahap 5–6)
- **Stratified Split:** Train 60,6% / Validation 15,2% / Test 24,2% (stratified by severity_score)
- **Data Dictionary:** 6 kolom terdefinisi formal
- **Class Weights:** Dihitung untuk binary dan severity → siap dipakai `model.fit()`
- **Validasi Leakage:** 0 overlap antara Train ∩ Validation ∩ Test ✅
- **Rekomendasi Augmentasi:** Kode `ImageDataGenerator` disediakan di notebook

---

## 📊 Status Checklist Terkini
- **Persiapan Dataset:** [x] 100% Selesai
- **Pertanyaan Bisnis:** [x] 100% Selesai
- **Data Wrangling:** [x] 100% Selesai
- **EDA & Visualisasi:** [x] 100% Selesai
- **Explanatory Analysis:** [x] 100% Selesai
- **Kesiapan Data:** [x] 100% Selesai
- **Dashboard Streamlit:** [ ] Belum dimulai

---

## 📂 Artefak Dokumentasi
### Baru dibuat:
1. [Temuan_EDA.md](file:///d:/Tugas/Kuliah/Semester%206/Dicoding/Capstone%20Project/Dataset%20Disleksia/Dokumentasi/Rainy/Temuan_EDA.md) — Dokumentasi lengkap temuan EDA (1–6), hasil augmentasi, dan class weights
2. [Explanatory_Analysis.md](file:///d:/Tugas/Kuliah/Semester%206/Dicoding/Capstone%20Project/Dataset%20Disleksia/Dokumentasi/Rainy/Explanatory_Analysis.md) — Jawaban pertanyaan bisnis dengan bukti kuantitatif

### Diperbarui:
3. [Data Scientist Checklist.md](file:///d:/Tugas/Kuliah/Semester%206/Dicoding/Capstone%20Project/Dataset%20Disleksia/Dokumentasi/Rainy/Data%20Scientist%20Checklist.md) — Semua item EDA dan Kesiapan Data di-update ke [x]

### Output untuk AI Engineer:
4. `master_dataset_final.csv` — Dataset bersih dengan 3 split (Train/Validation/Test), 180.726 baris
5. Class weights (binary + severity) tersedia di sel 5B notebook

---

## 🚀 Rencana Sesi Berikutnya
- Membangun **Dashboard Streamlit** untuk menampilkan insight EDA secara interaktif
- Finalisasi dokumentasi akhir dan handover resmi ke AI Engineer
- Memulai fase modeling (di sisi AI Engineer)
