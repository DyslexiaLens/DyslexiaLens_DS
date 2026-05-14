# Checkpoint 8 — Integrasi EMNIST, Arsitektur Shape-Agnostic, dan Migrasi Pipeline
**Tanggal:** 14 Mei 2026  
**Role:** Data Scientist  
**Status Notebook:** `EMNIST_to_Gambo.ipynb` (Penyatuan Dataset & Pemisahan Arsitektur)

---

## 🎯 Ringkasan Eksekutif Sesi
Melanjutkan keberhasilan sterilisasi dataset pada Checkpoint 7 (*Dataset Integrity Hardening*), sesi ini berfokus pada tahap krusial selanjutnya: **Integrasi Eksternal dan Desain Arsitektur Bebas Bias**. 

Kami sukses menggabungkan dataset EMNIST (Normal) dengan dataset Gambo (Disleksia) melalui *pipeline* baru yang lebih kokoh. Lebih jauh lagi, sesi ini melahirkan keputusan arsitektural berskala besar (*Plan A: Shape-Agnostic Approach*) yang memisahkan fitur translasi OCR dari fitur diagnosa klinis. Kombinasi dari standarisasi penamaan file yang aman (*filesystem-safe*) dan penyusunan dataset yang terkalibrasi membuat fondasi proyek ini resmi berstatus *Production-Ready*.

---

## 🚨 Pencapaian & Resolusi Sesi Ini

### 1. Perombakan Pipeline & Integrasi EMNIST Langsung
**(Referensi: `Hasil_Kerja_EMNIST_to_Gambo.md`)**
**Konteks:** *Pipeline* lama yang menggunakan folder `TEMP` sebelum pemindahan file dinilai berbelit-belit, rentan duplikasi, dan sulit untuk di-*maintenance*.
**Tindakan Resolusi:** 
- Alur kerja dirombak total: EMNIST diekstrak, diproses, dan langsung dimasukkan ke struktur *final split* (`Train/Validation/Test`).
- Melakukan *Stratified Balancing* secara langsung di direktori final. Jumlah EMNIST dibatasi dan dibagi rata untuk setiap huruf agar setara (50:50) dengan kelas *Dyslexia* di dataset Gambo.
- **Hasil:** Proses penggabungan menjadi jauh lebih sederhana, *scalable*, dan aman dari risiko *class imbalance*.

### 2. Resolusi Naming Convention & Windows Filesystem Safety
**(Referensi: `Hasil_Kerja_EMNIST_to_Gambo.md`)**
**Konteks:** Sistem penamaan lama seperti `Train_Normal_A-3.png` dan `Train_Normal_a-3.png` memicu tabrakan (*collision*) pada Windows yang bersifat *case-insensitive* (tidak bisa membedakan A besar dan a kecil pada nama file).
**Tindakan Resolusi:** 
- Menerapkan format penamaan literal: `[Split]_[Class]_[Case]_[Character]_[Index].png`. 
- Contoh: `Train_Normal_Upper_A_00470.png` dan `Train_Normal_Lower_a_00017.png`.
- **Hasil:** Dataset kini 100% aman lintas sistem operasi, terhindar dari tumpang tindih data (*overwrite*), dan menggunakan penomoran *zero-padding* yang berurutan natural (*regex-friendly*).

### 3. Penetapan Arsitektur *Shape-Agnostic* (Plan A)
**(Referensi: `01_Strategi_Fitur_dan_Arsitektur.md`)**
**Konteks:** Terdapat risiko *Shape Bias* (kebocoran data) jika CNN dilatih untuk menebak disleksia berdasarkan bentuk abjad, mengingat kelas *Reversal* di Gambo hanya memuat huruf kecil spesifik (`b`, `d`, `p`, `q`).
**Tindakan Resolusi:** 
- **Mempertahankan `b, d, p, q`:** Menjaga sampel ini di dataset Gambo karena merupakan "Golden Feature" medis dari *reversal error*.
- **Membuang Augmentasi Ber-Artefak:** Menghapus ~3.000 gambar bernoise blok putih di pojok agar tidak merusak fitur turunan matematis dan mencegah *shortcut learning*.
- **Pemisahan Jalur:**
    - **Translasi OCR:** Menggunakan model visi murni dengan asupan seluruh abjad EMNIST (A-Z, a-z) untuk membaca tulisan.
    - **Diagnosa Klinis (Late Fusion):** Menggabungkan kekuatan CNN (untuk ekstraksi pola spasial 28x28) dengan model Tabular yang memproses **5 Fitur Turunan Matematis** (`ink_density`, `center_of_mass`, `bounding_box`, `stroke_transitions`). Vektor dari kedua cabang ini digabungkan (*concatenation*) sebelum masuk ke layer klasifikasi akhir.
- **Hasil:** Diagnosa disleksia kini kebal terhadap bias bentuk abjad. Keberadaan 5 fitur matematis bertindak sebagai *strong regularization* yang memaksa CNN untuk tidak sekadar menghafal huruf, melainkan wajib mengevaluasi "kualitas motorik" tarikan garis.

### 4. Preservasi Kanonikal 28x28 (Anti-Distorsi)
**(Referensi: `Hasil_Kerja_EMNIST_to_Gambo.md`)**
**Konteks:** Muncul gagasan untuk langsung membesarkan gambar (*upscaling*) ke 224x224 untuk CNN modern.
**Tindakan Resolusi:** 
- Ide tersebut dibatalkan. *Upscaling* sederhana hanya akan melakukan interpolasi (*blurring*) dan merusak integritas *stroke* asli.
- Dataset final ditetapkan secara kanonikal di **28x28 grayscale**. *Enhancement/Upscaling* canggih jika diperlukan akan diserahkan pada *pipeline* terpisah milik tim AI di masa depan.

---

## 🧠 Evolusi Filosofi Proyek
Sesi ini menyadarkan kami bahwa *Data Engineering* bukan cuma soal merapikan tabel atau folder, melainkan memikirkan dampak UX (*User Experience*) dan implikasi klinis. Keputusan untuk menggabungkan *semua* variasi A-Z dan a-z EMNIST demi keleluasaan tes di kertas grid kosong, dibarengi dengan pendekatan *Shape-Agnostic* untuk diagnosanya, menunjukkan kedewasaan desain sistem yang memikirkan skenario dunia nyata ( *real-world application* ).

---

## 🚀 Dampak Strategis & Kesimpulan Perjalanan
Dengan selesainya Checkpoint 8, status proyek adalah sebagai berikut:
- Dataset `Gambo_hapusPutih_EMNIST` kini terstruktur sempurna: stabil, konsisten, seimbang (*balanced*), *case-safe*, dan siap dilempar ke CNN maupun ekstraksi tabular.
- *Masterplan* arsitektur (Plan A) telah dikunci, memastikan kolaborasi tim AI dan Full-Stack memiliki panduan yang jelas antara alur Translasi vs Diagnosa.

Fase *Data Wrangling* & *Engineering* dari sudut pandang *Data Scientist* telah mencapai bentuk akhir yang ideal dan elegan!
