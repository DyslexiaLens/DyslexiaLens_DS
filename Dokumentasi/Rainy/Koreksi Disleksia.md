# Konsep Pelabelan dan Scoring "DyslexiaLens"

Dokumen ini memuat skema pelabelan target (*target labeling*) untuk dataset huruf yang dikoreksi (Corrected/Reversal) berdasarkan tingkat keparahan (*severity*) visual dari goresan tulisan penderita disgrafia/disleksia.

---

## 1. Keguguran Asumsi Kebocoran Data (Data Leakage)
Sebelumnya diasumsikan bahwa nama awalan file seperti `4_1.png` atau bilangan 1-9 melambangkan karakter angka (digit). Ternyata setelah inspeksi manual, folder-folder dengan label `1, 4, 5, 6, 7, 8, 9` mengandung **hampir seluruh abjad huruf yang ada** — bukan hanya karakter angka.

Berhubung seluruh abjad terdistribusi merata di dalam folder-folder ini, dataset terbukti **tidak mengalami kebocoran data (Data Leakage)**. Kita dapat menggunakan seluruh isi dataset untuk melatih model *Machine Learning* tanpa takut model terjebak belajar *Character Recognition* alih-alih mendeteksi disleksia.

## 2. Arti Angka Folder (1 hingga 9) — Temuan Kunci
Sistem pembagian folder angka **bukan mewakili huruf/karakter yang sedang ditulis**, melainkan melambangkan metrik **Tingkat Keparahan Coretan (Severity Score)** dari tulisan penderita.

Sistem skalanya beroperasi secara **terbalik** (*Inverted Scale*) dari perspektif AI, dengan rincian hasil inspeksi visual sebagai berikut:

| Skor Asli (Periset) | Kondisi Visual | Keparahan Nyata |
|---|---|---|
| **1** | Goresan hancur lebur, tidak bisa ditebak huruf apa | Paling Parah |
| **4** | Goresan banyak timpa-menimpa, kerangka huruf masih samar | Cukup Parah |
| **5 - 8** | Koreksi tampak, huruf masih bisa ditebak tipis-tipis | Menengah |
| **9** | Goresan ringan, huruf aslinya masih mudah dikenali | Paling Ringan |

> [!IMPORTANT]
> Karena skala ini **terbalik** (9 = Ringan, bukan Parah), langsung menggunakannya pada model AI akan menyebabkan *Loss Function*-nya tersesat: model akan menganggap tulisan **paling parah (skor 1) justru paling dekat dengan Normal (skor 0)**. Ini adalah jebakan arsitektural yang harus diperbaiki.

## 3. Normalisasi Skala: Dictionary Mapping ke Skala 0–6

Perbaikan dilakukan menggunakan sistem *Dictionary Mapping* (bukan sekadar `10 - x`) agar skala menjadi linear dan konsisten antara `Corrected` dan `Reversal`:

| Skor Asli File | Skor AI Baru | Keterangan |
|---|---|---|
| `9` | **1** | Paling Ringan |
| `8` | **2** | |
| `7` | **3** | |
| `6` | **4** | |
| `5` | **5** | |
| `4` | **6** | Corrected Paling Parah |
| `1` | **6** | Reversal digabung ke puncak skor 6 |
| Kelas `Normal` | **0** | Bebas Disleksia |

Skor `1` dari data `Reversal` dan skor `4` dari data `Corrected` **disatukan ke puncak skor 6** karena keduanya merepresentasikan tingkat keparahan tertinggi di domain masing-masing. Dengan ini, rentang skor menjadi **mulus dan konsisten dari 0 sampai 6** tanpa ada gap angka kosong.

## 4. Strategi Training Machine Learning (Skema Klasifikasi)
Dengan skema pelabelan baru ini, arsitektur AI "DyslexiaLens" dapat mendukung tiga lapisan tugas sekaligus:

* **Klasifikasi Biner:** `target_class = 0` (Normal) vs `target_class = 1` (Ada Gejala Disleksia)
* **Klasifikasi Multi-kelas (Severity):** Skor `0` hingga `6`, di mana AI memberikan diagnosis tingkat derajat.
* **Klasifikasi Kategori:** Normal vs Corrected vs Reversal

*Contoh Output AI pada pasien:*
> **"Terdeteksi Anomali Goresan. Kategori: Corrected. Skor Keparahan: 6/6 (Sangat Parah — Disarankan segera rujuk ke ahli)."**

Pendekatan ini membuat model kita bukan sekadar *binary classifier* (Ya/Tidak), tetapi **sistem skrining ahli** dengan parameter derajat keparahan yang sangat informatif!

## 5. Temuan Data Auditing: Kontaminasi Label (*Label Noise*)
Selama inspeksi dataset secara manual, ditemukan file dengan format nama `NormalXXXX.png` muncul tidak hanya di dalam kelas `Corrected` dan `Reversal`, melainkan memiliki struktur goresan yang sangat cacat (*scribbling* tumpang tindih). Lebih mengejutkan lagi, isi kelas `Normal` murni milik dataset aslinya juga terbukti mengandung coretan-coretan parah.

Temuan ini membuktikan adanya **Kontaminasi Label (*Label Noise*)** dari pihak pembuat dataset asli — kemungkinan akibat *script rename otomatis* yang tidak disertai verifikasi visual.

**Keputusan Teknis Tim Pengembang (Drop Data):**
Karena model AI akan mengalami kebingungan batas keputusan (*Decision Boundary Confusion*) apabila diberikan "*baseline*" data "Normal" yang sebenarnya cacat, maka diambil keputusan:
1. Mengabaikan seluruh sub-klaster `unknown` dan file `NormalXXXX.png` yang tersesat menggunakan *Logical Cleaning* (tidak ada file yang dihapus secara fisik).
2. Memfokuskan *training loop* hanya pada gambar berindeks `1` hingga `9` (sebelum normalisasi) atau `1` hingga `6` (setelah normalisasi) untuk fitur skor keparahan.
3. Temuan anomali data dan keputusan pemangkasan ini dicatat dalam dokumentasi sebagai bukti proses *Data QA (Quality Assurance)* yang ketat:

> *"Berdasarkan hasil investigasi manual dan pengecekan script algoritmik, ditemukan bahwa sebagian dataset asli mengalami Kontaminasi Label (Label Noise). Gambar dengan tingkat goresan koreksi radikal ditemukan bocor ke dalam kelas Normal. Oleh karena itu, tim pengembang mengambil tindakan pembersihan (Drop Data) pada klaster/folder yang tidak terstruktur untuk menjaga kemurnian pelatihan akurasi AI."*