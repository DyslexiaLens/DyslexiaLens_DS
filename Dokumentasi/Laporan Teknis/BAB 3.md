# BAB 3: Pembersihan & Rekayasa Data (*Data Cleaning*)

Bab ini mendokumentasikan proses penyelamatan dataset Gambo dari anomali struktural yang ditemukan pada tahap Audit (Bab 2). Filosofi utama dari alur kerja ini adalah **'Logical First, Physical Last'**. Alih-alih menghapus file secara membabi buta, seluruh anomali disaring dan divalidasi terlebih dahulu secara logis di atas DataFrame Pandas. Setelah daftar file bersih (*Master CSV*) terbentuk sebagai cetak biru yang aman, barulah pembersihan fisik (*Physical Sync*) dieksekusi secara terukur.

---

## 3.1 Logical Cleaning & Pembuatan Master CSV

Langkah pertama adalah membangun "saringan" berbasis logika untuk memisahkan data valid dari data sampah, kemudian menuangkan hasilnya ke dalam sebuah master dokumen CSV yang akan menjadi *single source of truth* bagi seluruh *pipeline* AI.

### A. Sistem Penyaringan Lapis Pertama (Regex & OS Validation)

Proses *filtering* diinisiasi dengan 7 ekspresi reguler (Regex) digabungkan dengan **Validasi Sistem Operasi**.

| No. | Mekanisme / Filter | Pola / Kondisi | Target Anomali |
|---|---|---|---|
| 1 | `OS Path Validation` | `os.path.exists()` | Pencegahan *Broken Links* (file korup yang tercatat namun hilang dari *hard disk*) |
| 2 | `RE_DUPLICATE_WIN` | `(\d+)` | File duplikat hasil *copy-paste* Windows (misal: `Normal1305 (11).png`) |
| 3 | `RE_PLACEHOLDER` | `^(Normal\|Reversal\|Corrected).png$` | File *placeholder* tanpa ID yang bukan gambar tulisan tangan asli |
| 4 | `RE_GLITCH` | `.qNcy` | File *glitch* dari *download* terputus dengan ekstensi ganda |
| 5 | `RE_ALPHA_ONLY` | `^[A-Za-z].png$` | File referensi abjad tunggal (misal: `A.png`, `b.png`) |
| 6 | `RE_NORMAL_NUMBER` | `^Normal\d+` | File `Normal_XXX.png` yang anomali/terseret **di dalam folder Normal** |
| 7 | `RE_REVERSAL_NUMBER` | `^Reversal\d+` | File `Reversal_XXX.png` tanpa metrik keparahan yang valid |
| 8 | `RE_STARTS_WITH_ALPHA` | `^[A-Za-z][-_.]` | File dengan format huruf yang menyimpang di folder `Corrected`/`Reversal` |

> 🖼️ **[SUGESTI VISUAL 1]**
> *Tempatkan screenshot output rekapitulasi filter Python yang menunjukkan jumlah file yang dibuang per kategori filter.*
> `![Rekapitulasi Filter Cleaning](path/ke/gambar1.png)`

### B. Rekonstruksi Severity Score & Pemusnahan Label Noise

Setelah penyaringan level fisik selesai, langkah selanjutnya adalah menetralisir *Label Noise* dan Skala yang Terbalik melalui fungsi terpusat `get_score()`.

**1. Eksekusi Mati Label Noise:**
Fungsi memegang aturan validasi silang (*cross-validation*) absolut: `if 'Normal' in filename and folder != 'Normal': return 'DROP'`. Baris ini adalah "peluru perak" yang mengeksekusi semua gambar Normal yang tersesat di folder disleksia.

**2. Pembalikan Skala & Kompatibilitas *Physical Renaming*:**
Selanjutnya, fungsi memetakan ulang skor keparahan agar searah dengan urgensi klinis (nilai kecil = ringan, nilai besar = parah):

| Skor Asli Periset | Kondisi Visual | Makna Nyata | → | Skor Baru (AI Scale) |
|---|---|---|---|---|
| `9` (Corrected) | Koreksi sangat ringan | Paling Ringan | → | `1` |
| `8`, `7`, `6`, `5` | Semakin banyak koreksi | Berjenjang | → | `2`, `3`, `4`, `5` |
| `4` (Corrected) | Goresan hampir tidak terbaca | Parah | → | `6` |
| `1` (Reversal) | Goresan hancur / *letter reversal* | Paling Parah | → | `6` (digabung) |
| `Normal` | Tulisan bersih tanpa gejala | Normal | → | `0` |

Secara rekayasa data, *pipeline* `get_score()` dirancang sangat tangguh (*robust*). Fungsi ini mampu memproses nama file mentah (contoh: `9_23.png`) maupun nama file yang telah direkayasa ulang sebelumnya melalui skrip *Physical Renaming* opsional (`1_23.png`).

Skor keparahan dipetakan ulang agar searah dengan urgensi klinis (nilai 1 = paling ringan, 6 = paling parah). 
Secara rekayasa data, fungsi *parsing delimiter* (`_` dan `-`) sengaja dibuat sangat kaku (*strict*). Jika sebuah file memiliki suffix ganda yang ambigu (misal `9-23_baru.png`), sistem akan langsung menggagalkan *parsing* dan melabelinya `DROP` sebagai bentuk perlindungan dari data *corrupt*. Selain itu, *pipeline* bersifat idempoten; ia mampu memproses nama file mentah maupun file yang telah melalui skrip opsional *Physical Renaming* secara konsisten.

### C. Output: Definisi Kolom Master CSV

Hasil akhir proses cleaning logis adalah file `master_dataset_dyslexia.csv` dengan definisi kolom berikut:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `image_path` | String | Path absolut ke file gambar `.png` |
| `file_name` | String | Nama file (tanpa path) |
| `split` | String | Pembagian bawaan periset: `Train` atau `Test` |
| `folder_category` | String | Kelas asal: `Normal`, `Corrected`, `Reversal` |
| `severity_score` | Integer | Skor keparahan (Multi-Class): `0` = Normal, `1`–`6` = Keparahan |
| `target_class` | Integer | Label biner: `0` = Normal, `1` = Disleksia |

> ⚠️ **Skenario Pemodelan & Pencegahan Data Leakage Kelas Berat:** 
> 1. **Penyatuan Biner vs Multi-Class:** Kolom `target_class` memampatkan `Corrected` dan `Reversal` menjadi kelas `1` murni untuk membangun *baseline screening* (Sehat vs Sakit). Namun, identitas medis yang krusial tetap dikuantifikasi secara ordinal pada kolom `severity_score` (Skor 6 untuk Reversal, 1-5 untuk Corrected) guna melayani skenario model *Multi-class Classification* ke depannya.
> 2. **Bahaya Nama File:** Kolom `severity_score`, `folder_category`, dan **bahkan nama file itu sendiri (`file_name`)** mengandung label (*ground truth*). Keempatnya **diharamkan masuk sebagai fitur**. String *path* murni hanya boleh digunakan sebagai *pointer* pemuatan piksel (`cv2.imread`).
> 3. **Distrust pada Split Bawaan:** Kolom `split` (Train/Test) tetap dipertahankan sekadar untuk referensi komparasi. AI Engineer sangat direkomendasikan mengabaikan split bawaan ini karena potensi ketidakseimbangannya, dan wajib melakukan *Stratified Shuffle Split* atau *K-Fold Cross Validation* ulang dari nol dengan *random seed* yang deterministik.

> 🖼️ **[SUGESTI VISUAL 2]**
> *Tempatkan screenshot output `df_clean.sample(5)` dari notebook yang menampilkan isi master CSV.*
> `![Contoh Isi Master CSV](path/ke/gambar2.png)`

---

## 3.2 Sinkronisasi Fisik & Penghapusan Anomali Background

Setelah cetak biru logis (Master CSV) terbentuk, intervensi fisik *hard disk* dilakukan:

### A. Sinkronisasi Folder Dataset
File `.png` yang **tidak memiliki record di dalam CSV** (karena terkena `DROP` atau Regex) dianggap sebagai sampah (*noise*) dan dihapus secara fisik untuk menghemat ruang.

### B. Penghapusan Anomali *Inverted Background / Overexposed*
Satu filter tambahan berbasis *Computer Vision* diterapkan: menghapus gambar dengan `mean_pixel > 127`. Mengingat standar dataset tulisan tangan AI (seperti MNIST) didominasi latar hitam (piksel 0), gambar dengan *mean* di atas 127 mengindikasikan anomali **Inverted Background** (latar putih, tulisan hitam) atau keberadaan **artefak bercak putih raksasa** (*overexposed*). Memasukkan citra dengan polaritas warna yang terbalik ini akan merusak filter konvolusi CNN.
*(Catatan Batasan: Filter ini sangat efektif membunuh anomali putih, namun belum dirancang untuk menangkap anomali gambar hitam pekat buta (`mean_pixel < 5`). Anomali tersebut ditangguhkan pada tahap inspeksi visual EDA).*

### C. Rebuilding Master CSV (Anti-Ghost Records)
Langkah B (penghapusan fisik gambar anomali putih) menyebabkan CSV memiliki **Ghost Records** (baris data yang merujuk ke file gambar yang baru saja dihapus). Oleh karena itu, skrip pembuatan `master_dataset_dyslexia.csv` wajib di-*rebuild* ulang (*directory scanning*) untuk mengeliminasi semua *Ghost Records* dan menjamin sinkronisasi absolut 100%.

---

## 3.3 Ringkasan Kuantitatif Hasil Cleaning

| Tahap | Proses | Status |
|---|---|---|
| **A** | Logical Cleaning (7 Regex + OS Validation) | ✅ Selesai |
| **B** | Sinkronisasi Folder (Hapus fisik non-CSV) | ✅ Selesai |
| **C** | Penghapusan Anomali Polaritas Putih (`mean_pixel > 127`) | ✅ Selesai |
| **D** | Rebuild `master_dataset_dyslexia.csv` Final | ✅ Selesai |

> 🖼️ **[SUGESTI VISUAL 3]**
> *Tempatkan screenshot log terminal yang menampilkan RINGKASAN KUANTITATIF (Berapa file terhapus oleh get_score, OS Validation, dan BERAPA TOTAL FILE BERSIH yang selamat).*
> `![Ringkasan Kuantitatif Cleaning](path/ke/gambar3.png)`

> 📌 **Kesimpulan Bab 3:**
> Melalui *Logical Cleaning* berlapis yang disusul pembersihan *Inverted Background*, dataset Gambo telah direstorasi. Anomali *Label Noise* musnah, *Severity Score* tertata logis, dan *Ghost Records* berhasil ditumpas. Dokumen CSV akhir yang memuat kumpulan file selamat (*survived files*) ini resmi menjadi **satu-satunya sumber kebenaran (single source of truth)** untuk tahapan ekstraksi fitur (*Explainable AI*).
>
> **Catatan Penangguhan Eksekusi:** Satu-satunya anomali audit (Bab 2) yang **sengaja belum diintervensi** pada tahap pembersihan ini adalah **Class Imbalance**. Isu ketimpangan distribusi tersebut ditangguhkan untuk dieksekusi secara khusus melalui strategi Augmentasi (Injeksi EMNIST) pasca tahap *Exploratory Data Analysis*, demi mencegah tercemarnya kemurnian data asli selama proses perancangan fitur XAI (Bab 4).
