# BAB 8: Kesimpulan & *Action Items* (Handover)

Bab ini merupakan penutup resmi dari seluruh rangkaian *pipeline* Data Science untuk proyek **DyslexiaLens**. Tujuannya ada dua: (1) menjawab secara definitif keempat **Pertanyaan Bisnis** yang didefinisikan di Bab 1, dan (2) mendokumentasikan **mandat teknis (*Action Items*)** yang mengikat secara operasional bagi tim AI Engineer sebagai penerima estafet dataset.

---

## 8.1 Jawaban Pertanyaan Bisnis

Berikut adalah jawaban final atas keempat pertanyaan analitis yang menjadi fondasi seluruh eksperimen dalam laporan ini:

### Pertanyaan 1: *"Apakah dataset asli (Gambo) sudah cukup representatif dan seimbang untuk melatih model AI?"*

**❌ TIDAK.** Dataset Gambo mentah menderita tiga cacat fundamental:
- **Class Imbalance 3.35:1** — Kelas disleksia mendominasi populasi secara masif terhadap kelas Normal (Bab 2 & 5).
- **Label Noise dua arah** — File Normal tersesat di folder Disleksia, dan sebaliknya (Bab 2).
- **Severity Score terbalik dan berlubang** — Skala keparahan periset asli menggunakan konvensi `9 = Ringan`, `1 = Parah`, dengan angka 2 dan 3 hilang total (Bab 2).

**Resolusi:** Seluruh anomali telah diintervensi melalui *Logical Cleaning* berlapis (Bab 3) dan augmentasi EMNIST yang tervalidasi secara statistik (Bab 6), menghasilkan dataset final dengan rasio kelas **1:1** yang seimbang. 
*(Catatan: Keseimbangan 1:1 ini hanya berlaku untuk kelas Biner Sehat vs Sakit. Distribusi internal `severity_score` tetap dibiarkan timpang secara alami untuk merepresentasikan distribusi klinis yang otentik di dunia nyata).*

### Pertanyaan 2: *"Apakah pola visual dalam tulisan tangan cukup kuat untuk merepresentasikan kondisi kognitif disleksia?"*

**✅ YA, SANGAT KUAT.** Tiga bukti empiris mendukung kesimpulan ini:
1. **Variance Heatmap (Bab 5):** Populasi disleksia menunjukkan *Inkonsistensi Spasial* yang sangat nyata — area variansi piksel menyebar luas dan tidak beraturan, berbanding terbalik dengan pola terpusat milik anak Normal.
2. **KDE Plot Sub-tipe (Bab 5):** Setiap sub-tipe disleksia memiliki "sidik jari" numerik yang unik — Corrected terdeteksi melalui *Stroke Density* ekstrem, Reversal melalui anomali *Horizontal Symmetry*.
3. **A/B Testing (Bab 6):** Cohen's d membuktikan bahwa 6 fitur XAI konsisten menangkap perbedaan pola klinis bahkan setelah injeksi data EMNIST (Effect Size = Negligible, artinya sinyal asli tidak terdistorsi).

### Pertanyaan 3: *"Bagaimana cara mengekstrak metrik visual agar AI tidak menjadi black-box?"*

**✅ MELALUI 6 FITUR XAI MATEMATIS (Bab 4).** Keenam fitur diekstrak secara *stateless* (per gambar, tanpa kebocoran antar-split) dan memiliki makna klinis yang dapat dirasionalisasi:

| Fitur | Gejala Klinis yang Ditangkap |
|---|---|
| `stroke_density` | *Over-tracing* (keraguan menulis) |
| `center_of_mass_x` | Distorsi spasial horizontal (posisi tulisan melenceng ke kiri/kanan) |
| `center_of_mass_y` | Distorsi spasial vertikal (posisi tulisan melenceng ke atas/bawah) |
| `bounding_box_ratio` | Inkonsistensi proporsi huruf akibat kontrol spasial yang lemah |
| `stroke_transitions` | Getaran tangan (*tremor*) berupa garis bergerigi |
| `horizontal_symmetry` | *Letter reversal* (huruf terbalik, misal: b ↔ d) |

Fitur-fitur ini memungkinkan AI Engineer merancang arsitektur **Late Fusion** di mana model tidak sekadar menebak, tetapi mampu mencetak alasan klinis di balik setiap prediksinya.

### Pertanyaan 4: *"Bagaimana merekonstruksi Severity Score yang anomali agar layak menjadi target prediksi?"*

**✅ DISELESAIKAN DI BAB 3.** Fungsi `get_score()` berhasil:
1. **Membalik skala** dari konvensi periset asli (9 = Ringan) menjadi konvensi AI standar (1 = Ringan, 6 = Parah, 0 = Normal).
2. **Memampatkan lubang & Menggabungkan Puncak** — Angka 2 dan 3 yang hilang berhasil terisi melalui pergeseran indeks, sementara 2 skor ekstrem di dataset asli (skor 4 untuk Corrected terparah dan skor 1 untuk Reversal) secara logis digabungkan menjadi satu puncak keparahan absolut (skor 6).
3. **Mengeliminasi Label Noise** — File Normal di folder Disleksia dan sebaliknya dieksekusi secara algoritmik (`return 'DROP'`).

Hasilnya: kolom `severity_score` (0–6) kini bersifat **Kategorikal Ordinal** yang bersih dan siap dijadikan target Multi-Class Classification.

---

## 8.2 Rangkuman Perjalanan Pipeline

| Tahap | Bab | Input | Output | Transformasi Kunci |
|---|---|---|---|---|
| **Audit** | 2 | Dataset Gambo mentah (208.372 gambar) | Laporan 4 anomali kritis | Deteksi Label Noise, Inverted Score, Imbalance |
| **Cleaning** | 3 | 208.372 gambar + anomali | ~156.453 gambar bersih + Master CSV | 8 filter logika, rekonstruksi `severity_score` |
| **Feature Eng.** | 4 | Master CSV + gambar bersih | CSV + 6 kolom fitur XAI | Ekstraksi *stateless* per gambar |
| **EDA** | 5 | Featured CSV | Jawaban 4 Pertanyaan Bisnis + Dashboard | Variance Heatmap, KDE Plot, Boxplot |
| **Augmentasi** | 6 | Gambo (156k) + EMNIST | Dataset Balanced 1:1 (~204.833) | Injeksi Normal & *Fair Pruning* Disleksia, validasi A/B |
| **Preparation** | 7 | Dataset Balanced | Train/Val/Test (70/15/15) + Data Dictionary | Stratified Split, Class Weights |

---

## 8.3 *Action Items* — Mandat Teknis untuk AI Engineer

Bagian ini bersifat **kontraktual**. Seluruh instruksi di bawah ini wajib dipatuhi oleh tim AI Engineer demi menjaga integritas saintifik dari dataset yang telah dibangun.

### A. Instruksi Wajib (*MUST*)

| # | Mandat | Alasan | Referensi |
|---|---|---|---|
| 1 | Gunakan `master_dataset_final_balanced_rill_featured.csv` sebagai **satu-satunya sumber kebenaran** | Mengandalkan struktur folder fisik akan menyebabkan *Data Poisoning* akibat *Label Noise* bawaan | Bab 2 & 3 |
| 2 | Masukkan `binary_weight_dict` ke parameter `class_weight` pada `model.fit()` | Meskipun rasio global sudah 1:1, distribusi internal `severity_score` tetap timpang | Bab 7.1.D |
| 3 | Aplikasikan **StandardScaler/MinMaxScaler** pada 6 fitur XAI sebelum *concat* ke Dense Layer | Fitur masih bersifat `[RAW]` dengan rentang berbeda; tanpa scaling, fitur berskala besar akan mendominasi bobot neuron | Bab 7.2 |
| 4 | Fokuskan metrik evaluasi pada **F1-Score dan Recall**, bukan Accuracy | Pada dataset medis, *False Negative* (gagal deteksi anak disleksia) jauh lebih berbahaya daripada *False Positive* | Prinsip *Medical AI* |
| 5 | Taklukkan **Klasifikasi Biner** (`target_class`: 0 vs 1) terlebih dahulu | Model *Multi-Class* (`severity_score`) rentan *Gradient Instability* akibat ketimpangan 1:50 pada kelas minoritas | Bab 7.1.D |

### B. Larangan Mutlak (*MUST NOT*)

| # | Larangan | Konsekuensi Pelanggaran | Referensi |
|---|---|---|---|
| 1 | **DILARANG** menggunakan `severity_score`, `folder_category`, `file_name`, atau `split` sebagai fitur input model | **Data Leakage** — model menghafal label, bukan belajar pola | Bab 3.1.C & 7.2 |
| 2 | **DILARANG** melakukan **Transformasi Spasial** (Horizontal/Vertical Flip, Rotasi) saat augmentasi *on-the-fly* | Mengubah orientasi huruf (b→d, p→q) dan menghancurkan diagnosis *letter reversal* | Bab 6.1.C & 7.2 |
| 3 | **DILARANG** memodelkan `severity_score` sebagai tugas **Regresi** (MSE Loss) atau **Kategorikal Multiclass standar** (Cross-Entropy murni) | `severity_score` bersifat *Kategorikal Ordinal*. Categorical Cross-Entropy (CCE) standar itu "buta urutan" (salah tebak 1 ke 6 akan dihukum sama dengan tebak 1 ke 2). Wajib menggunakan **Ordinal Loss** (seperti *Coral Ordinal*). | Bab 7.2 |

### C. Rekomendasi Opsional (*SHOULD*)

| # | Saran | Tujuan |
|---|---|---|
| 1 | Rancang arsitektur **Late Fusion (Multi-Input)**: Branch 1 (CNN) untuk gambar, Branch 2 (Dense) untuk 6 fitur XAI | Memaksimalkan transparansi dan akurasi prediksi |
| 2 | Jalankan **McNemar Test** untuk membandingkan akurasi model yang dilatih pada Dataset A (Gambo murni) vs Dataset B (Gambo+EMNIST) | Memvalidasi secara empiris bahwa augmentasi EMNIST benar-benar meningkatkan performa model |
| 3 | Pahami bahwa 6 fitur XAI diekstrak **pasca-kompresi 28×28** — rasio geometris mencerminkan *kepadatan kanvas*, bukan dimensi kertas asli | Mencegah misinterpretasi klinis pada output model |
| 4 | Lakukan **Pixel-Level Leakage Check** menggunakan *Cryptographic/Perceptual Hashing* | Mendeteksi duplikasi gambar yang lolos dari validasi level nama file |

---

## 8.4 Penutup

> 📌 **Deklarasi Akhir:**
> 
> Laporan teknis ini mendokumentasikan perjalanan *end-to-end* Data Science untuk proyek DyslexiaLens — dari sebuah dataset publik yang penuh cacat (*Label Noise*, *Inverted Severity Score*, *Class Imbalance* 3.35:1), menjadi sebuah **Master Dataset** yang bersih, seimbang (1:1), tervalidasi secara statistik (A/B Testing, Cohen's d), dan dilengkapi kontrak operasional (*Data Dictionary*) yang mengikat.
>
> Dengan ini, seluruh tanggung jawab **Data Scientist** dalam pipeline DyslexiaLens dinyatakan **SELESAI**. 
>
> Estafet resmi diserahkan kepada tim **AI Engineer**.
>
> ---
> *"Data yang bersih adalah fondasi. Model yang cerdas adalah bangunannya. Namun tanpa fondasi yang kokoh, bangunan secantik apapun pasti runtuh."*
> — Tim Data Science, DyslexiaLens
