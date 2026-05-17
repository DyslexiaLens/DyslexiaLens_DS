# Keputusan Strategis: Dataset, Fitur Gambar, dan Arsitektur Deteksi

Dokumen ini memuat rangkuman diskusi komprehensif terkait penanganan anomali dataset Gambo, ekstraksi dataset EMNIST, dan penentuan arsitektur akhir dari aplikasi DyslexiaLens.

## 1. Analisis dan Penanganan Anomali Dataset Disleksia (Gambo)

### A. Anomali Huruf Kecil pada Kelas Reversal
**Konteks Masalah:**
Secara umum, dataset Gambo didominasi oleh tulisan tangan huruf kapital. Namun, ditemukan bahwa sekitar 20% data pada sub-kelas *Reversal* terdiri dari huruf kecil, secara spesifik huruf `b`, `d`, `p`, dan `q`.

**Keputusan: DIPERTAHANKAN (Tidak Dihapus)**

**Rasionalisasi Medis & Teknis:**
1. **Golden Feature Disleksia:** Kesulitan membedakan arah (kiri/kanan) pada huruf simetris (`b` vs `d`, `p` vs `q`) adalah salah satu gejala klinis paling mendasar pada anak penderita disleksia (*Reversal Error*). 
2. **Kesesuaian Medis:** Keberadaan 4 huruf kecil ini di dalam kelas *Reversal* bukanlah sebuah ketidaksengajaan (noise), melainkan sampel berharga yang merepresentasikan kondisi medis pasien di dunia nyata.
3. Menghapus data ini sama dengan menghilangkan kemampuan model AI untuk mempelajari salah satu ciri utama penyakit disleksia.

### B. Anomali Artefak pada Augmentasi Warna
**Konteks Masalah:**
Sekitar 3.000 gambar hasil augmentasi warna menghasilkan artefak berupa blok/garis putih di bagian ujung/tepi gambar akibat proses *thresholding* atau *cropping* yang tidak sempurna.

**Keputusan: DIHAPUS (Drop dari Dataset)**

**Rasionalisasi Teknis:**
1. **Risiko Data Leakage (Shortcut Learning):** Model CNN cenderung mencari jalan pintas termudah untuk membedakan kelas. Jika blok putih ini sering muncul pada gambar hasil augmentasi (yang mendominasi kelas tertentu), CNN akan belajar mendeteksi keberadaan "blok putih" dan mengabaikan bentuk huruf utamanya. Nanti akurasinya terlihat tinggi palsu.
2. **Kehancuran Fitur Turunan Matematis:** Adanya piksel putih di tepi gambar akan merusak metrik ekstraksi fitur:
   *   `bounding_box_ratio`: Kotak pembatas (*bounding box*) akan tertarik menutupi seluruh gambar (28x28), sehingga rasio tinggi/lebar huruf aslinya menjadi rusak.
   *   `center_of_mass`: Pusat gravitasi massa tinta akan melenceng jauh dari posisi huruf yang sebenarnya.
3. Karena jumlah gambar anomali ini hanya ~3.000 (kurang dari 2% total dataset), menghapusnya adalah cara paling efisien dan aman tanpa mengurangi integritas dataset secara signifikan.

---

## 2. Strategi Ekstraksi Dataset EMNIST (Data Normal)

### A. Dilema Pemilihan Kelas (Shape Bias vs Generalisasi)
Untuk menyeimbangkan kelas Disleksia, diperlukan dataset normal dari EMNIST. Muncul dilema:
*   *Jika hanya mengambil A-Z + b,d,p,q:* Model sangat fokus pada segi medis, namun akan gagal (*error*) jika pengguna menulis kalimat bebas yang mengandung huruf lain.
*   *Jika mengambil A-Z + a-z:* Model bisa mengenali semua tulisan di kalimat bebas, namun berisiko bias (misal: menganggap bentuk huruf 'a' atau 'g' pasti Normal karena tidak ada di dataset Gambo).

**Keputusan Akhir: Ekstrak SEMUA variasi abjad EMNIST (A-Z dan a-z / Kelas 10-61)**

**Rasionalisasi UX (User Experience):**
*   Target produk akhir akan memberikan **Kertas Grid Kosong** kepada *user* (orang tua/guru) yang mengizinkan anak untuk menyalin/menulis kata atau kalimat bebas. 
*   Jika model hanya dilatih pada huruf spesifik, fitur Translasi (OCR) akan gagal membaca kata yang ditulis. Dengan mengekstrak seluruh abjad, AI dibekali "kamus" tulisan normal yang lengkap, sehingga kebal terhadap input OOV (*Out-of-Vocabulary*).

### B. Penanganan Class Imbalance (Ketidakseimbangan Kelas)
EMNIST memiliki ratusan ribu gambar. Memasukkan seluruhnya akan menenggelamkan rasio dataset Gambo.
*   **Strategi Wajib:** Dilakukan **Stratified Random Sampling** pada EMNIST.
*   Total gambar yang diambil dari EMNIST harus dibatasi agar seimbang (Rasio 1:1) dengan total kelas Disleksia dari Gambo.
*   **Implementasi Python:**
    ```python
    # Mengambil kelas 10 hingga 61 (A-Z dan a-z)
    valid_classes = list(range(10, 62))  
    emnist_filtered = emnist_df[emnist_df['label'].isin(valid_classes)]
    
    # Sampling acak seimbang per kelas (misal: n=1500 per abjad)
    emnist_sampled = emnist_filtered.groupby('label').sample(n=1500, random_state=42, replace=True)
    ```

---

## 3. Arsitektur Pemisahan Alur Utama (Plan A)

Untuk menangani risiko bias abjad (*Shape Bias*) seperti yang dibahas di atas, dirancang arsitektur sistem cerdas yang memisahkan proses pengenalan tulisan dan diagnosa medis ke dalam dua jalur model (pendekatan *Shape-Agnostic*):

### Komponen 1: Fitur Translasi (OCR)
*   **Fungsi:** Mengubah gambar tulisan anak menjadi teks digital.
*   **Mekanisme:** Sepenuhnya mengandalkan model Computer Vision (CNN kustom atau API eksternal) yang dilatih menggunakan seluruh abjad EMNIST (A-Z, a-z).
*   **Fokus:** Mempelajari **BENTUK (Shape)** dari masing-masing karakter huruf.

### Komponen 2: Fitur Diagnosa Disleksia (Multi-Modal CNN Architecture)
*   **Fungsi:** Menentukan probabilitas keberadaan indikasi disleksia (Normal vs Dyslexia).
*   **Mekanisme:** Menggunakan pendekatan **Late Fusion (Multi-Input Neural Network)** yang menggabungkan kekuatan ekstraksi fitur otomatis dari CNN dengan fitur matematis klinis:
    *   **Cabang 1 (Visual):** Model CNN menerima gambar matriks 28x28 untuk mengekstrak pola kompleks spasial (bentuk, tekstur, lekukan).
    *   **Cabang 2 (Klinis/Tabular):** Model memproses **5 Fitur Turunan Matematis** dari matriks piksel ke dalam arsitektur *Dense Layers*.
    *   **Penggabungan (Concatenation):** Vektor hasil dari kedua cabang ini digabungkan (*concatenate*) sebelum diteruskan ke layer klasifikasi prediksi akhir.
*   **Penjelasan 5 Fitur Matematis (Feature Engineering):**
    1.  `ink_density`: Mendeteksi ketebalan tulisan akibat *over-tracing* atau penekanan pensil berulang.
    2.  `center_of_mass_x`: Mendeteksi distorsi orientasi kemiringan secara horizontal.
    3.  `center_of_mass_y`: Mendeteksi tulisan yang melayang keluar batas garis bayangan secara vertikal.
    4.  `bounding_box_ratio`: Mengidentifikasi proporsi huruf yang hancur, terlalu memanjang, atau terlalu memipih.
    5.  `stroke_transitions`: Mengukur fluktuasi garis (transisi piksel putih ke hitam ke putih) sebagai indikator getaran tangan (*tremor*) atau motorik halus yang terhambat.
*   **Keunggulan Masterplan Arsitektur:** Penggabungan ini bertindak sebagai **Strong Regularization**. Meskipun CNN dilatih menggunakan gambar huruf, keberadaan 5 fitur turunan matematis akan "memaksa" CNN untuk tidak terjebak pada bias bentuk huruf (*Shape Bias*). CNN menjadi terarah untuk secara murni memperhatikan kualitas eksekusi goresan motorik anak tersebut.

---

## Rencana Cadangan Darurat (Plan B)

Jika proses integrasi *Feature Engineering* ke dalam Machine Learning Tabular terlalu kompleks atau terhambat oleh *deadline* Capstone, sistem akan diturunkan (*downgrade*) ke pendekatan konservatif:
*   **Skenario:** Aplikasi tidak menggunakan kertas grid kosong. Sistem akan mem-*generate* file PDF berisi contoh huruf atau frasa kaku (misal: "APA KABAR") dengan panduan tipis.
*   Anak hanya akan menyalin ulang huruf tersebut secara repetitif (menurun ke bawah).
*   **Status Plan B:** **DITAHAN (On-Hold).** Plan A dinilai jauh lebih elegan, dinamis, superior dalam segi UX, dan menunjukkan *engineering maturity* yang mengesankan untuk standar penilaian Capstone. Plan B hanya dieksekusi sebagai *last resort*.
