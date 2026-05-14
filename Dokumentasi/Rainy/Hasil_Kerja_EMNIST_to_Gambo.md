# Ringkasan Lengkap Pipeline Dataset Gambo_hapusPutih_EMNIST

## Tujuan Utama

Mengintegrasikan:

* dataset EMNIST ByClass (huruf alfabet)
* dataset dyslexia internal (`Corrected`, `Reversal`)

ke dalam satu dataset final:

```text id="mk1fxy"
Dataset/Gambo_hapusPutih_EMNIST
```

dengan karakteristik:

* konsisten
* balanced
* aman dari data leakage
* filesystem-safe
* CNN-ready
* scalable
* reproducible
* production-friendly

---

# Perubahan Arsitektur Pipeline

## Pipeline Lama

Sebelumnya alur kerja menggunakan:

```text id="j4z11f"
EMNIST
→ TEMP folder
→ balancing
→ move ke dataset final
```

---

## Pipeline Baru

Diubah menjadi:

```text id="sxomuu"
EMNIST
→ langsung ke Gambo_hapusPutih_EMNIST
→ balancing langsung di dataset final
```

---

# Alasan Perubahan

Karena pipeline baru:

* lebih sederhana
* lebih stabil
* tidak perlu folder sementara
* mengurangi duplikasi file
* lebih mudah untuk incremental update
* lebih mudah maintenance

---

# Struktur Dataset Final

## Split Dataset

Dataset dibagi menjadi:

```text id="g4hvbq"
Train
Validation
Test
```

---

## Kategori Dataset

Setiap split memiliki:

```text id="1kkjzl"
Normal
Corrected
Reversal
```

---

# Struktur Folder Final

```text id="m26qyx"
Dataset/
└── Gambo_hapusPutih_EMNIST/
    ├── Train/
    │   ├── Normal/
    │   ├── Corrected/
    │   └── Reversal/
    │
    ├── Validation/
    │   ├── Normal/
    │   ├── Corrected/
    │   └── Reversal/
    │
    └── Test/
        ├── Normal/
        ├── Corrected/
        └── Reversal/
```

---

# Filtering Dataset EMNIST

Hanya alfabet yang digunakan:

```text id="2eh9hn"
A-Z
a-z
```

Digit:

```text id="cq1kto"
0-9
```

dibuang.

---

# Split Dataset

## Rasio Final

```text id="mn0dxn"
Train      = 70%
Validation = 15%
Test       = 15%
```

Split dilakukan:

* per karakter
* setelah shuffle deterministic
* menggunakan random seed tetap (`42`)

Tujuannya:

* reproducible
* mencegah data leakage
* distribusi karakter lebih stabil

---

# Perubahan Naming Convention

## Masalah Awal

Sebelumnya file Normal menggunakan:

```text id="g3l04u"
Train_Normal_A-3.png
Train_Normal_a-3.png
```

Masalah:
Windows filesystem bersifat:

```text id="yqgj01"
case-insensitive
```

Sehingga:

```text id="ssm8kl"
A == a
```

dan menyebabkan:

* collision
* overwrite
* file dianggap sama

---

# Solusi Final Naming

## Format Final untuk Normal

```text id="u10r8r"
Train_Normal_Upper_A_00470.png
Train_Normal_Lower_a_00017.png
```

---

# Struktur Naming Normal

```text id="5zkngh"
[Split]_[Class]_[Case]_[Character]_[Index].png
```

---

# Contoh

```text id="g9r9bp"
Validation_Normal_Upper_Z_00088.png
Test_Normal_Lower_b_00125.png
```

---

# Naming Dataset Dyslexia

## Corrected

```text id="5tb7ha"
Train_Corrected_1_00003.png
```

---

## Reversal

```text id="n8mjlwm"
Validation_Reversal_6_00001.png
```

---

# Struktur Naming Dyslexia

```text id="46h1az"
[Split]_[Class]_[Severity]_[Index].png
```

---

# Keuntungan Naming Baru

## 1. Aman di Semua OS

Karena:

```text id="akgqfa"
Upper_A
```

dan:

```text id="mqb8qf"
Lower_a
```

sekarang berbeda secara literal.

---

## 2. Sorting Natural

Menggunakan:

```text id="yn60h1"
zero padding
```

contoh:

```text id="fjlwmf"
00001
00002
00003
```

---

## 3. Regex-Friendly

Regex final untuk Normal:

```python id="5m2yvv"
r'^(Train|Validation|Test)_Normal_'
r'(Upper|Lower)_'
r'([A-Za-z])_'
r'(\d+)\.png$'
```

---

# Rename Migration

Seluruh file lama:

```text id="3x5z0r"
Train_Normal_A-3.png
```

dimigrasikan menjadi:

```text id="vjlwmx"
Train_Normal_Upper_A_00003.png
```

dan:

```text id="g6uj6x"
Train_Normal_a-17.png
```

menjadi:

```text id="vndepw"
Train_Normal_Lower_a_00017.png
```

---

# Extraction Pipeline Final

## Source

Menggunakan:

```text id="hcd7dc"
emnist-byclass-train.csv
```

---

## Mapping

Menggunakan:

```text id="qjlwm4"
emnist-byclass-mapping.txt
```

untuk mengubah:

```text id="j99s2y"
label → karakter ASCII
```

---

# Orientation Fix

Karena EMNIST menggunakan:

```text id="o63jlwm"
column-major storage
```

maka gambar wajib:

```python id="qjlwm6"
img = img.T
```

agar orientasi karakter benar.

---

# Ukuran Gambar

## Final Size

Dataset tetap disimpan dalam:

```text id="mjlwm5"
28x28 grayscale
```

---

# Alasan Tetap Menggunakan 28x28

Awalnya sempat dipertimbangkan:

```text id="kj0uh0"
224x224
```

namun hasil visual kurang baik karena:

* hanya interpolasi
* detail asli tidak bertambah
* stroke menjadi blur

---

# Keputusan Final

Dataset disimpan dalam:

```text id="7cpx7v"
28x28 original canonical form
```

agar:

* tetap sesuai sumber asli EMNIST
* tidak destructive
* reproducible
* future-proof

---

# Rencana Selanjutnya

Upscaling dan enhancement akan dilakukan:

```text id="jlwmm7"
setelah dataset final selesai
```

oleh pipeline terpisah.

Tujuannya:

* meningkatkan kualitas visual
* super-resolution
* enhancement untuk CNN

tanpa merusak dataset source utama.

---

# Incremental Indexing

## Problem

Dataset existing sudah memiliki:

```text id="gjlwm8"
Upper_A_00470
```

maka extraction baru harus:

```text id="jlwmh9"
melanjutkan index
```

bukan reset ulang.

---

# Solusi

Sebelum extraction:

* scan seluruh folder
* baca filename existing
* cari index terbesar per karakter

---

# Tracking Key Final

Tracking menggunakan:

```python id="jlwmk0"
Upper_A
Lower_a
```

contoh:

```python id="jlwmn1"
{
    'Upper_A': 470,
    'Lower_a': 17
}
```

---

# Hasil

Extraction baru otomatis menjadi:

```text id="jlwmp2"
Train_Normal_Upper_A_00471.png
Train_Normal_Upper_A_00472.png
```

tanpa collision.

---

# Balancing Dataset

## Tujuan

Menyeimbangkan:

```text id="jlwmq3"
Normal vs Dyslexia
```

---

# Strategi Balancing

Balancing dilakukan:

* langsung di dataset final
* per split
* character-aware

---

# Proses Balancing

## 1. Hitung jumlah:

```text id="jlwmr4"
Normal
Corrected
Reversal
```

---

## 2. Hitung Excess

```python id="jlwms5"
to_remove = total_normal - total_dyslexia
```

---

## 3. Group per Character

contoh:

```text id="jlwmt6"
Upper_A
Lower_a
Upper_B
```

---

## 4. Binary Search Character Cap

Tujuan:

* menjaga distribusi karakter
* mencegah dominasi huruf tertentu

---

## 5. Hapus Excess

File dengan:

```text id="jlwmu7"
index terbesar
```

dihapus lebih dahulu.

---

# Status Final Dataset

## Sudah Selesai

```text id="jlwmv8"
✔ Rename migration
✔ Case-safe naming
✔ Extraction pipeline
✔ Incremental indexing
✔ Train/Validation/Test split
✔ EMNIST integration
✔ Balancing
✔ Windows-safe filenames
✔ Character-aware balancing
✔ Reproducible random seed
✔ Canonical 28x28 preservation
```

---

# Hasil Akhir

Dataset:

```text id="jlwmw9"
Gambo_hapusPutih_EMNIST
```

sekarang:

* balanced
* konsisten
* uppercase/lowercase aman
* regex-friendly
* CNN-ready
* scalable
* reproducible
* production-safe
* siap untuk tahap enhancement/upscaling berikutnya

---