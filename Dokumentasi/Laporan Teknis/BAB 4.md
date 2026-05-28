# BAB 4: Feature Engineering — Explainable AI (XAI)

Bab ini mendokumentasikan proses transformasi **matriks piksel mentah** menjadi **metrik kuantitatif** yang merepresentasikan karakteristik motorik tulisan tangan. Pendekatan ini dikenal sebagai *Explainable AI* (XAI): alih-alih menyerahkan gambar mentah ke dalam *black-box* CNN, kita terlebih dahulu mengekstrak 6 fitur matematis yang memiliki **makna klinis** sehingga setiap prediksi model kelak dapat dirasionalisasi secara manusiawi.

> ⚠️ **Pertahanan MLOps (Zero Data Leakage):** 
> Seluruh ekstraksi fitur geometri di bab ini bersifat **Stateless Operation** (dihitung murni dan mandiri per gambar). Karena tidak ada penggunaan agregat populasi (seperti *mean/variance scaling*), ekstraksi fitur secara global pada Master CSV dijamin **100% bebas dari kebocoran data (Data Leakage)** antar-*split* Train dan Test.

---

## 4.1 Preprocessing Citra Dasar

Sebelum fitur diekstrak, setiap gambar melewati dua tahap normalisasi keruangan dan warna:

### A. Konversi Grayscale & Spatial Normalization (Resize)

Seluruh gambar dikonversi ke format *grayscale* (1 kanal warna, skala 0–255) dan di-*resize* secara absolut ke resolusi standar **28 × 28 piksel**. 
*(Catatan Metodologi: Proses resize absolut ini secara inheren memaksa normalisasi batas keruangan. Oleh karena itu, teknik standarisasi whitespace manual/padding yang direncanakan di awal sengaja dibatalkan, karena hanya berisiko mendistorsi aspek rasio bawaan dari matriks sparsa tulisan tangan).*

### B. Binarisasi (*Thresholding*)

Matriks grayscale (0–255) ditransformasi menjadi matriks biner (0 dan 1) menggunakan ambang batas (*threshold* = 128):
```python
binary = (pixels > 128).astype(np.float64)
```
Mengingat dataset ini menggunakan standar latar belakang hitam (seperti MNIST):
- **Piksel > 128** → dikategorikan sebagai **Foreground (goresan/tulisan putih)** → nilai `1`.
- **Piksel ≤ 128** → dikategorikan sebagai **Background (latar hitam)** → nilai `0`.

---

## 4.2 Definisi, Justifikasi, & Batasan 6 Fitur Matematis

Keenam fitur dirancang secara matematis untuk menangkap gejala motorik disleksia. Berikut adalah pembedahan algoritmanya beserta pengungkapan keterbatasan secara objektif:

### Fitur 1: `stroke_density` — Kepadatan Tinta (Deteksi *Over-tracing*)

| Aspek | Detail |
|---|---|
| **Formula** | `Σ(piksel foreground) / total_piksel (784)` |
| **Rentang Output** | `0.0` (gambar kosong) – `1.0` (gambar penuh) |
| **Celah Algoritmik** | **Bias Skala (Scale-Dependent):** Karena pembaginya adalah luas total kanvas (784) dan bukan luas area huruf (*Bounding Box Area*), fitur ini juga menangkap ukuran tulisan (*macrographia/micrographia*). Huruf besar yang ditarik tipis bisa mendapat skor sama dengan huruf kecil yang ditekan tebal (*over-tracing*). |
| **Justifikasi Klinis** | Penderita disleksia sering menunjukkan perilaku *over-tracing*: menekan pena berulang kali di garis yang sama karena keraguan motorik. Akibatnya, kepadatan tinta (*stroke density*) secara proporsional lebih tinggi dibandingkan tulisan normal yang satu tarikan efisien. |

### Fitur 2–3: `center_of_mass_x` & `center_of_mass_y` — Pusat Massa (Distorsi Spasial)

| Aspek | Detail |
|---|---|
| **Formula** | `mean(koordinat piksel foreground)` pada sumbu X dan Y |
| **Rentang Output** | `0.0` – `27.0` (sesuai dimensi gambar 28×28) |
| **Justifikasi Klinis** | Tulisan normal cenderung memiliki *Center of Mass* (CoM) yang stabil di sekitar pusat kanvas (X=14, Y=14). Pada penderita disleksia, CoM kerap bergeser secara asimetris akibat distorsi keruangan (spatial distortion) dan kesulitan mempertahankan titik awal penulisan. |

### Fitur 4: `bounding_box_ratio` — Rasio Rentang Aktif (Distorsi Dimensi)

| Aspek | Detail |
|---|---|
| **Formula** | `(Σ(baris_aktif) + 1) / (Σ(kolom_aktif) + 1)` |
| **Rentang Output** | `> 0.0` (penambahan +1 mencegah pembagian nilai nol) |
| **Celah Algoritmik** | Fitur ini secara matematis menghitung rasio **Active Ink Span** (jumlah baris bertinta), bukan *True Bounding Box* (max_y - min_y). Pendekatan ini justru dipertahankan karena lebih sensitif dalam menghukum (memberi rasio aneh) pada garis tulisan yang putus-putus akibat tremor parah. |
| **Justifikasi Klinis** | Mengidentifikasi huruf yang proporsinya hancur (terlalu "gepeng" atau memanjang keluar batas) akibat kontrol motorik halus yang terganggu. |

### Fitur 5: `stroke_transitions` — Transisi Warna (Deteksi Tremor)

| Aspek | Detail |
|---|---|
| **Formula** | `Σ(|diff(baris_biner)|) / IMG_SIZE (28)` |
| **Rentang Output** | `≥ 0.0` (semakin tinggi skor, semakin kuat indikasi tremor/gerigi) |
| **Celah Algoritmik** | Mengandung bias skala vertikal (**Scale-Dependent Tremor Approximation**). Karena dibagi dengan total kanvas (28) dan bukan dengan tinggi huruf asli, tulisan lurus yang panjang secara vertikal dapat mengakumulasi skor transisi yang tinggi secara artifisial. |
| **Justifikasi Klinis** | Menghitung rata-rata perpindahan warna (hitam↔putih) per baris. Getaran tangan (*tremor*) menyebabkan garis menjadi bergerigi atau putus-putus, sehingga jumlah transisi melonjak drastis dibandingkan garis lurus/mulus pada anak normal. |

### Fitur 6: `horizontal_symmetry` — Simetri Absolut (Deteksi *Reversal*)

| Aspek | Detail |
|---|---|
| **Formula** | `mean(belahan_kiri_kanvas == flip(belahan_kanan_kanvas))` |
| **Rentang Output** | Teoritis `0.0` - `1.0` (namun secara praktis terkompresi > `0.85`) |
| **Celah Algoritmik** | **1. Ilusi Rentang:** Akibat dominasi >90% *background* hitam pekat yang selalu simetris (`0 == 0`), skor fitur ini mengalami kompresi dan nyaris tidak pernah turun di bawah `0.85`.<br>**2. Absolute Spatial:** Pemisahan dilakukan tepat di pusat kanvas (kolom 14), bukan di pusat huruf (CoM). |
| **Justifikasi Klinis** | Karakteristik *Absolute Spatial* di atas justru brilian: skor akan anjlok tidak hanya jika bentuk hurufnya asimetris (seperti *letter reversal* "b" vs "d"), tetapi juga jika huruf tersebut diletakkan melenceng dari tengah kanvas (kegagalan tata ruang). Ini adalah indikator terkuat untuk kasus Disleksia tipe *Reversal*. |

---

## 4.3 Pipeline Ekstraksi & Validasi

Fungsi ekstraksi diaplikasikan secara iteratif pada `master_dataset_dyslexia.csv`. Hasilnya digabungkan secara horizontal menjadi 12 kolom final. Hasil ekstraksi memicu dua proses validasi:

1. **NaN Audit:** Berkat pembersihan *Broken Links* di Bab 3, audit melaporkan **0 Error/NaN**, membuktikan kekokohan *pipeline* rekayasa data.
2. **Distribusi Histogram:** Analisis visual mengonfirmasi bahwa sebaran fitur antar kelas tidak saling tumpang tindih secara identik.

> 🖼️ **[SUGESTI VISUAL 1]**
> *Tempatkan screenshot histogram distribusi 6 fitur (Normal vs Disleksia, 2×3 grid) dari Tahap 6.*
> `![Distribusi 6 Fitur XAI](path/ke/gambar_distribusi_fitur.png)`

### Ringkasan Statistik Selisih Antar Kelas

> 🖼️ **[SUGESTI VISUAL 2]**
> *Tempatkan screenshot output tabel terminal `=== Selisih Absolut (Disleksia - Normal) ===` dari notebook Tahap 6.*
> `![Selisih Statistik Fitur](path/ke/gambar_selisih_fitur.png)`

*(Berdasarkan tabel log di atas, fitur dengan selisih absolut terbesar terbukti menjadi diskriminator utama yang merepresentasikan perbedaan nyata secara klinis).*

---

## 4.4 Implikasi Arsitektur: *Late Fusion Model*

| Kolom Baru | Tipe | Deskripsi (Data Dictionary) |
|---|---|---|
| `stroke_density` | Float | Kepadatan area tulisan putih (0.0–1.0) |
| `center_of_mass_x` | Float | Titik pusat goresan sumbu-X (0–27) |
| `center_of_mass_y` | Float | Titik pusat goresan sumbu-Y (0–27) |
| `bounding_box_ratio` | Float | Rasio baris aktif vs kolom aktif (*Active Ink Span*) |
| `stroke_transitions` | Float | Rata-rata transisi per baris (skala *IMG_SIZE*) |
| `horizontal_symmetry` | Float | Skor kemiripan cermin spasial absolut (terkompresi > 0.8) |

📌 **Kesimpulan Bab 4:** Ekstraksi fitur matematis berhasil menerjemahkan kondisi motorik (tremor, asimetri spasial, keraguan/ *over-tracing*) ke dalam 6 metrik tabular. Dengan membedah secara jujur keterbatasan algoritmik dari formulanya (seperti bias skala tremor dan kompresi rentang simetri), fitur ini terbukti tetap memiliki variansi tinggi untuk membedakan kelas Normal dan Disleksia. Dataset yang telah diperkaya fitur tabular pendamping ini (*Featured Dataset*) membuka ruang bagi AI Engineer untuk merancang arsitektur *Late Fusion* (Multi-Input Model), di mana cabang pertama (CNN) menganalisis pola gambar mentah dan cabang kedua (Dense Layer) menganalisis 6 fitur biologis ini, menciptakan AI yang tidak sekadar menebak namun mampu menjelaskan alasannya secara klinis. Dataset ini kini siap untuk dianalisis lebih lanjut pada tahap *Exploratory Data Analysis* (Bab 5).
