# 📁 Laporan Handover: Data Scientist ke AI Engineer

## 🎯 Objektif Selesai
Seluruh rangkaian pipeline penyiapan data (Data Wrangling, Cleaning, Balancing, dan EDA) telah selesai. Dataset `Gambo` (Dyslexia) telah berhasil dibersihkan dan digabungkan secara simetris dengan dataset eksternal `EMNIST` (Normal).

Semua tahap krusial sudah divalidasi:
1. **Pemurnian Label**: Menghapus `Label Noise` (file Normal yang tersesat di kelas Dyslexia).
2. **Balancing**: Menerapkan Oversampling pada kelas Dyslexia dan menambahkan EMNIST untuk menyeimbangkan kelas Normal.
3. **Stratified Splitting**: Membagi dataset menjadi porsi 80% Train dan 20% Test dengan proporsi kelas yang identik (~1:1) tanpa memicu *Domain Shift*.
4. **Pembuatan Master CSV**: Menyimpan daftar indeks (`master_dataset_dyslexia.csv`) sebagai _Single Source of Truth_.

---

## 🚀 Fitur Tambahan (Diserahkan ke Repositori)
Sebagai penutup tugas Data Scientist, telah disertakan dua script tambahan untuk mempermudah transisi kerja ke tim AI Engineer:

### 1. `app.py` (Streamlit Data Viewer)
Aplikasi Streamlit ini dirancang untuk mempermudah AI Engineer maupun *Stakeholders* dalam mengeksplorasi dataset tanpa harus menggali folder fisik.
*   **Menampilkan Metrik:** Total gambar, rasio Train vs Test.
*   **Visualisasi Kelas:** Menampilkan distribusi grafik antar kelas.
*   **Image Explorer:** Fitur *drop-down* untuk menampilkan sampel gambar acak berdasarkan split dan kelas.

**Cara Menjalankan:**
```bash
streamlit run app.py
```

### 2. `baseline_model.py` (Simple SGD Classifier)
Script ini berfungsi murni sebagai **Unit Test** bagi dataset (bukan model untuk produksi).
*   **Tujuan:** Membuktikan bahwa goresan tangan dari dataset kita memiliki fitur dasar yang bisa dipelajari (*learnable*) oleh algoritma klasifikasi.
*   **Algoritma:** Stochastic Gradient Descent (SGD) Linear Classifier dari Scikit-Learn.
*   **Hasil Evaluasi:** Mengalahkan akurasi tebakan acak (Random Guess > 50%), yang memvalidasi bahwa dataset sudah layak diteruskan ke tahap Arsitektur *Deep Learning*.

**Cara Menjalankan:**
```bash
python baseline_model.py
```

---

## 🤝 Batas Kerja (AI Engineer Area)
Folder fisik `Dataset_Ready/` sudah terstruktur dengan standar Keras (`tf.keras.preprocessing.image_dataset_from_directory`). Mulai dari titik ini, pengembangan **100% beralih ke tanggung jawab AI Engineer**.

Tugas AI Engineer berikutnya:
1. Membuat arsitektur Convolutional Neural Network (CNN) atau Deep Learning lainnya.
2. Melakukan augmentasi data lanjutan secara dinamis (`Albumentations`).
3. Mengatur *Learning Rate, Batch Size, Optimizer*.
4. Melatih, mengevaluasi, dan menyimpan model produksi.

*Good luck, AI Engineering Team! Dataset is yours.*
