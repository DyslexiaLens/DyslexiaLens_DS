# Dokumentasi Diskusi Strategi Dataset & Arsitektur Fitur DyslexiaLens

## 1. Penanganan Anomali pada Dataset Gambo (Disleksia)
### a. Kasus Huruf Kecil (b, d, p, q) pada Kelas Reversal
*   **Temuan:** Terdapat anomali di mana dataset Gambo mayoritas berisi huruf kapital, namun pada kelas *Reversal* terdapat sekitar 20% huruf kecil spesifik seperti `b`, `d`, `p`, dan `q`.
*   **Keputusan:** **Dipertahankan (Jangan Dihapus).**
*   **Alasan Medis:** Secara klinis, disleksia sangat identik dengan *reversal error* (tertukarnya arah) pada huruf-huruf simetris tersebut. Menghapus data ini berarti membuang indikator emas (*golden feature*) pendeteksi disleksia.

### b. Kasus Gambar Augmentasi Ber-Artefak (White Borders)
*   **Temuan:** Terdapat sekitar 3.000 gambar hasil augmentasi (beda warna latar) yang menyisakan blok/artefak putih di bagian tepi pojok gambar.
*   **Keputusan:** **Dihapus/Drop (Tidak Dipakai).**
*   **Alasan Teknis:**
    *   **Kehancuran Fitur Matematis:** Artefak di pojokan akan merusak perhitungan `bounding_box_ratio` (kotak ditarik maksimal) dan `center_of_mass` (bergeser ke tepi).
    *   **Data Leakage (Shortcut Learning):** CNN akan mengabaikan bentuk huruf dan hanya belajar mengklasifikasikan kelas berdasarkan keberadaan "titik putih di pojokan". Karena jumlahnya kecil (< 2% dari total 156.000 data), membuangnya adalah langkah paling efisien untuk menjaga kemurnian dataset.

---

## 2. Strategi Ekstraksi Dataset EMNIST (Normal)
### a. Pemilihan Kelas Abjad (A-Z dan a-z)
*   **Keputusan:** Mengekstrak **SEMUA** variasi abjad (Kelas 10-61 pada EMNIST ByClass), yang mencakup A-Z (Kapital) dan a-z (Kecil).
*   **Alasan UX (User Experience):** Aplikasi akan mengizinkan pengguna menulis kalimat bebas di kertas grid kosong. Jika AI hanya dilatih dengan huruf spesifik (seperti b,d,p,q), fitur translasi (OCR) akan gagal mengenali huruf lain (seperti a, e, g, dll).

### b. Penanganan Ketidakseimbangan Kelas (Class Imbalance)
*   **Tindakan Wajib:** Melakukan **Stratified Sampling** pada dataset EMNIST.
*   **Alasan:** EMNIST memiliki ratusan ribu data. Jika digabungkan mentah-mentah, kelas "Normal" akan mendominasi dan menyebabkan model selalu memprediksi "Normal". Jumlah total gambar yang diambil dari EMNIST harus seimbang (rasio 1:1) dengan total dataset disleksia dari Gambo, dibagi rata untuk ke-52 abjad.

---

## 3. Arsitektur Pemisahan Fitur (The "Shape-Agnostic" Approach)
Untuk mencegah model bias terhadap bentuk huruf tertentu (misal: "Jika huruf 'a', pasti Normal karena di dataset Disleksia tidak ada huruf 'a'"), diputuskan arsitektur pemisahan sistem sebagai berikut:

### Plan A (Arsitektur Utama - Dijalankan)
Sistem memisahkan alur kerja antara Translasi OCR dan Diagnosa Disleksia secara elegan:
1.  **Fitur Translasi (OCR):**
    *   Menggunakan model Visi (CNN atau eksternal API) yang dilatih menggunakan seluruh abjad EMNIST (A-Z, a-z) murni untuk mengenali bentuk karakter dan menerjemahkannya menjadi teks tertulis.
2.  **Fitur Diagnosa Disleksia:**
    *   **Tidak bergantung pada bentuk huruf** untuk klasifikasi penyakit.
    *   Menggunakan model Tabular/Machine Learning (seperti Random Forest, XGBoost, atau Dense NN) yang dilatih secara khusus menggunakan **5 Fitur Turunan Matematis (Feature Engineering)** yang diekstrak dari piksel gambar:
        *   `ink_density`: Mendeteksi penebalan tulisan akibat *over-tracing*.
        *   `center_of_mass_x` & `center_of_mass_y`: Mendeteksi distorsi orientasi/kemiringan dan posisi penulisan yang melayang/anjlok.
        *   `bounding_box_ratio`: Mengidentifikasi distorsi proporsi huruf (terlalu pipih/melebar).
        *   `stroke_transitions`: Mengukur frekuensi perubahan warna piksel untuk mendeteksi getaran tangan (*tremor*).
    *   **Keunggulan:** Diagnosa menjadi kebal terhadap bias abjad (*Shape-Agnostic*). Model menilai murni dari kualitas motorik (tarikan garis), bukan mempermasalahkan anak tersebut menulis huruf apa.

### Plan B (Rencana Cadangan)
*   Jika Plan A menghadapi kebuntuan waktu/teknis, sistem akan dibuat lebih restriktif: Aplikasi melakukan *generate* dokumen PDF berisi template teks spesifik (misal: tulisan "APA KABAR") untuk disalin ulang oleh pengguna ke dalam grid. 
*   **Status:** Ditahan sebagai langkah darurat (Fallback). Plan A dinilai jauh lebih *user-friendly*, dinamis, dan memiliki kompleksitas *engineering* yang tinggi untuk proyek Capstone.
