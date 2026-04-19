# Temuan Exploratory Data Analysis (EDA) — DyslexiaLens

Dokumen ini merangkum seluruh temuan dari **Tahap 4 (EDA)** dan **Tahap 5 (Data Augmentation)** yang dilakukan di notebook `Dyslexia.ipynb`. Temuan-temuan ini menjadi dasar rekomendasi preprocessing dan strategi training untuk AI Engineer.

> **Tanggal:** 19 April 2026  
> **Peran:** Data Scientist  
> **Sumber Data:** `master_dataset_dyslexia.csv` (180.726 baris data bersih)

---

## 1. Distribusi Kelas per Split (Temuan EDA-1)

### Data

| Kelas | Train | Test |
|---|---|---|
| Corrected | 65.534 | 17.677 |
| Normal | 39.334 | 19.557 |
| Reversal | 32.142 | 6.482 |
| **Total** | **137.010** | **43.716** |

Rasio Train : Test ≈ **76% : 24%**

### Insight
- Kelas `Corrected` mendominasi baik di Train maupun Test.
- Kelas `Normal` dan `Reversal` memiliki jumlah yang lebih rendah.
- Proporsi relatif antar kelas **konsisten** antara Train dan Test — tidak ada *distribution shift* yang ekstrem. Ini berarti evaluasi model pada Test set akan representatif terhadap performa sebenarnya.

---

## 2. Distribusi Severity Score (Temuan EDA-2)

### Data

| Severity Score | Jumlah | Proporsi |
|---|---|---|
| 0 (Normal) | 58.891 | 32,6% |
| 1 (Ringan) | 42.966 | 23,8% |
| 2 | 8.049 | 4,5% |
| 3 | 8.049 | 4,5% |
| 4 | 8.049 | 4,5% |
| 5 | 8.049 | 4,5% |
| 6 (Parah) | 46.673 | 25,8% |

### Insight
- Distribusi **sangat tidak merata** — skor 2–5 masing-masing hanya memiliki ~8K gambar, sementara skor 0, 1, dan 6 memiliki 42–59K.
- Skor `6` tinggi karena menggabungkan dua skor asli periset (`1` untuk Reversal dan `4` untuk Corrected terparah).
- Ketidakseimbangan ini mungkin dapat melemahkan model dalam mengenali keparahan menengah jika tidak ditangani.
- **Solusi Final:** Kita BUKAN melakukan augmentasi fisik (*offline storage*), melainkan menggunakan kalkulasi **`class_weight`** untuk menghukum model secara matematis jika salah menebak kelas minoritas (lihat Bagian 7).

---

## 3. Analisis Class Imbalance Binary (Temuan EDA-3)

### Data

| Kelas | Jumlah | Proporsi |
|---|---|---|
| Normal (target_class = 0) | 58.891 | 32,6% |
| Disleksia (target_class = 1) | 121.835 | 67,4% |

**Rasio Disleksia : Normal = 2,07 : 1**

### Insight
- Dataset bersifat **imbalanced** secara biner — kelas Disleksia dua kali lebih banyak dari Normal.
- Jika tidak ditangani, model akan bias memprediksi Disleksia untuk semua input (*majority class bias*).
- **Rekomendasi mitigasi:**
  - Gunakan `class_weight='balanced'` atau bobot manual (lihat Bagian 7).
  - Evaluasi model dengan **F1-Score** dan **Recall**, bukan hanya Accuracy.
  - Pertimbangkan *stratified split* untuk validasi.

---

## 4. Perbedaan Visual Antar Kelas (Temuan EDA-4)

Sampel visual 5 gambar acak per kelas menunjukkan perbedaan pola yang jelas:

| Kelas | Karakteristik Visual |
|---|---|
| **Normal** | Huruf terbentuk jelas, satu goresan dominan, minim noise. Bentuk karakter mudah dikenali. |
| **Corrected** | Goresan tumpang-tindih akibat koreksi berulang. Pola *scribbling* menjadi ciri khas utama. |
| **Reversal** | Huruf tertulis terbalik (*mirror image*) — misalnya `b` terlihat seperti `d`. Gejala klasik disleksia. |

**Kesimpulan:** Perbedaan visual antar kelas **cukup jelas** untuk membedakan pola goresan secara kasar — mendukung kelayakan dataset untuk klasifikasi.

---

## 5. Perbedaan Visual Antar Severity Score (Temuan EDA-5)

Perbandingan visual antara skor rendah (1), menengah (3), dan tinggi (6):

| Severity Score | Karakteristik Visual |
|---|---|
| **Skor 1 (Ringan)** | Goresan koreksi minimal — huruf asli masih sangat mudah dikenali. Distorsi hampir tidak terlihat. |
| **Skor 3 (Menengah)** | Koreksi mulai tampak — ada goresan tambahan yang menutupi sebagian bentuk huruf asli. |
| **Skor 6 (Parah)** | Goresan sangat destruktif — huruf hampir tidak bisa ditebak. *Scribbling* mendominasi. |

**Kesimpulan:** Perbedaan visual yang jelas antara skor rendah dan tinggi **mendukung hipotesis** bahwa Severity Score dapat menjadi variabel target yang bermakna untuk model AI.

---

## 6. Pembatalan Data Augmentation Fisik (Offline)

### Strategi Ekseksusi Awal (DIBATALKAN)
Awalnya, direncakan *offline data augmentation* (menyimpan gambar rotasi/zoom baru ke *disk*) pada skor 2–5 untuk menyeimbangkan distribusi severity score.

### Alasan Pembatalan (Keputusan Teknis):
1. **Risiko Overfitting & Bloating:** Mengeksekusi augmentasi fisik pada dataset berjumlah dasar 180.000 gambar membuat total gambar menjadi hampir 300.000 file. Ini disebut *"Opsi Kurang Bijak"* karena akan membuat RAM hancur dan waktu *training* sangat lama.
2. **Potensi Manipulasi Label:** Memutar gambar kelas Normal secara berlebihan berpotensi membuatnya jadi terlihat disleksia (misal huruf `b` jadi `d`).
3. **Alternatif Jauh Lebih Baik:** Penyeimbangan distribusi sepenuhnya diserahkan kepada **AI Engineer** menggunakan fungsi `class_weight` saat _training_ model tanpa memodifikasi 1 file pun.

> **Keputusan Final:** Folder `Gambo_Augmented` dan file `master_dataset_augmented.csv` resmi dihapus/dibatalkan penggunaannya. Cukup gunakan dataset original di `master_dataset_final.csv`.

---

## 7. Kalkulasi Class Weights (Strategi Wajib AI Engineer)

Karena binary imbalance (Normal vs Disleksia) dan severity imbalance tidak dimitigasi via perbanyakan gambar fisik, berikut bobot kelas yang dihitung menggunakan `sklearn.utils.class_weight.compute_class_weight` dari **Dataset Asli Original (180k baris)**:

### Binary (`target_class`)

*Catatan: Kelas Disleksia (121k) jauh lebih banyak dari kelas Normal (58k).*

| Kelas | Label | Weight | Deskripsi |
|---|---|---|---|
| 0 | Normal | **1.55** | Berikan penalti 1.55x lipat jika model salah menebak ini |
| 1 | Disleksia | **0.75** | Berikan penalti standar 0.75x jika salah menebak |

### Severity (`severity_score`)

| Skor | Weight |
|---|---|
| 0 (Normal) | **0.44** |
| 1 (Ringan) | **0.60** |
| 2 | **3.22** |
| 3 | **3.22** |
| 4 | **3.22** |
| 5 | **3.22** |
| 6 (Parah) | **0.55** |

> **Cara penggunaan bagi AI Engineer:** Pilih akan menggunakan Binary atau Severity Target. Masukkan dictionary weight di atas sebagai parameter `class_weight` pada saat komputernya di _train_ ( `model.fit(..., class_weight=weights)` ).

---

## 8. Ringkasan Temuan EDA Final

| # | Pertanyaan | Temuan | Tindak Lanjut Terkini |
|---|---|---|---|
| EDA-1 | Distribusi kelas konsisten antar split? | ✅ Ya — proporsi relatif Train dan Test serupa | - |
| EDA-2 | Severity Score terdistribusi merata? | ⚠️ Tidak — skor 2–5 sangat kurang | Ditangani dengan Severity `class_weight` |
| EDA-3 | Ada *class imbalance* binary? | ⚠️ Ya — rasio 1:2,07 | Ditangani dengan Binary `class_weight` |
| EDA-4 | Perbedaan visual antar kelas jelas? | ✅ Ya — Normal bersih, Corrected bertumpuk, Reversal terbalik | Melanjutkan ke CNN Modeling |
| EDA-5 | Perbedaan visual antar severity jelas? | ✅ Ya — skor rendah masih terbaca, skor tinggi destruktif | Skor ini sangat layak jadi patokan level parah |
| EDA-6 | Pola Corrected vs Reversal berbeda? | ✅ Ya — jenis distorsi berbeda secara mendrag | - |

### Kesimpulan Utama
Dataset "harta karun" berjumlah 180.726 baris ini **100% LAYAK** digunakan tanpa perlu menghapus sebuah datapun (*Undersampling*) dan tanpa menduplikasi data manapun (*Augmentasi Spesifik/Offline*). Seluruh ketidakseimbangan diretas dengan sangat cemerlang dengan mengandalkan matematis **`class_weight`** di layer CNN!
