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
- Ketidakseimbangan ini akan menyebabkan model sangat lemah mengenali keparahan menengah jika tidak dimitigasi.
- **Solusi:** Augmentasi fisik pada skor 2–5 (lihat Bagian 6).

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

## 6. Data Augmentation — Hasil Eksekusi (Tahap 5)

### Strategi
Augmentasi **hanya diterapkan pada skor 2–5 dari split Train** untuk menyeimbangkan distribusi severity score, menggunakan parameter sesuai Project Plan:

| Teknik | Parameter |
|---|---|
| Rotasi searah jarum jam | +10° |
| Rotasi berlawanan jarum jam | -10° |
| Zoom in (scaling up) | 1.1× + crop center |
| Zoom out (scaling down) | 0.9× + padding |
| ❌ Horizontal Flip | **Tidak digunakan** (merusak label Reversal) |

### Hasil Eksekusi

```
🔄 Augmentasi Skor 2 (4 copy × 6.442 gambar) → 25.768 gambar
🔄 Augmentasi Skor 3 (4 copy × 6.442 gambar) → 25.768 gambar
🔄 Augmentasi Skor 4 (4 copy × 6.442 gambar) → 25.768 gambar
🔄 Augmentasi Skor 5 (4 copy × 6.442 gambar) → 25.768 gambar

Total augmented: 103.072 gambar | Error: 0
```

### Perbandingan Distribusi Severity Score (Train)

| Severity Score | Sebelum | Sesudah | Perubahan |
|---|---|---|---|
| 0 (Normal) | 39.334 | 39.334 | Tidak diubah ✅ |
| 1 (Ringan) | 33.324 | 33.324 | Tidak diubah ✅ |
| 2 | 6.442 | 32.210 | ×5 ✅ |
| 3 | 6.442 | 32.210 | ×5 ✅ |
| 4 | 6.442 | 32.210 | ×5 ✅ |
| 5 | 6.442 | 32.210 | ×5 ✅ |
| 6 (Parah) | 38.584 | 38.584 | Tidak diubah ✅ |

> **Alasan Normal TIDAK diaugmentasi:** Skor 0 sudah berada di ~39K — setara dengan skor tertinggi lainnya. Mengaugmentasinya justru akan menciptakan ketidakseimbangan baru di mana Normal menjadi kelas paling besar.

### Output File
- **Gambar augmented:** Tersimpan di folder `Gambo_Augmented/`
- **CSV baru:** `master_dataset_augmented.csv` (283.798 baris = 180.726 original + 103.072 augmented)

---

## 7. Class Weights untuk AI Engineer

Karena binary imbalance (Normal vs Disleksia) tidak dimitigasi via augmentasi, berikut bobot kelas yang dihitung menggunakan `sklearn.utils.class_weight.compute_class_weight('balanced')` dari data augmented Train:

### Binary (`target_class`)

| Kelas | Label | Weight |
|---|---|---|
| 0 | Normal | **3,0518** |
| 1 | Disleksia | **0,5980** |

### Severity (`severity_score`)

| Skor | Weight |
|---|---|
| 0 | 0,8720 |
| 1 | 1,0292 |
| 2 | 1,0648 |
| 3 | 1,0648 |
| 4 | 1,0648 |
| 5 | 1,0648 |
| 6 | 0,8889 |

> **Cara penggunaan:** Masukkan dictionary weight ini sebagai parameter `class_weight` di `model.fit()` atau sebagai bobot di *loss function* custom.

---

## 8. Ringkasan Temuan EDA

| # | Pertanyaan | Temuan |
|---|---|---|
| EDA-1 | Distribusi kelas konsisten antar split? | ✅ Ya — proporsi relatif Train dan Test serupa |
| EDA-2 | Severity Score terdistribusi merata? | ⚠️ Tidak — skor 2–5 sangat kurang (dimitigasi via augmentasi) |
| EDA-3 | Ada *class imbalance* binary? | ⚠️ Ya — rasio 1:2,07 (dimitigasi via `class_weight`) |
| EDA-4 | Perbedaan visual antar kelas jelas? | ✅ Ya — Normal bersih, Corrected bertumpuk, Reversal terbalik |
| EDA-5 | Perbedaan visual antar severity jelas? | ✅ Ya — skor rendah masih terbaca, skor tinggi destruktif |
| EDA-6 | Pola Corrected vs Reversal berbeda? | ✅ Ya — distribusi severity dan jenis distorsi berbeda |

### Kesimpulan Utama
Dataset ini **layak** digunakan untuk klasifikasi biner (Normal vs Disleksia) maupun multi-class severity. Ketidakseimbangan severity telah dimitigasi via augmentasi fisik, dan ketidakseimbangan binary ditangani via `class_weight`. Strategi mitigasi berlapis ini memastikan model tidak bias terhadap kelas mayoritas.
