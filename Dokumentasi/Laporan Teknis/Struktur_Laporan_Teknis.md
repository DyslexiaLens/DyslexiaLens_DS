# 📑 Struktur Laporan Teknis Data Science — DyslexiaLens

> **Catatan:** Laporan ini difokuskan pada **Pipeline Data Science**, mendokumentasikan rekam jejak teknis, *evidence* empiris, serta panduan *handover* untuk tim AI Engineer. 

---

## 1. Pendahuluan & Konteks Bisnis
*Mendefinisikan latar belakang masalah agar seluruh langkah teknis memiliki tujuan yang jelas.*
- **1.1 Latar Belakang Masalah:** Urgensi deteksi dini disleksia dan potensi tulisan tangan sebagai *biomarker* kuantitatif.
- **1.2 Tujuan Proyek:** Membangun *pipeline dataset* yang bersih, seimbang, dan bebas bias untuk pelatihan *Machine Learning*.
- **1.3 Pertanyaan Bisnis:**
  - Evaluasi Keseimbangan Dataset (Imbalance).
  - Pembuktian Pola Disleksia (Tremor/Asimetri).
  - Rancangan Explainable AI (XAI).
  - Interpretasi Sub-tipe/Severity Score.
## 2. Audit & Profiling Dataset Awal
*Mendokumentasikan kondisi data mentah (Gambo) sebelum diproses.*
- **2.1 Sumber & Karakteristik Data:** Profil dataset Gambo (jumlah, resolusi, format visual).
- **2.2 Temuan Anomali (*Data Assessing*):** 
  - Penemuan *Label Noise* (file terklasifikasi di folder yang salah).
  - Skala *Severity Score* bawaan yang terbalik (9 = Ringan, 1 = Parah).

## 3. Pembersihan & Rekayasa Data (*Data Cleaning*)
*Menjelaskan solusi teknis atas anomali yang ditemukan.*
- **3.1 Logical Cleaning:** Teknik pembuangan *label noise* secara aman via Pandas DataFrame.
- **3.2 Rekonstruksi *Severity Score*:** Pemetaan ulang skala keparahan menjadi standar yang logis (0 = Sehat, 1-6 = Rentang Disleksia).

## 4. Feature Engineering (Explainable AI / XAI)
*Menjelaskan proses ekstraksi pola citra menjadi metrik kuantitatif.*
- **4.1 Preprocessing Citra Dasar:** Binarisasi dan standardisasi *whitespace* (*padding*).
- **4.2 Ekstraksi 6 Fitur Matematis:** Penjelasan logis mengapa fitur seperti `ink_density`, `bounding_box_ratio`, dan `stroke_transitions` mampu merepresentasikan gejala motorik disleksia (berdasarkan literatur/asumsi medis).

## 5. Exploratory Data Analysis (EDA) & Dashboarding
*Memaparkan temuan visual dan deployment hasil analisis.*
- **5.1 Analisis Imbalance & Korelasi:** Bukti visual kesenjangan jumlah data dan hubungan antar skor keparahan.
- **5.2 *Explanatory Analysis*:** Perbandingan visual distribusi fitur XAI antara Normal vs Disleksia.
- **5.3 Deployment Dashboard:** Penyajian interaktif temuan EDA melalui *Streamlit Cloud* untuk kemudahan pemantauan *stakeholder*.

## 6. Strategi Augmentasi & A/B Testing
*Mendokumentasikan keputusan strategis penyeimbangan dataset.*
- **6.1 Solusi *Dual-Track* & EMNIST:** Mengapa EMNIST dipilih dan mengapa augmentasi spasial (rotasi/flip) dilarang keras.
- **6.2 A/B Testing Integritas Data:** Eksekusi *Mann-Whitney U Test* untuk membuktikan secara statistik bahwa injeksi EMNIST tidak merusak karakteristik asli pola tulisan.

## 7. Penyiapan Data Final (*Data Preparation*)
*Tahap pemaketan data sebelum diserahkan ke AI Engineer.*
- **7.1 Stratified Splitting:** Mekanisme pembagian 80% Train, 10% Validation, 10% Test untuk mencegah kebocoran data.
- **7.2 Data Dictionary Final:** Spesifikasi struktur akhir dari `master_dataset_final_balanced_rill_featured.csv`.

## 8. Kesimpulan & *Action Items* (Handover)
*Menjawab pertanyaan bisnis dan memberikan mandat teknis ke tahap selanjutnya.*
- **8.1 Jawaban Pertanyaan Bisnis:** Rangkuman temuan utama dari EDA dan A/B Testing.
- **8.2 *Action Items* (Panduan AI Engineer):** Mandat penggunaan nilai parameter `class_weight` saat proses *training* dan larangan *spatial augmentation*.
