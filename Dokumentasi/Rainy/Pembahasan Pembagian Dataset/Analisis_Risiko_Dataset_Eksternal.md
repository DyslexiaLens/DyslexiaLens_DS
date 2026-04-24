# Laporan Analisis Risiko Injeksi Dataset Eksternal (EMNIST & AZ123)
**Peran:** Data Scientist  
**Konteks:** Strategi *Balancing* Kelas pada Dataset DyslexiaLens (Normal vs Disleksia)

---

## 🎯 1. Ringkasan Eksekutif (Executive Summary)
Untuk mengatasi ketimpangan rasio kelas **1 : 2.8** (39.334 Normal vs 112.315 Disleksia) pada dataset utama (Gambo), telah dilakukan eksperimen ekstensif untuk menyuntikkan data *Normal* tambahan dari sumber eksternal, yakni:
1. **Dataset EMNIST** (Folder *Images*)
2. **Dataset Kaggle A-Z Handwritten Data** (*CSV / AZ123*)

**Keputusan Akhir:** 
Tim Data Science memutuskan untuk **MENOLAK 100%** penggunaan dataset eksternal tersebut dan memilih pendekatan algoritmik (**`class_weight`**) pada saat *training* model. Dokumen ini menjabarkan bukti empiris (statistik dan visual) yang melatarbelakangi keputusan krusial ini guna mencegah kegagalan model di dunia nyata (*Shortcut Learning*).

---

## 🔬 2. Temuan Eksperimen & Bukti Empiris

Kami telah membangun *pipeline Domain Adaptation* untuk memaksa data eksternal menyamar menjadi data Gambo melalui proses Binarisasi (*Thresholding*) dan *Resizing* (Padding 20x20 di atas kanvas 28x28). Namun, analisis metrik menunjukkan anomali yang membahayakan *Data Integrity*.

### A. Bukti 1: Distribusi Intensitas Piksel (Histogram)
Sebelum *preprocessing*, dataset eksternal (EMNIST & AZ123) memiliki distribusi piksel *grayscale* (abu-abu / *anti-aliasing*), ditandai dengan landainya kurva pada nilai piksel 50-200. Sebaliknya, dataset Gambo asli murni bersifat **Biner** (hitam pekat di 0, putih pekat di 255). 
* **Bahaya:** Jika dicampur mentah-mentah, CNN akan belajar *"Jika ada piksel abu-abu = Kelas Normal"*.

### B. Bukti 2: Jarak Domain (Mean Absolute Difference / MAD)
Kami mengukur *Mean Absolute Pixel Difference* (jarak rata-rata intensitas piksel) antara gambar Rata-rata (*Mean Image Heatmap*) dari berbagai kelas.

**Sebelum Preprocessing:**
* Gambo Normal vs EMNIST Mentah = `~10.54 / 255`
* Gambo Normal vs AZ123 Mentah = `14.95 / 255`
* Gambo Normal vs Gambo Disleksia = `18.70 / 255`

**Setelah Preprocessing (Binarisasi & Shrinking):**
* Gambo Normal vs EMNIST Processed = `15.08 / 255`
* Gambo Normal vs AZ123 Processed = `15.35 / 255`

**Analisis:**
Fakta bahwa skor EMNIST dan AZ123 sangat identik di kisaran `15.xx` membuktikan bahwa AZ123 (Kaggle) secara fundamental adalah **dataset turunan (subset) yang sama dengan EMNIST**. Keduanya membawa "DNA" gaya tulisan orang dewasa dari demografi Amerika (NIST) yang lengkungan dan tarikan garisnya sangat berbeda dengan coretan demografi asli dataset Gambo (anak-anak/remaja).

---

## ⚠️ 3. Ancaman Fatal: Shortcut Learning

Meskipun secara visual (setelah *preprocessing*) data EMNIST/AZ123 sudah terlihat hitam-putih seperti Gambo, *Convolutional Neural Networks* (CNN) bertindak sebagai pengekstrak fitur super-sensitif.

Jika kelas *Normal* kita campur dengan 72.000 gambar eksternal ini, CNN akan melakukan **Shortcut Learning**:
1. CNN mendeteksi *micro-features* (gaya lengkungan pena khas EMNIST).
2. CNN mengaitkan *micro-features* tersebut dengan label "Normal".
3. CNN berhenti mempedulikan ciri-ciri klinis Disleksia (seperti *reversal* atau tremor).
4. **Hasil Ilusi:** Akurasi validasi akan tembus 99% di atas kertas, tetapi ketika diuji di dunia nyata menggunakan tulisan normal dari pengguna, aplikasi akan **Gagal Total** karena tulisan pengguna tidak memiliki gaya "EMNIST".

---

## 🛡️ 4. Solusi & Rekomendasi Arsitektural

Mengingat aplikasi DyslexiaLens bersifat sebagai **Alat Skrining Medis/Psikologi**, menjaga **Kemurnian Distribusi Data (Data Integrity)** adalah syarat mutlak (*Zero Compromise*).

Oleh karena itu, penanganan *imbalance* akan diserahkan kepada ranah **Algorithmic-Level Balancing**:
1. **Rasio 1:2.8 Tergolong Ringan (*Mild Imbalance*):** Angka absolut 39.334 gambar untuk kelas Normal sudah sangat masif dan lebih dari cukup bagi CNN untuk mempelajari *manifold* kelas Normal secara komprehensif.
2. **Implementasi `class_weight`:** Pada tahap pemodelan (`model.fit`), AI Engineer akan diinstruksikan untuk memasukkan parameter `class_weight`. Ini akan secara otomatis mengalikan bobot *Penalty Loss* sekitar 2.8x lipat setiap kali model salah mengklasifikasikan gambar Normal, memaksa model untuk lebih "berhati-hati" tanpa harus mencemari kumpulan data murni.

*(Dokumen ini mengacu pada eksperimen yang terekam pada `Domain_Adaptation_EMNIST.ipynb` dan `Perbandingan_AZ123.ipynb` di folder Dataset).*
