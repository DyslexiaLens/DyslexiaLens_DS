# Logika Pemrosesan Dataset (Pipeline Preprocessing) "DyslexiaLens"

Dokumen ini merekam secara rinci seluruh proses rekayasa data (*Data Engineering*) dan perbaikan logika (*Logic Fixes*) yang telah dilakukan pada dataset asli "Gambo" sebelum dimasukkan ke dalam model *Machine Learning*.

---

## 1. Pendekatan Pembersihan Logis (*Logical Cleaning* via CSV)
Mengingat dataset berjumlah lebih dari 208.000 file gambar, melakukan penataan data secara fisik (membuat, menghapus, atau memindahkan file di Windows Explorer / Google Drive) sangat tidak direkomendasikan karena akan:
* Membebani I/O *storage* (terutama Google Drive yang sangat lambat untuk operasi *mass file I/O*).
* Menghilangkan jejak rekam (*reproducibility*) — tidak ada *log* pencatatan.
* Berpotensi merusak atau menghapus data asli secara permanen.

**Penyelesaian:** Pendekatan *Logical Cleaning* diterapkan menggunakan *Jupyter Notebook* (`Dyslexia.ipynb`):
1. Semua jejak jalur file (*file path*) di-*scan* lalu dimasukkan ke dalam tabel leksikon (*Pandas DataFrame*).
2. File gambar kotor atau kontaminasi label (seperti `NormalXXXX.png` yang terselip di folder disleksia) **dibuang dari record tabel CSV** — tanpa menghapus file aslinya.
3. Sisa data yang lolos seleksi disimpan ke `master_dataset_dyslexia.csv`.

Model AI (CNN) **hanya akan membaca gambar yang terdaftar di CSV ini**. Gambar kotor yang masih ada di disk sepenuhnya diabaikan.

## 2. Preprocessing Fisik Opsional (Physical Renaming)
Sebagai langkah tambahan opsional, nama file gambar fisik dapat diganti secara massal agar skala keparahannya konsisten dan langsung terbaca dari nama file.

**Script:** Tersedia di `Dyslexia.ipynb` sebagai **Tahap 2**.

**Mekanisme:**
* Menggunakan sistem *Dictionary Mapping* (bukan rumus matematika sederhana).
* Dua fase rename untuk mencegah konflik nama (*collision*): **FASE 1** mengganti nama ke `.TEMP`, lalu **FASE 2** menghapus sufiks `.TEMP`.
* Dilengkapi sistem *Retry* (10x percobaan dengan `time.sleep(0.1)`) untuk mengatasi Windows `PermissionError (WinError 32)` yang terjadi saat Windows Defender/Antivirus mengunci file sementara.

## 3. Normalisasi Skala Keparahan (*Inverted Severity Scale*)
Dari hasil inspeksi manual (*Visual QA*), ditemukan kejanggalan dalam struktur nama penomoran yang diberikan periset asli untuk kelas `Corrected` dan `Reversal`:
* Angka **1** = Dysgrafia Paling Parah / Hancur.
* Angka **9** = Paling Ringan / Mendingan.

Jika dipertahankan mentah-mentah, *Loss Function* AI akan mengalami kerusakan arsitektural:
> AI menganggap skor mulai dari 0 (Normal). Jika tulisan paling parah diberi skor 1, AI akan menyimpulkan bahwa tulisan paling parah justru **paling mirip dengan Normal**!

**Perbaikan Teknis:** Skala dikoreksi menggunakan *Dictionary Mapping* agar konsisten dan tidak ada gap angka:

| Skor Asli (File) | Skor AI Baru | Keterangan |
|---|---|---|
| `9` | **1** | Paling Ringan |
| `8` | **2** | |
| `7` | **3** | |
| `6` | **4** | |
| `5` | **5** | |
| `4` | **6** | Corrected Paling Parah |
| `1` | **6** | Reversal — digabung ke puncak 6 |
| Normal | **0** | Bebas Disleksia |

Skor Reversal asli (`1`) dan Corrected terparah (`4`) **digabung ke skor tunggal 6** karena keduanya merepresentasikan tingkat keparahan tertinggi di domain masing-masing, dan menggabungkannya menghindari gap kosong di angka 7 dan 8.

## 4. Struktur Tabel *Training* Final (`master_dataset_dyslexia.csv`)
Hasil akhir dari *pipeline* ini memaksa model AI untuk mempelajari tiga parameter utama per barisnya:

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `image_path` | String | Jalur lengkap lokasi file gambar |
| `split` | String | `Train` atau `Test` |
| `folder_category` | String | `Normal`, `Corrected`, atau `Reversal` |
| `severity_score` | Integer (0–6) | Skor keparahan disleksia (0 = Sehat, 6 = Ekstrem) |
| `target_class` | Integer (0/1) | Label biner: 0 = Normal, 1 = Ada gejala disleksia |

## 5. Strategi Keseimbangan Kelas Murni (*Pure Class Weighting*)
Terdapat ketimpangan data antara Normal (58k) dan Disleksia (121k). Pipeline ini **menolak skema Data Augmentation fisik maupun Undersampling** karena berisiko merusak pola alami (*Overfitting*) dan membuang puluhan ribu data. 
Sebagai gantinya, Data Scientist memproses sebuah matriks bobot (*Dictionary Mapping*) menggunakan pustaka Scikit-Learn.
- Normal akan diberikan bobot penalti kekeliruan (Weight) sebesar: `1.55` (Skala Prioritas Tinggi)
- Disleksia diberikan bobot: `0.75` (Skala Prioritas Normal)

Mekanisme ini memungkinkan Neural Network menyesuaikan diri di level kalkulasi loss-function (*Algorithmic Level*) alih-alih di level manipulasi data (*Data Level*).

## 6. Algoritma Pengambilan Skor (*Dual-Path Logic*)
Untuk memastikan *reproducibility* baik di lingkungan lokal maupun *cloud* (Google Colab), fungsi `get_score` di Tahap 3 dirancang untuk menangani dua kondisi secara otomatis:
1. **Lokal (Post-Stage 2):** Jika *Physical Renaming* sudah dijalankan, kode membaca skor 1-6 langsung dari nama file.
2. **Cloud/Colab (Pre-Stage 2):** Jika *Physical Renaming* dilewati untuk menghemat I/O, kode otomatis menerapkan *Dictionary Mapping* dari skor asli periset ke skala AI 0-6.

```
[Tahap 1] Assessing Data (Wajib)
          ↓ Cek distribusi, integritas (sampling), dan anomali label.
[Tahap 2] Physical Renaming (Opsional)
          ↓ Ganti nama file fisik ke skala 1-6 (Dictionary Mapping).
[Tahap 3] Cleaning Data & CSV Generation (Wajib)
          ↓ Filter noise & normalisasi skor → master_dataset_dyslexia.csv
[Tahap 4] Exploratory Data Analysis & Explanatory
          ↓ Analisis pola dan distribusi data bersih.
[Tahap 5] Stratified Validation Split & Class Weights 
          ↓ Pembagian rasio akurat (Train/Val/Test) & Matriks Anti-Imbalance
[Tahap Akhir] Handover ke AI Engineer
          ↓ master_dataset_final.csv siap ditraining.
```
