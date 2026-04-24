# 📁 Dokumentasi: Stratified Splitting Dataset

## 🎯 Objektif
Sesuai arahan, tujuan utama tahap ini adalah mengimplementasikan **Stratified Split**. Kita ingin memastikan proporsi kelas (Normal vs Dyslexia) maupun sumber data (Gambo vs EMNIST) merata dengan rasio yang identik antara data latih (Train) dan data uji (Test).

## 🛠 Mengapa Stratifikasi Itu Penting?
Sebelumnya, dataset terbagi berdasarkan folder `Train` dan `Test` fisik dari dataset asli. Setelah penambahan `EMNIST`, semua gambar augmentasi masuk ke dalam foldernya masing-masing, namun hal ini menyebabkan **ketidakseimbangan distribusi**:
- Data `Train` memiliki campuran **Gambo + EMNIST**.
- Data `Test` **hanya** memiliki **Gambo**.

Jika AI Engineer melatih model dengan struktur folder ini, model akan mengalami **Domain Shift** saat dievaluasi, karena ia tidak pernah melihat pola EMNIST di tahap testing.

## 🚀 Implementasi Kode (`stratified_split.py`)
Script `stratified_split.py` telah dibuat dan dijalankan dengan alur berikut:
1. **Scanning Total**: Mengumpulkan seluruh file `.png` dari folder `Gambo/` dan `EMNIST_Processed/`.
2. **Double Stratification**: Memisahkan dataset menjadi 80% Train dan 20% Test dengan parameter `stratify` menggunakan kombinasi `Target Class` (0/1) dan `Source` (Gambo/EMNIST).
3. **Penyalinan Fisik**: Menyalin file-file secara fisik ke dalam folder baru yang bersih bernama `Dataset_Ready/`.

## 📊 Hasil Distribusi Baru (Dataset_Ready)
Dataset kini memiliki rasio **51.9% Disleksia** dan **48.1% Normal**, yang nyaris mendekati rasio emas 1:1.

Proporsi Train (80%):
- Kelas 1 (Dyslexia): 51.9%
- Kelas 0 (Normal): 48.1%

Proporsi Test (20%):
- Kelas 1 (Dyslexia): 51.9%
- Kelas 0 (Normal): 48.1%

Folder `Dataset_Ready` memiliki struktur standar Keras/PyTorch:
```text
Dataset_Ready/
├── Train/
│   ├── Normal/     (Berisi Gambo + EMNIST_Processed)
│   └── Dyslexia/   (Berisi Gambo)
└── Test/
    ├── Normal/     (Berisi Gambo + EMNIST_Processed)
    └── Dyslexia/   (Berisi Gambo)
```

## 🧠 Rekomendasi Objektif Selanjutnya (Data Scientist vs AI Engineer)
Sebagai seorang Data Scientist, tugas krusial Anda (Data Wrangling, Cleaning, Balancing, EDA, Stratified Splitting) **sudah selesai** dengan terciptanya folder `Dataset_Ready/`!

Agar tidak bentrok (overlap) dengan tanggung jawab **AI Engineer**, ini adalah panduan objektif selanjutnya:

### ✅ Batas Tanggung Jawab Data Scientist
* **Data Quality Check (Terakhir):** Pastikan `Dataset_Ready` bersih dari corrupt images dan duplikasi.
* **Baseline Modeling (Tugas Tambahan yang Dianjurkan):** Buat model yang sangat sederhana (seperti `DummyClassifier` atau arsitektur CNN paling simpel) hanya untuk memvalidasi bahwa dataset "bisa dipelajari" dan pipeline tidak rusak. Jangan berfokus mengejar akurasi tinggi!
* **Feature Engineering Konseptual:** Serahkan rekomendasi preprocessing visual (seperti CLAHE, Edge Detection, atau Binarization) sebagai laporan ke AI Engineer, tapi jangan wajib diterapkan secara statis jika AI Engineer ingin memprosesnya di dalam pipeline mereka (`tf.data` atau `Albumentations`).

### ❌ Jangan Dilakukan (Area AI Engineer)
* Mendesain arsitektur *Deep Learning* kompleks seperti ResNet, EfficientNet, atau ViT.
* Melakukan *Hyperparameter Tuning* intensif (Epoch, Batch Size, Optimizer, Learning Rate).
* Merancang strategi Deployment atau konversi model (TFLite, ONNX).

**Saran Langkah Berikutnya:** Buat dokumentasi kesimpulan data (*Dataset Handover Report*) dan serahkan folder `Dataset_Ready` ke AI Engineer. Anda bisa merancang *Baseline Model* sederhana selagi mereka bekerja!
