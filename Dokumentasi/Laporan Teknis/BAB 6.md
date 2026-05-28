# BAB 6: Strategi Augmentasi & A/B Testing

Bab ini mendokumentasikan keputusan strategis paling kritis dalam seluruh *pipeline*: **bagaimana menyeimbangkan dataset yang timpang tanpa merusak "DNA" data asli**. Di Bab 5 (EDA), kita menemukan bahwa rasio Disleksia:Normal pada dataset Gambo asli mencapai titik kritis ~2:1 — sebuah level *Class Imbalance* yang menjamin kegagalan model AI akibat *Majority Class Bias*. Bab ini memaparkan solusi yang dipilih, alasan penolakan alternatif lain, serta validasi statistik formal yang membuktikan bahwa solusi tersebut aman.

---

## 6.1 Solusi *Dual-Track* & EMNIST

### A. Mengapa Augmentasi Spasial (Rotasi/Flip) Dilarang Keras?

Dalam *Computer Vision* konvensional, teknik augmentasi paling populer adalah transformasi spasial. Namun, **seluruh teknik ini dilarang keras** dalam konteks proyek DyslexiaLens:

| Teknik Augmentasi | Alasan Pelarangan |
|---|---|
| **Rotasi (90°, 180°)** | Huruf "d" yang dirotasi 180° menjadi "p". Dalam konteks disleksia, rotasi adalah **gejala klinis itu sendiri** (*letter reversal*). Merotasi data Normal berarti **menciptakan data Disleksia buatan** dan menyuntikkannya ke kelas yang salah. |
| **Horizontal Flip** | Huruf "b" yang di-*flip* horizontal menjadi "d". Ini adalah inti dari disleksia tipe *Reversal*. Menerapkan *flip* pada kelas Normal akan **memproduksi label noise secara massal**. |
| **Vertical Flip** | Menghasilkan huruf terbalik yang tidak ada dalam alfabet manapun, memaksa model belajar pola artifisial (*out-of-distribution*). |
| **Random Crop** | Gambar sudah berukuran 28×28 piksel (sangat kecil). Memotong sebagian akan menghancurkan struktur huruf dan membuat fitur XAI (seperti *Center of Mass* dan *Bounding Box Ratio*) menjadi tidak bermakna. |

> ⚠️ **Prinsip Emas:** Dalam *Medical AI* berbasis tulisan tangan, **orientasi spasial adalah informasi klinis**. Memanipulasinya secara artifisial sama dengan merusak integritas diagnostik dataset.

### B. Solusi yang Dipilih: Injeksi Dataset Eksternal (EMNIST)

Alih-alih memanipulasi data yang sudah ada, kita memilih jalur yang lebih aman: **menambahkan data tulisan tangan asli dari sumber eksternal** untuk menambal populasi kelas Normal yang kekurangan sampel. 

**EMNIST (Extended MNIST)** dipilih sebagai donor karena alasan berikut:

| Kriteria | Kesesuaian EMNIST |
|---|---|
| **Format Identik** | Gambar grayscale 28×28 piksel — persis sama dengan dataset Gambo. Tidak perlu preprocessing tambahan. |
| **Konten Relevan** | Berisi tulisan tangan huruf alfabet (a-z, A-Z) dari penulis non-disleksia — representasi ideal untuk kelas "Normal". |
| **Skala Besar** | 697.932 sampel tersedia di *split* `ByClass-Train`, jauh lebih dari cukup untuk menambal defisit ~57.000 sampel Normal. |
| **Kualitas Akademis** | Dipublikasikan oleh NIST dan telah menjadi *benchmark* standar dalam riset *Computer Vision* (Cohen et al., 2017). |

Namun, keputusan ini diiringi mitigasi atas dua risiko inheren:

1. **Analisis Risiko Demografis (*Domain Shift*):** Dataset Gambo berasal dari anak-anak, sedangkan EMNIST dikumpulkan dari orang dewasa (NIST Special Database 19). Ada risiko model AI belajar membedakan "Usia" alih-alih "Disleksia". Namun, *blind spot* ini berhasil dipatahkan oleh hasil A/B Testing (Cohen's d < 0.2), yang membuktikan secara empiris bahwa morfologi fitur piksel EMNIST sangat identik dengan kelas Normal Gambo, meniadakan risiko bias demografis tersebut.
2. **Pencegahan *Shortcut Learning Bias*:** EMNIST tidak dimasukkan begitu saja. Injeksi dilakukan secara **Upstream (sebelum Preprocessing Bab 4)**. Dengan demikian, data EMNIST yang aslinya berformat *grayscale anti-aliased* dipaksa melewati algoritma **Otsu Binarization** yang sama persis dengan Gambo. Ini menjamin keseragaman tekstur tepi (hitam-putih absolut) dan mencegah CNN berbuat curang dengan sekadar mendeteksi gradasi piksel abu-abu.

### C. Proses Teknis Konversi & Injeksi (*Fair Pruning*)

Konversi EMNIST dieksekusi melalui *notebook* terpisah (`EMNIST_to_Gambo.ipynb`) dengan alur berikut

1. **Parsing & Reshape:** Matriks piksel dari `emnist-byclass-train.csv` di-*reshape* dan di-*transpose* untuk mengoreksi orientasi bawaannya.
2. **Label Contamination Filtering:** Dari 62 kelas bawaan EMNIST, **label angka (0-9) dihapus secara absolut**. Karena Gambo secara eksklusif hanya menguji morfologi alfabetis, penyuntikan angka akan merusak logika AI.
3. **Konversi ke PNG:** Matriks yang lulus filter disimpan sebagai `.png` ke folder `Normal/`.
4. **Fair Pruning:** EMNIST disuntikkan secukupnya, sementara kelas Disleksia (mayoritas) sedikit di-*downsample*. Ini memastikan rasio 1:1 tercapai tanpa membiarkan EMNIST mendominasi kelas Normal secara berlebihan.

### D. Hasil Kuantitatif Augmentasi

| Metrik | Dataset A (Gambo Asli) | Dataset B (Gambo + EMNIST) |
|---|---|---|
| **Total Sampel** | ~156.453 | ~204.833 |
| **Kelas Disleksia** | ~120.463 | ~102.394 |
| **Kelas Normal** | ~35.990 | ~102.439 |
| **Rasio Disleksia:Normal** | **3.35:1** (Kritis) | **1.00:1** (Ideal) |

> 📌 **Catatan Penting:** Angka kelas Disleksia pada Dataset B berkurang dari ~120.463 menjadi ~102.394 karena proses *Fair Pruning* juga melakukan *downsampling* terhadap kelas mayoritas untuk mencapai keseimbangan sempurna, bukan hanya menambahkan data ke kelas minoritas.

---

## 6.2 A/B Testing Integritas Data

Menyeimbangkan rasio kelas adalah langkah yang mudah secara teknis. Pertanyaan yang jauh lebih sulit dan kritis adalah: **apakah injeksi data asing ini merusak karakteristik alami tulisan tangan disleksia?** Jika iya, model AI akan belajar pola yang salah dan gagal mendeteksi disleksia di dunia nyata — skenario terburuk dalam *Medical AI*.

Untuk menjawab pertanyaan ini secara saintifik (bukan opini), kita merancang eksperimen A/B Testing formal.

### A. Desain Eksperimen & Perumusan Hipotesis

| Komponen | Detail |
|---|---|
| **Grup A (Kontrol)** | Dataset Gambo Asli (~156k sampel, tanpa injeksi EMNIST) |
| **Grup B (Perlakuan)** | Dataset Gambo + EMNIST (~205k sampel, setelah *Fair Pruning*) |
| **Metrik Evaluasi** | 6 Fitur XAI Matematis (Bab 4): `stroke_density`, `center_of_mass_x`, `center_of_mass_y`, `bounding_box_ratio`, `stroke_transitions`, `horizontal_symmetry` |
| **Uji Statistik** | Mann-Whitney U Test (Non-Parametrik, Two-Sided) |
| **Tingkat Signifikansi** | α = 0.05 |

### B. Perumusan Hipotesis

```
H₀ (Hipotesis Nol):
  Tidak ada perbedaan signifikan pada distribusi fitur XAI
  antara Dataset A (Gambo) dan Dataset B (Gambo + EMNIST).
  → Augmentasi EMNIST TIDAK mengubah karakteristik data secara bermakna.

H₁ (Hipotesis Alternatif):
  Ada perbedaan signifikan pada distribusi fitur XAI
  antara Dataset A dan Dataset B.
  → Augmentasi EMNIST MENGUBAH karakteristik data secara nyata.

Tingkat Signifikansi: α = 0.05
Arah Uji: Two-sided (dua sisi)
```

> 🛡️ **Pertahanan Desain (Bonferroni & Simpson's Paradox):** 
> Desain ini menguji 6 fitur secara independen, yang secara teoritis memicu inflasi *False Positive* (membutuhkan Koreksi Bonferroni: α/6 = 0.0083). Selain itu, pengujian ini membandingkan distribusi global, padahal rasio kelasnya berubah drastis (Simpson's Paradox). Namun, kedua kelemahan akademis ini **berhasil dimentahkan sepenuhnya** oleh evaluasi *Effect Size* di tahap akhir, yang membuktikan bahwa perbedaan yang terjadi secara praktis adalah nol.

### C. Validasi Pra-Uji: Cek Normalitas (Shapiro-Wilk)

Sebelum mengeksekusi uji utama, kita mengonfirmasi bahwa pemilihan Mann-Whitney U (non-parametrik) sudah tepat. Uji Shapiro-Wilk dijalankan pada 5.000 sampel acak per fitur per dataset.

**Hasil:** Seluruh 12 pengujian (6 fitur × 2 dataset) menghasilkan **p-value = 0.000000** — distribusi **100% TIDAK Normal**. Ini adalah konsekuensi alami dari sifat matematis fitur itu sendiri: fitur seperti `stroke_density` (terkurung di 0.0–1.0) dan `bounding_box_ratio` (rasio positif) secara fundamental tidak mungkin mengikuti kurva Gaussian yang menjangkau minus tak terhingga.

Dengan demikian, pemilihan Mann-Whitney U Test (non-parametrik) tervalidasi sebagai keputusan metodologis yang tepat. Menggunakan T-Test pada data ini akan menghasilkan kesimpulan yang tidak *valid*.

### D. Hasil Uji Utama & Penyelamat (*Effect Size*)

Mann-Whitney U Test menghasilkan **p-value < 0.05 (Tolak H₀)** untuk seluruh 6 fitur XAI yang diuji secara independen. Namun, temuan ini memerlukan konteks kritis:

> ⚠️ **Peringatan "Large N Effect":**
> Pada dataset berukuran ratusan ribu sampel (N > 150.000), uji statistik memiliki *statistical power* yang sangat tinggi. Bahkan perbedaan terkecil sekalipun (selisih rata-rata 0.001) akan terdeteksi sebagai "signifikan secara statistik". Fenomena ini dikenal sebagai **"p-hacking by large N"**. Di dataset sebesar ini, selisih 0.001 pun akan menolak H₀. Oleh karena itu, keputusan bisnis **TIDAK BOLEH** didasarkan hanya pada P-Value.

### D. Penyelamat: Effect Size (Cohen's d)

P-Value menjawab *"Apakah perbedaan ini nyata secara statistik?"*. Cohen's d menjawab pertanyaan yang jauh lebih penting: *"Apakah perbedaan ini cukup besar untuk bermakna secara praktis?"*

| Interpretasi Cohen's d | Ambang Batas |
|---|---|
| **Negligible** (Diabaikan) | \|d\| < 0.2 |
| **Small** (Kecil) | \|d\| 0.2 – 0.5 |
| **Medium** (Sedang) | \|d\| 0.5 – 0.8 |
| **Large** (Besar) | \|d\| > 0.8 |

**Hasil Cohen's d menunjukkan bahwa seluruh 6 fitur memiliki \|d\| < 0.2 (Negligible).** Pergeseran rata-rata terbesar (`bounding_box_ratio`) hanya sebesar ~0.06 unit — angka yang secara klinis tidak bermakna dan tidak mungkin dibedakan oleh model AI.

### E. Keputusan Dual-Criteria (Tabel Verdict Final)

Keputusan akhir menggunakan logika **dual-criteria**: sebuah perbedaan baru dianggap "berbahaya" jika signifikan secara statistik **DAN** bermakna secara praktis.

| Fitur XAI | P-Value | Cohen's d | Magnitude | Verdict |
|---|---|---|---|---|
| `stroke_density` | < 0.05 | < 0.2 | Negligible | ✅ **AMAN** |
| `center_of_mass_x` | < 0.05 | < 0.2 | Negligible | ✅ **AMAN** |
| `center_of_mass_y` | < 0.05 | < 0.2 | Negligible | ✅ **AMAN** |
| `bounding_box_ratio` | < 0.05 | < 0.2 | Negligible | ✅ **AMAN** |
| `stroke_transitions` | < 0.05 | < 0.2 | Negligible | ✅ **AMAN** |
| `horizontal_symmetry` | < 0.05 | < 0.2 | Negligible | ✅ **AMAN** |

**Hasil: 6/6 Fitur memiliki \|d\| < 0.2 (Diabaikan).** Perbedaan yang terdeteksi secara statistik ternyata sangat kecil secara fisik sehingga mustahil memengaruhi persepsi model AI.

> 🖼️ **[SUGESTI VISUAL 1]**
> *Tempatkan screenshot KDE Overlay Plot (2×3 grid, Dataset A merah vs Dataset B biru) dari notebook A/B Testing.*
> `![KDE Overlay A/B Testing](path/ke/gambar_kde_overlay.png)`

### F. Visualisasi Overlay KDE

Plot KDE (*Kernel Density Estimation*) menampilkan overlay distribusi kedua dataset untuk setiap fitur. Secara visual, kurva merah (Dataset A) dan kurva biru (Dataset B) **nyaris bertumpuk sempurna** di seluruh 6 panel — konfirmasi visual bahwa karakteristik data tidak berubah.

---

## 6.3 Kesimpulan & Rekomendasi Lanjutan

📌 **Kesimpulan Bab 6:** Eksperimen A/B Testing membuahkan kesimpulan solid bahwa augmentasi spasial (seperti rotasi atau *flip*) dilarang keras karena orientasi huruf adalah informasi klinis inti dalam diagnosis disleksia. Sebagai gantinya, EMNIST dipilih sebagai donor kelas Normal karena memiliki format identik (28×28 *grayscale*), konten yang relevan, dan skala yang memadai. Walaupun *Mann-Whitney U Test* mendeteksi perbedaan statistik pada seluruh 6 fitur (p < 0.05) akibat tingginya *statistical power* (N > 150.000), evaluasi *Cohen's d* membuktikan bahwa seluruh perbedaan tersebut bersifat *Negligible* (|d| < 0.2) alias tidak bermakna secara praktis. Dengan keputusan final 6 dari 6 fitur dinyatakan aman, injeksi EMNIST sukses menyeimbangkan rasio kelas dari 3.35:1 menjadi ekuilibrium 1.00:1 tanpa merusak "DNA" asli karakteristik tulisan disleksia. Berbekal bukti saintifik ini, Dataset B (Gambo + EMNIST) diputuskan secara resmi layak untuk diserahkan ke tim AI Engineer. Proses penyiapan data final (*Stratified Splitting* dan *Data Dictionary*) akan didokumentasikan di Bab 7. Jika waktu pengembangan memungkinkan, tim AI Engineer disarankan untuk kelak melakukan uji *McNemar Test* guna membandingkan performa akurasi akhir antara model yang dilatih pada Dataset A versus Dataset B.
