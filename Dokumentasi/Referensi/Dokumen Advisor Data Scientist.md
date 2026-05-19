# Dokumen Advisor — Data Scientist
## DyslexiaLens: Intelligent Handwriting Detection and Assistance for Dyslexia

---

## Documents

| No | Dokumen | Link |
|---|---|---|
| 1 | Project Plan | https://docs.google.com/document/d/1BkX0I5QH9HFt60nAbPNSEl4ZMN_j5Vl9YCDMRqIT2ew/edit?tab=t.0 |
| 2 | Repository Github (DS) | https://github.com/DyslexiaLens |
| 3 | Dataset Kaggle (Gambo) | https://www.kaggle.com/datasets/drizasazanitaisa/dyslexia-handwriting-dataset |
| 4 | Dataset Kaggle (EMNIST) | https://www.kaggle.com/datasets/crawford/emnist |
| 5 | Project Brief | https://docs.google.com/document/d/17R37WHy5uttdOUbrMQNrJhDG2QS-y1oCujnGWw3oZQI/edit?tab=t.0 |
| 6 | Executive Dashboard (Streamlit Cloud) | Sudah deploy — dapat diakses publik secara online |

---

## Short Introduction & Meeting Expectation

1. Tim *Data Science* DyslexiaLens sedang mengelola dua varian *pipeline* dataset (*Dual-Track Strategy*):
   - **Track A (NoAugmentation):** Dataset asli yang sudah dibersihkan (~180k gambar).
   - **Track B (EMNIST):** Dataset yang diseimbangkan menggunakan algoritma *Fair Pruning* (~273k gambar).
2. *Pipeline* data telah dilengkapi sistem ekstraksi **6 Fitur Matematis (XAI)** untuk mengukur karakteristik visual dari tulisan penderita disleksia dan mendukung transparansi model AI. Fitur tersebut mencakup:
   - *Ink Density* (mengukur penebalan tinta akibat coretan berulang).
   - *Center of Mass X & Y* (mengukur pergeseran/kemiringan posisi tulisan).
   - *Bounding Box Ratio* (mengukur distorsi proporsi bentuk huruf).
   - *Stroke Transitions* (mengukur tingkat getaran/putusnya goresan).
   - *Horizontal Symmetry* (mengukur asimetri pada tulisan).
3. Tim juga telah mendeploy **Executive Dashboard** interaktif ke Streamlit Cloud untuk menyajikan seluruh alur analisis data secara publik.
4. **Ekspektasi sesi ini:** Mendapatkan arahan khusus di domain *Data Science*, terutama terkait validasi *A/B Testing* dataset dan penyusunan *Technical Report*.

---

## Progres Saat Ini (Status Data Science)

| Item | Status |
|---|---|
| Audit & Data Wrangling Dataset Gambo | ✅ Selesai |
| EDA & Visualisasi Explanatory (Heatmaps, KDE, Boxplot) | ✅ Selesai |
| Stratified Split (Train/Validation/Test, tanpa Data Leakage) | ✅ Selesai |
| Integrasi EMNIST + Fair Pruning Balancing | ✅ Selesai |
| Feature Engineering (6 Fitur XAI) | ✅ Selesai |
| Executive Dashboard Streamlit | ✅ Selesai |
| Deployment Dashboard ke Streamlit Cloud | ✅ Selesai |
| Handover Dataset ke AI Engineer (CSV + ZIP) | ✅ Selesai |
| A/B Testing (NoAugment vs EMNIST) | 🔄 Belum dimulai (mandiri — membandingkan distribusi 6 fitur XAI antar dataset) |
| Technical Report Komprehensif | 🔄 Belum dimulai |

---

## Team Challenges & Questions to Advisor

### A. Terkait Laporan Teknikal & Dashboard

1. Apakah *Technical Report* wajib menyertakan *snippet* kode teknis, atau cukup fokus pada narasi analisis dan visualisasinya saja?
2. Adakah komponen interaktif spesifik di *Dashboard* yang dampaknya sangat besar pada nilai namun sering dilupakan peserta?

### B. Terkait Pendekatan & Metodologi Data Science

3. Apakah pemakaian dataset eksternal (EMNIST) untuk mengatasi *class imbalance* dinilai lebih baik daripada augmentasi sintetis?
4. Apakah ekstraksi 6 fitur matematis ini sudah memadai untuk memenuhi standar *Explainable AI (XAI)*?
5. Bagaimana metode terbaik membuktikan bahwa 6 fitur XAI ini benar-benar meningkatkan performa model akhir?
6. Apakah *upscale* ekstrem gambar dari 28x28 menjadi 224x224 (demi *pre-trained model*) termasuk *overkill* atau lumrah?

### C. Terkait A/B Testing (Prioritas Utama)

7. Apakah uji beda distribusi fitur (Mann-Whitney) sah sebagai *A/B Testing*, atau Dicoding mutlak menuntut uji akurasi model (McNemar)?
8. Jika hasil uji A/B ini signifikan, bagaimana cara terbaik menarasikan *business value*-nya di laporan?
9. Jika hasilnya tidak signifikan, apakah eksperimen ini "gagal", atau justru membuktikan augmentasi EMNIST aman?
10. Apakah format pelaporan *A/B Testing* dibebaskan, atau cukup lewat narasi visualisasi dan *P-value* di *notebook*?

### D. Terkait Submission & Penilaian

11. Area kelemahan *Data Science* apa yang dirasa paling kritis di proyek ini untuk segera diperbaiki?
12. Apa saja kesalahan fatal (*common mistakes*) di tahap *Data Science* yang paling sering menyebabkan pengurangan nilai?
