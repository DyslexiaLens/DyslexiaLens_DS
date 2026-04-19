# Laporan Analisis Dataset (DyslexiaLens)

Berdasarkan analisis mendalam pada dataset `Gambo` — termasuk inspeksi visual manual dan *audit* algoritmik — berikut adalah laporan komprehensif yang mencakup revisi dan koreksi asumsi awal, serta keputusan-keputusan teknis final untuk proyek **DyslexiaLens**.

> [!NOTE]
> Dokumen ini telah **direvisi** dari versi awal. Asumsi awal mengenai *data leakage* telah **gugur** setelah ditemukan fakta bahwa nama folder numerik (1, 4, 5, 6, 7, 8, 9) bukan merepresentasikan karakter angka, melainkan **Tingkat Keparahan Coretan (Severity Score)**. Seluruh kelas berisi distribusi abjad huruf yang beragam secara merata.

---

## 1. Ringkasan
Dataset **Gambo** berisi **208.372 gambar** yang dibagi ke dalam dua folder utama (`Train` dan `Test`). Dataset ini berfokus pada sampel tulisan tangan satu karakter yang merepresentasikan tiga kondisi: tulisan disleksia yang dikoreksi (`Corrected`), tulisan dengan pembalikan arah huruf (`Reversal`), dan tulisan tangan normal (`Normal`).

* **Data Bersih** (setelah *drop* kontaminasi): **~180.726 file**
* **Sumber data kotor yang dibuang**: file `NormalXXXX.png` yang terselip di folder non-Normal.

## 2. Analisis Struktur Folder
Struktur folder menggunakan hierarki standar `Split/Class` untuk PyTorch/Keras:
* **Train** (Total: 151.649 gambar)
  * `Corrected` (65.534 gambar) — Berisi berbagai abjad + angka yang dikoreksi
  * `Normal` (39.334 gambar) — Berisi berbagai abjad ditulis dengan wajar
  * `Reversal` (46.781 gambar) — Berisi karakter rawan terbalik: `b, d, j`, dan `1`
* **Test** (Total: 56.723 gambar)
  * `Corrected` (19.284 gambar)
  * `Normal` (19.557 gambar)
  * `Reversal` (17.882 gambar)

**Observasi:**
* Pembagian train-test adalah sekitar 73% Train / 27% Test.
* Sub-folder numerik di dalam `Corrected` dan `Reversal` (label `1, 4, 5, 6, 7, 8, 9`) merepresentasikan *Severity Score* dari keparahan goresan, bukan identitas karakter yang ditulis.

## 3. Tipe Data & Konsistensi Format
* **Tipe File:** Konsistensi 100%. Seluruh 208.372 file berformat `.png`. Tidak ada file yang rusak (*corrupt*).
* **Resolusi:** Sangat seragam di **28x28** dan **29x29** piksel — identik dengan format MNIST/EMNIST.
* **Format Warna:** Grayscale (`L`) atau Binary (`1`). Tidak ada warna RGB.
* **Implikasi:** Setiap gambar adalah karakter tunggal yang terisolasi, bukan kata/kalimat.

## 4. Analisis Label & Kelas

### 4.1 Struktur Kelas Utama
| Kelas | Deskripsi |
|---|---|
| `Normal` | Tulisan tangan wajar, bebas dari ciri disleksia |
| `Corrected` | Penulis menimpa/mencoret goresan yang salah tanpa menghapus. Menghasilkan goresan tumpang tindih parah |
| `Reversal` | Penulis menulis karakter dengan arah terbalik (*mirror writing*) — gejala klasik disleksia |

### 4.2 Sistem Skoring Keparahan (Temuan 1 — Kunci)
Folder-folder numerik (`1, 4, 5, 6, 7, 8, 9`) di dalam `Corrected` dan `Reversal` merepresentasikan **derajat keparahan goresan (Severity Score)** — bukan identitas karakter. Setelah inspeksi visual dan normalisasi skala, sistem skor final setelah *preprocessing* adalah:

| Skor (Setelah Normalisasi) | Makna |
|---|---|
| **0** | Normal — Tidak ada gejala disleksia |
| **1** | Sangat Ringan — Goresan masih jelas terbaca |
| **2 - 5** | Menengah — Ada koreksi atau pembalikan yang semakin parah |
| **6** | Paling Parah — Goresan sangat hancur, hampir tidak terbaca manusia |

> [!IMPORTANT]
> Skala asli dari periset (1=Parah, 9=Ringan) bersifat **terbalik secara tidak intuitif**. Tim pengembang telah melakukan normalisasi menggunakan *Dictionary Mapping* sehingga skala menjadi linear: **0 = Sehat hingga 6 = Paling Parah**.

### 4.3 Kontaminasi Label / Label Noise (Temuan 2)
Ditemukan file bernama `NormalXXXX.png` yang terselip di dalam folder `Corrected` dan `Reversal`. Secara visual, konten gambar tersebut adalah goresan cacat — bukan tulisan normal. Ini adalah *Label Noise* yang dibuang sebelum training melalui *Logical Cleaning*.

### 4.4 Anomali Visual di Kelas Normal Asli (Temuan 3)
Melalui inspeksi visual manual, ditemukan bahwa sejumlah sampel di dalam kelas `Normal` menampilkan goresan koreksi atau pola yang menyerupai karakteristik `Corrected`. Hal ini mengindikasikan **kontaminasi label dua arah** pada dataset asli:
* File bergoresan cacat masuk ke folder Normal
* Sebagian file di folder Normal memiliki goresan yang seharusnya masuk kategori Corrected

> Temuan ini tercatat sebagai **risiko residual** dan menjadi dasar keputusan untuk menggunakan `master_dataset_dyslexia.csv` sebagai sumber kebenaran tunggal.

## 5. Penilaian Kualitas Data
* **Kejelasan Gambar:** Resolusi 28x28 membatasi detail halus goresan, namun cukup untuk membedakan pola kelas secara kasar.
* **Variasi:** Pencahayaan dan latar belakang telah dinormalisasi. Tidak ada variasi *background*.
* **Konteks Klinis:** Gambar karakter terisolasi kehilangan konteks makro disleksia (spasi, *baseline*, margin). Dataset ini cocok sebagai *proxy screening* tingkat huruf, bukan kata.
* **Kontaminasi Label (*Label Noise*):**
    * File `NormalXXXX.png` terselip di folder non-Normal → Dimitigasi via *Logical Cleaning*.
    * Anomali visual di kelas Normal asli → Tercatat sebagai risiko residual.

## 6. Risiko yang Berhasil Dimitigasi
| Risiko Awal | Status | Solusi |
|---|---|---|
| *Data Leakage* (model belajar karakter, bukan goresan) | ✅ Gugur | Folder 1-9 merupakan *Severity Score*, bukan karakter |
| *Label Noise* (`NormalXXXX.png` tersesat) | ✅ Dimitigasi | *Drop* via *Logical Cleaning* di Pandas CSV |
| Skala skor terbalik (1=Parah dekat ke 0=Sehat) | ✅ Dikoreksi | *Dictionary Mapping* normalisasi ke skala 0–6 |
| Anomali visual kelas Normal | ⚠️ Risiko Residual | Tercatat, CSV sebagai *ground truth* tunggal |
| *Class Imbalance* Train vs Test | ⚠️ Perlu Pantau | Gunakan argumen `class_weight` murni saat training CNN |

## 7. Keputusan Teknis Final (Actionable)

* **Preprocessing Fisik (Opsional):** Nama file diganti secara massal melalui script Python di `Dyslexia.ipynb` (Tahap 2). Tidak ada file yang dihapus, hanya diganti namanya agar skor konsisten (1–6).
* **Preprocessing Logis (Wajib):** Filter data kotor via `Dyslexia.ipynb` (Tahap 3) menghasilkan `master_dataset_dyslexia.csv`. Algoritma dirancang dengan *dual-path logic* untuk menangani dataset baik sebelum maupun sesudah *Physical Renaming*.
* **Augmentasi Fisik Dibatalkan:** Segala bentuk *Offline Augmentation* (rotasi, shear, zoom) dibatalkan untuk menghindari *overfitting* yang dipaksa dan *bloating* harddisk (dari 180.000 menjadi 300.000 file). Semuanya ditangani cukup via komputasi statistik `class_weight`.
* **Tidak Perlu Merombak Struktur Folder Fisik:** Struktur `Train/Test/Kelas` bawaan dataset sudah memadai karena file murni `master_dataset_final.csv` sebagai *filter master* akan mengatur segalanya.

## 8. Wawasan Strategis

* **Suitabilitas untuk Klasifikasi:** Dataset ini kini layak untuk tiga lapisan tugas klasifikasi sekaligus:
  1. *Binary*: Normal (0) vs. Disleksia (1)
  2. *Multi-class Severity*: Skor keparahan 0–6
  3. *Category*: Normal vs. Corrected vs. Reversal
* **Potensi Inovasi:** Output AI DyslexiaLens tidak hanya "Ya/Tidak", tetapi berupa skor derajat keparahan — menjadikannya sistem skrining klinis yang jauh lebih informatif dan premium.
* **Sequence Modeling:** Tidak direkomendasikan. Data berupa karakter terisolasi, bukan urutan tulisan. Fokus pada arsitektur CNN.
