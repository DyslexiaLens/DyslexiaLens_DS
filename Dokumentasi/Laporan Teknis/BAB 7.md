# BAB 7: Penyiapan Data Final (*Data Preparation*)

Bab ini adalah tahap pemaketan terakhir sebelum seluruh aset data diserahkan (*handover*) ke tim AI Engineer. Seluruh proses di bab sebelumnya — pembersihan anomali (Bab 3), ekstraksi fitur XAI (Bab 4), validasi EDA (Bab 5), dan bukti keamanan augmentasi EMNIST (Bab 6) — bermuara di sini. Dataset final harus melewati dua gerbang kritis: **Stratified Splitting** yang menjamin keadilan distribusi, dan **Data Dictionary** yang menjadi kontrak formal spesifikasi data.

---

## 7.1 Stratified Splitting

### A. Mengapa Split Bawaan Dataset Tidak Digunakan?

Dataset Gambo asli sudah memiliki pembagian Train/Test bawaan dari periset awal. Namun, di Bab 3 kita telah memutuskan bahwa split bawaan ini **tidak memenuhi standar MLOps** karena:
1. **Tidak ada set Validasi** — Model AI membutuhkan tiga partisi (Train/Validation/Test), bukan hanya dua.
2. **Stratifikasi tidak terjamin** — Tidak ada bukti bahwa periset awal melakukan *stratified sampling* berdasarkan `severity_score`. Tanpa stratifikasi, dimungkinkan satu level keparahan seluruhnya masuk ke Train dan tidak ada representasinya di Test — menghasilkan evaluasi yang menipu.
3. **Populasi berubah** — Setelah augmentasi EMNIST (Bab 6), komposisi dataset berubah total. Split lama menjadi tidak relevan.

### B. Mekanisme *Stratified Shuffle Split*

Pembagian ulang dilakukan menggunakan `sklearn.model_selection.train_test_split` dengan parameter `stratify=df['severity_score']`. Ini menjamin bahwa **proporsi setiap level keparahan (0–6) terjaga identik** di seluruh partisi.

| Parameter | Nilai |
|---|---|
| **Rasio Train** | 70% |
| **Rasio Validation** | 15% |
| **Rasio Test** | 15% |
| **Stratifikasi** | Berdasarkan `severity_score` (7 level: 0–6) |
| **Random State** | 42 (Reprodusibilitas) |

Split dilakukan dalam dua tahap:
1. **Tahap 1:** Pisahkan 15% sebagai Test (stratified), sisanya 85% menjadi pool Train+Validation.
2. **Tahap 2:** Dari pool 85%, pisahkan ~17.6% (= 15/85) sebagai Validation (stratified). Sisanya menjadi Train final (70%).

> 🛡️ **Justifikasi Split Konservatif (70/15/15):**
> Pada era *Deep Learning*, dataset masif (>200.000 sampel) umumnya memadai dengan rasio 90/5/5. Namun, proyek ini secara sadar mempertahankan pendekatan konservatif 70/15/15. Morfologi tulisan tangan anak-anak memiliki variansi visual (*noise*) yang ekstrem. *Test Set* berukuran raksasa (>30.000 gambar) mutlak dipertahankan agar evaluasi metrik (F1-Score/Recall) benar-benar kebal terhadap anomali outlier dan mewakili 7 level keparahan secara representatif.

> 🛡️ **Pertahanan Metodologi (Sub-Group Stratification):**
> Kelas 0 (Normal) merupakan gabungan dari data Gambo Asli dan injeksi EMNIST. Secara teoritis, fungsi `stratify` hanya menjaga total populasi kelas 0, bukan sub-grupnya. Namun, berkat ukuran sampel kelas 0 yang sangat masif (>100.000 data), **Hukum Bilangan Besar (*Law of Large Numbers*)** secara matematis menjamin bahwa rasio internal Gambo vs EMNIST di dalam *Test set* akan tersebar secara proporsional dan mencegah terjadinya *Distribution Shift*.

### C. Validasi Integritas Split

Setelah split dieksekusi, tiga lapisan verifikasi dijalankan secara otomatis:

1. **Sinkronisasi CSV vs Direktori:** Jumlah baris di `master_dataset_final_balanced_rill.csv` dibandingkan secara matematis dengan jumlah file `.png` fisik di folder `Dataset/Gambo_Balanced/`. Hasil: **100% sinkron**.
2. **Missing File Audit:** Setiap `image_path` di CSV divalidasi keberadaan fisiknya di *disk*. Hasil: **0 file hilang**.
3. **Data Leakage Check (Zero Overlap):** Irisan (*intersection*) dihitung secara eksplisit antar himpunan partisi.
   > ⚠️ **Koreksi Logika Validasi:** Mengiris nilai `image_path` secara utuh akan selalu menghasilkan `0` (ilusi validasi) karena keberbedaan prefix folder (`/Train/`, `/Test/`). Oleh karena itu, pengujian *Zero Overlap* ini dieksekusi secara ketat pada kolom `file_name` (basename murni) untuk memastikan tidak ada duplikasi identitas lintas partisi. Hasilnya:
   - Train ∩ Validation = **0**
   - Train ∩ Test = **0**
   - Validation ∩ Test = **0**

> ✅ **Verdict:** Dataset dinyatakan **bebas kebocoran data (*Zero Data Leakage*) di level nama file**. 
> *(Catatan Handover: Mengingat sejarah dataset Gambo yang tidak diketahui riwayat duplikasinya, validasi kebocoran level piksel menggunakan Cryptographic/Perceptual Hashing direkomendasikan sebagai pengamanan ekstra di masa depan).*

> 🖼️ **[SUGESTI VISUAL 1]**
> *Tempatkan screenshot Pie Chart proporsi split (70/15/15) dan Bar Chart distribusi kelas per split dari notebook Tahap 5.*
> `![Proporsi Split](path/ke/gambar_split.png)`

### D. *Class Weights* untuk AI Engineer

Meskipun augmentasi EMNIST telah menyeimbangkan rasio global menjadi ~1:1, distribusi `severity_score` (7 level) tetap tidak seimbang secara alami. Untuk mengakomodasi hal ini, *class weights* dihitung secara otomatis menggunakan `sklearn.utils.class_weight.compute_class_weight('balanced')` **khusus dari data Train saja** (mencegah bocornya informasi Validation/Test ke dalam parameter pelatihan).

Hasil perhitungan ini disimpan dalam dua *dictionary*:
- **`binary_weight_dict`**: Bobot untuk klasifikasi biner Normal (0) vs Disleksia (1).
- **`severity_weight_dict`**: Bobot untuk klasifikasi multi-kelas Severity Score (0–6).

AI Engineer **wajib** memasukkan *dictionary* ini ke parameter `class_weight` pada fungsi `model.fit()`.

> ⚠️ **Peringatan Arsitektur Multi-Kelas (*Gradient Explosion*):**
> Mengingat ketimpangan tajam antara Skor 0 (~102.000 sampel) dan Skor 6 (skala ribuan), penggunaan `severity_weight_dict` rentan memicu ketidakstabilan gradien (*Gradient Instability*) karena bobot penalti untuk kelas minoritas menjadi terlampau raksasa. AI Engineer direkomendasikan untuk menaklukkan **Klasifikasi Biner (0 vs 1)** terlebih dahulu, dan menjadikan klasifikasi *Severity* sebagai iterasi sekunder dengan penyesuaian *learning rate* yang hati-hati.

---

## 7.2 Data Dictionary Final

Berikut adalah spesifikasi formal (**kontrak data**) dari file output utama `master_dataset_final_balanced_rill_featured.csv`:

| Kolom | Tipe Data | Deskripsi | Rentang Nilai |
|---|---|---|---|
| `image_path` | String | Path ke file gambar `.png` | `Dataset/Gambo_Balanced/Train/...` |
| `file_name` | String | Nama file gambar fisik (termasuk prefix split) | `Train_Normal_A-3.png` |
| `split` | String | Partisi dataset | `Train`, `Validation`, `Test` |
| `folder_category` | String | Kategori kelas diagnosis | `Normal`, `Corrected`, `Reversal` |
| `severity_score` | Integer | `[ORDINAL CATEGORICAL]` Skor keparahan (skala ternormalisasi Bab 3) | `0` = Sehat, `1`–`6` = Ringan–Parah |
| `target_class` | Integer | Label target klasifikasi biner | `0` = Normal, `1` = Disleksia |
| `stroke_density` | Float | `[RAW]` Kepadatan area tulisan (Bab 4) | `0.0` – `1.0` |
| `center_of_mass_x` | Float | `[RAW]` Pusat massa goresan sumbu-X (Bab 4) | `0.0` – `27.0` |
| `center_of_mass_y` | Float | `[RAW]` Pusat massa goresan sumbu-Y (Bab 4) | `0.0` – `27.0` |
| `bounding_box_ratio` | Float | `[RAW]` Rasio *Active Ink Span* (Bab 4) | `> 0.0` |
| `stroke_transitions` | Float | `[RAW]` Rata-rata transisi warna per baris (Bab 4) | `≥ 0.0` |
| `horizontal_symmetry` | Float | `[RAW]` Skor simetri spasial absolut (Bab 4) | `0.0` – `1.0` (terkompresi > 0.85) |

### Aturan Penggunaan untuk AI Engineer

| Aturan | Penjelasan |
|---|---|
| **Input model utama** | Matriks piksel gambar dari `image_path` (28×28 grayscale) |
| **Input model sekunder** | 6 fitur XAI tabular (opsional, untuk arsitektur *Late Fusion*) |
| **Kewajiban Feature Scaling**| 6 fitur XAI di atas bersifat **mentah (unscaled)**. Wajib mengaplikasikan *StandardScaler/MinMaxScaler* pada fitur ini sebelum menggabungkannya (*concat*) ke dalam *Dense Layer* untuk mencegah *Weight Dominance*. |
| **Interpretasi Geometris** | ⚠️ AI Engineer wajib memahami bahwa 6 fitur XAI diekstrak **SETELAH** kompresi gambar absolut ke 28×28 piksel (Bab 4). Oleh karena itu, rasio (seperti `bounding_box_ratio`) melambangkan *kepadatan spasial* di dalam kanvas kompresi, BUKAN *aspect ratio* asli dari goresan di atas kertas. |
| **Output utama** | `target_class` (klasifikasi biner: Normal vs Disleksia) |
| **Output sekunder** | `severity_score` (klasifikasi multi-kelas: 7 level keparahan) |
| **❌ PELARANGAN REGRESI** | `severity_score` (0-6) adalah variabel **kategorikal ordinal**, BUKAN variabel kontinu. Dilarang memodelkannya sebagai Regresi (misal: dengan *MSE Loss*) karena jarak keparahan antar skor tidaklah linier. Wajib diproses sebagai *Multi-Class Classification*. |
| **⚠️ KOLOM TERLARANG** | `severity_score`, `folder_category`, `file_name`, `split` → menggunakannya sebagai input fitur akan menyebabkan **Data Leakage** fatal |
| **Format gambar** | Grayscale, 28×28 piksel, `.png` |
| **❌ LARANGAN MUTLAK** | **Transformasi Spasial (Horizontal/Vertical Flip & Rotasi)** dilarang keras saat augmentasi *on-the-fly* karena merusak makna klinis (misal: "b" menjadi "d"). |

### File Output untuk Handover

| File | Deskripsi |
|---|---|
| `master_dataset_final_balanced_rill_featured.csv` | ***Single Source of Truth*** — Metadata lengkap, path bersih, label tervalidasi, dan 6 fitur XAI |
| `Dataset_Gambo_Balanced.zip` | Arsip seluruh gambar `.png` (Train/Validation/Test) yang siap diekstrak dan di-*load* |

*(Catatan: File CSV representasi piksel dari pipeline No-Augment sebelumnya telah ditarik dari daftar handover guna mencegah AI Engineer melakukan evaluasi pada universe data yang salah).*

---

📌 **Kesimpulan Bab 7:** Dataset akhirnya telah berhasil melewati seluruh gerbang kualitas secara paripurna. Melalui proses *Stratified Split*, representasi proporsional setiap level keparahan di seluruh partisi dapat dijamin, dan protokol *Zero Data Leakage* telah dibuktikan secara ketat secara algoritmik di level *filename*. Kehadiran *Data Dictionary* turut mengunci integritas ini dengan memberikan kontrak formal yang mengikat tim AI Engineer agar tidak menyalahgunakan kolom terlarang, sembarangan menormalisasi fitur *raw*, atau melakukan augmentasi spasial yang berpotensi merusak diagnosis. Dengan pencapaian ini, seluruh tanggung jawab tim Data Scientist dalam *pipeline* hulu DyslexiaLens secara resmi dinyatakan selesai. Tongkat estafet kini sepenuhnya diserahkan kepada tim AI Engineer untuk memulai perancangan arsitektur dan pelatihan model. Rangkuman final mengenai seluruh temuan dan rekomendasi strategis akan dipaparkan di Bab 8 (Kesimpulan & Handover).
