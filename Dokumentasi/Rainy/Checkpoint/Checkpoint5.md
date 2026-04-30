# Checkpoint 5: Unifikasi Dashboard & Optimalisasi Data Interaktif (DyslexiaLens)

**Tanggal:** 26 April 2026
**Fokus:** Penyatuan hasil riset (Dataset Original Gambo) ke dalam satu dashboard interaktif Streamlit bersama dengan data kolega (Augmented EMNIST), serta optimalisasi visualisasi dinamis.

## 🎯 Objektif Selesai
1. **Unifikasi Dashboard (Single Source of Truth):** 
   - Menyempurnakan `app.py` agar dapat digunakan secara bersamaan oleh tim. 
   - Membuat *sidebar dinamis* yang memungkinkan pengguna melakukan *toggle* antara **Dataset Tanpa Augmentasi (Original Gambo)** (fokus riset Rainy) dan **Dataset Dengan Augmentasi (Gambo + EMNIST)** (fokus kolega).
   
2. **Rendering Visualisasi Dinamis:**
   - Semua *Business Questions* dan visualisasi Exploratory Data Analysis (EDA) sekarang bereaksi terhadap dataset yang dipilih. 
   - Script diatur untuk secara dinamis meload gambar statis yang tepat (contoh: `heatmap_rainy.png` vs `heatmap_eda.png`, `class_samples_rainy.png` vs `class_samples.png`).
   - Melakukan *handling* terhadap *deprecation warnings* dari Streamlit (mengubah `use_container_width=True` menjadi `width='stretch'`) agar UI tetap dirender dengan mulus tanpa *error*.

3. **Optimalisasi Memori (Compressed Pixel CSV):**
   - Mengonversi data *Test* dari dataset Rainy (43,716 gambar 28x28 piksel grayscale) menjadi sebuah file pipih (flattened) menggunakan algoritma khusus.
   - Menyimpan hasilnya sebagai `dyslexialens_test_rainy.csv.gz` (~10MB) agar dashboard dapat menampilkan fitur "Eksplorasi Data" (Analisis Piksel Interaktif & Ghost Image) secara luring (*offline*) tanpa perlu memuat puluhan ribu file gambar fisik.

4. **Perbaikan Pathing & Regenerasi Heatmap Matematis:**
   - Menyelesaikan *bug* di mana gambar gagal diload karena ketidaksesuaian struktur direktori (`Dataset/...` vs `notebooks/Dataset/...`).
   - Berhasil menghitung rata-rata selisih piksel (0-255) antara pasien disleksia **Skor 1 (Gejala Ringan)** dan **Skor 6 (Gejala Parah)** untuk membuktikan adanya perbedaan ketebalan goresan (*reversal/corrected*) secara kuantitatif.

## 📦 Hasil Akhir & Berkas Kunci
- `app.py`: Aplikasi Streamlit utama yang sudah komprehensif.
- `assets/*_rainy.png`: Berkas-berkas grafik statis khusus untuk data tanpa augmentasi.
- `dyslexialens_test_rainy.csv.gz`: Berkas data gzip untuk evaluasi interaktif yang super ringan.

## 🚀 Langkah Selanjutnya (Next Steps)
Dashboard penyerahan (Handover Dashboard) untuk tim *Data Scientist* kini sudah dinyatakan **stabil dan final**. 
Fokus selanjutnya adalah masuk ke tahapan pemodelan (Modeling), di mana kita akan mulai mendesain arsitektur *Convolutional Neural Network* (CNN) menggunakan dataset master yang telah terstandarisasi.
