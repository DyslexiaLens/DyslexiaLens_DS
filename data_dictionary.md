# 📖 Data Dictionary — DysRead Helper

## Deskripsi Proyek

**DysRead Helper** adalah sistem early screening disleksia pada anak berbasis analisis citra tulisan tangan menggunakan pendekatan Vision-based (CNN). Sistem ini mendeteksi **pola kognitif visual** pada tulisan tangan, bukan membaca teks (OCR).

---

## 1. Raw Data (Input)

### 1.1 Gambar Tulisan Tangan

| Field | Deskripsi |
|-------|-----------|
| **Sumber** | Dyslexia Handwriting Dataset (Kaggle) — Dr. Iza Sazanita Isa |
| **Format** | PNG / JPG, grayscale |
| **Resolusi** | Bervariasi (tipikal 28×28 hingga 128×128 px) |
| **Konten** | Gambar huruf individu (A-Z, a-z) |

### 1.2 Kelas Original (3 Kelas)

| Kelas | Deskripsi | Jumlah Est. | Contoh |
|-------|-----------|-------------|--------|
| `Normal` | Huruf ditulis dengan orientasi benar dan proporsional | ~78,275 | Huruf "b" ditulis normal |
| `Reversal` | Huruf ditulis terbalik/mirror — ciri khas disleksia | ~52,196 | Huruf "b" ditulis seperti "d" |
| `Corrected` | Huruf yang awalnya salah, lalu dicoba diperbaiki oleh anak | ~8,029 | Coret-coretan koreksi terlihat |

### 1.3 Mapping ke Binary Label

| Original | Binary Label | Kode Numerik | Rasionale |
|----------|-------------|--------------|-----------|
| `Normal` | `non_dyslexic` | `0` | Tulisan tanpa indikasi disleksia |
| `Reversal` | `dyslexic` | `1` | Pembalikan huruf = gejala utama disleksia |
| `Corrected` | `dyslexic` | `1` | Adanya koreksi menunjukkan kesulitan menulis |

---

## 2. Processed Data (Output Preprocessing)

### 2.1 CNN Tensor

| Field | Spesifikasi |
|-------|-------------|
| **Format file** | NumPy array (`.npy`) |
| **Shape** | `(128, 128, 1)` — Height × Width × Channel |
| **Dtype** | `float32` |
| **Range pixel** | `[0.0, 1.0]` (normalized dari 0-255) |
| **Background** | `0.0` (hitam) |
| **Foreground** | Nilai > 0 (goresan tulisan, putih = 1.0) |
| **Padding** | Center padding hitam untuk preservasi aspek rasio |

### 2.2 Data Split

| Split | Proporsi | Strategi | Seed |
|-------|----------|----------|------|
| `train` | 70% | Stratified random | 42 |
| `val` | 15% | Stratified random | 42 |
| `test` | 15% | Stratified random | 42 |

---

## 3. Extracted Features (Output Feature Engineering)

### 3.1 Kategori A — Character-Level Features

| # | Nama Fitur | Tipe | Range | Satuan | Deskripsi |
|---|-----------|------|-------|--------|-----------|
| 1 | `char_count` | int | 0–∞ | count | Jumlah karakter yang berhasil disegmentasi dari gambar |
| 2 | `char_aspect_ratio_mean` | float | 0–∞ | ratio | Rata-rata rasio lebar/tinggi semua karakter |
| 3 | `char_aspect_ratio_var` | float | 0–∞ | ratio² | **Variance** rasio aspek — tinggi = ukuran huruf tidak konsisten |
| 4 | `char_rotation_mean` | float | 0–180 | derajat | Rata-rata sudut rotasi huruf (dari fitEllipse) |
| 5 | `char_rotation_std` | float | 0–∞ | derajat | **Std deviasi** rotasi — tinggi = huruf miring tidak konsisten |
| 6 | `stroke_width_mean` | float | 0–∞ | pixel | Rata-rata ketebalan goresan (dari distance transform) |
| 7 | `stroke_width_std` | float | 0–∞ | pixel | Std deviasi ketebalan goresan |
| 8 | `stroke_width_cv` | float | 0–∞ | - | **Coefficient of Variation** ketebalan — tinggi = tekanan pena tidak stabil |
| 9 | `skeleton_endpoints` | int | 0–∞ | count | Jumlah titik ujung pada skeleton huruf |
| 10 | `skeleton_junctions` | int | 0–∞ | count | Jumlah percabangan pada skeleton huruf |

### 3.2 Kategori B — Word/Line-Level Features

| # | Nama Fitur | Tipe | Range | Satuan | Deskripsi |
|---|-----------|------|-------|--------|-----------|
| 11 | `inter_char_spacing_mean` | float | -∞–∞ | pixel | Rata-rata jarak antar karakter (negatif = overlap) |
| 12 | `inter_char_spacing_cv` | float | 0–∞ | - | **CV spasi** — tinggi = spacing sangat tidak konsisten |
| 13 | `baseline_rmse` | float | 0–∞ | pixel | **RMSE deviasi baseline** — tinggi = huruf melompat dari garis |
| 14 | `baseline_slope` | float | -90–90 | derajat | Kemiringan garis baseline (0 = horizontal sempurna) |
| 15 | `slant_angle_mean` | float | -45–45 | derajat | Rata-rata sudut kemiringan huruf |
| 16 | `slant_angle_std` | float | 0–∞ | derajat | **Std kemiringan** — tinggi = slant tidak konsisten |

### 3.3 Kategori C — Page-Level Features

| # | Nama Fitur | Tipe | Range | Satuan | Deskripsi |
|---|-----------|------|-------|--------|-----------|
| 17 | `line_straightness` | float | 0–1 | score | Skor kelurusan baris (1 = sangat lurus, 0 = berliku) |
| 18 | `density_uniformity` | float | 0–1 | score | Uniformitas kepadatan tulisan per region grid |
| 19 | `ink_ratio` | float | 0–1 | ratio | Proporsi pixel foreground (tinta) terhadap total pixel |
| 20 | `ink_ratio_cv` | float | 0–∞ | - | CV rasio tinta per baris — tinggi = kepadatan fluktuatif |
| 21 | `contour_area_cv` | float | 0–∞ | - | CV luas kontour karakter — tinggi = ukuran huruf bervariasi |

---

## 4. Label/Target Variable

| Field | Deskripsi |
|-------|-----------|
| **Nama** | `label` |
| **Tipe** | Binary integer |
| **Values** | `0` = non_dyslexic, `1` = dyslexic |
| **Distribusi** | Imbalanced (~56% Normal, ~38% Reversal, ~6% Corrected) |
| **Catatan** | Label TIDAK dimasukkan ke dalam fitur training (no data leakage). Split dilakukan SEBELUM augmentation. |

---

## 5. Augmented Data

| Field | Deskripsi |
|-------|-----------|
| **Sumber** | Hasil augmentasi dari data training saja (val/test TIDAK di-augment) |
| **Label** | Sama dengan gambar asli (augmentasi label-safe) |
| **Teknik Non-Dyslexic** | Rotation ±5°, brightness ±15%, Gaussian noise, mild elastic |
| **Teknik Dyslexic** | Semua di atas + BaselineWave, strong elastic, spacing perturbation |
| **DILARANG** | Horizontal flip pada kelas Normal (mengubah label!) |

---

## 6. Metadata Files

| File | Konten |
|------|--------|
| `data_card.md` | Ringkasan dataset: sumber, lisensi, limitasi, etika |
| `data_dictionary.md` | Dokumen ini — deskripsi setiap kolom dan fitur |
| `configs/preprocessing_config.yaml` | Parameter preprocessing yang digunakan |
| `metadata/data_manifest.csv` | (Dibuat saat runtime) Log file yang berhasil/gagal diproses |
