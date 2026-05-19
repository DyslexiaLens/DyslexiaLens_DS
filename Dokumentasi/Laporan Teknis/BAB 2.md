# BAB 2: Audit & Profiling Dataset Awal

Sebelum melakukan pemrosesan data, tahap krusial pertama dalam *pipeline* ini adalah mengaudit "bahan baku" secara menyeluruh. Proses *Assessing Data* ini bertujuan untuk membongkar kotak hitam dataset Gambo, memvalidasi integritas file fisik, serta mengidentifikasi anomali bawaan yang berpotensi merusak model AI jika dibiarkan.

## 2.1 Sumber & Karakteristik Data
Dataset yang dievaluasi adalah **Dyslexia Handwriting Dataset (Gambo)** yang diperoleh dari repositori publik Kaggle. Berdasarkan skrip audit komprehensif yang dieksekusi menggunakan Python, berikut adalah profil fisik dari dataset mentah tersebut:

- **Total Keseluruhan File:** 208.372 gambar.
- **Ekstensi & Format:** 100% berformat `.png`.
- **Resolusi & Dimensi:** Seragam pada ukuran 28×28 piksel.
- **Mode Warna (*Color Mode*):** Seluruhnya konsisten pada mode *Grayscale* (`L`) atau *Binary* (`1`), tanpa ada gambar RGB yang menyusup.
- **Hierarki Folder Asli:** Terbagi atas klasifikasi *Train* dan *Test*, dengan tiga sub-kategori utama di dalamnya: `Normal`, `Corrected`, dan `Reversal`.

> 🖼️ **[SUGESTI VISUAL 1]**
> *Tempatkan screenshot dari Windows Explorer atau output terminal (tree) yang menampilkan struktur hierarki folder Gambo asli.*
> `![Struktur Folder Asli Gambo](path/ke/gambar1.png)`

- **Integritas File:** Tidak ditemukan file *corrupt* atau rusak secara struktural dari hasil ekstraksi dan sampling visual.

> 📊 **[SUGESTI VISUAL 2: TABEL/CHART DISTRIBUSI]**
> *Tempatkan screenshot hasil output code Python yang menampilkan jumlah file per split (Train/Test) dan per kelas. Ini adalah bukti sahih hasil profiling distribusimu.*
> `![Tabel Distribusi Dataset Gambo](path/ke/gambar2.png)`

Secara struktural dan integritas *file* fisik, dataset ini tampak sempurna. Namun, audit semantik (membedah makna nama file dan kesesuaian visual) mengungkap celah logika yang sangat dalam.

## 2.2 Temuan Anomali Kritis (*Data Assessing*)
Melalui inspeksi algoritmik yang dikombinasikan dengan validasi visual acak, kami menemukan **berbagai kelemahan fatal** bawaan dari periset asli:

### A. Kontaminasi Label Silang (*Label Noise*)
Hierarki folder ternyata tidak mencerminkan kebenaran label (*ground truth*) 100%. Ditemukan ratusan file ber-prefix `NormalXXXX.png` yang justru berserakan dan "tersesat" di dalam folder kelas disleksia (`Corrected` dan `Reversal`).

> 🖼️ **[SUGESTI VISUAL 3]**
> *Tempatkan screenshot yang menunjukkan file berawalan `Normal_` terperangkap di dalam folder `Corrected`. Bukti otentik Label Noise.*
> `![Bukti Label Noise](path/ke/gambar3.png)`

Jika dataset ini langsung didistribusikan ke model AI menggunakan *ImageFolder Dataset Generator* standar, model akan "dipaksa" mempelajari tulisan normal sebagai ciri-ciri disleksia. Cacat ini dijamin akan menghancurkan kemampuan prediksi kelas.

### B. Skala *Severity Score* yang Terbalik & Cacat Jarak
Periset asli menyimpan informasi Tingkat Keparahan dengan menyematkan angka di awal nama file (misal: `4_1.png` atau `9_23.png`). Sayangnya, konvensi ini memiliki cacat matematis:

1. **Skala yang Terbalik (Inverted Scale):** Angka `9` merepresentasikan coretan disleksia paling ringan, sedangkan angka `1` dan `4` merepresentasikan goresan yang sangat hancur (*reversal*). Jika model memproses angka ini mentah, AI akan menyimpulkan bahwa skor keparahan `1` sangat mirip dengan label Normal (`0`). Padahal di dunia nyata, `1` adalah kondisi terparah.

> 🖼️ **[SUGESTI VISUAL 4]**
> *Tempatkan perbandingan 2 gambar (kiri: skor 9 yang rapi, kanan: skor 1 yang hancur). Ini visualisasi kuat bahwa skala aslinya terbalik.*
> `![Perbandingan Visual Severity Score](path/ke/gambar4.png)`

2. **Kekosongan Metrik (*Missing Values*):** Rentang asli yang digunakan adalah `1, 4, 5, 6, 7, 8, 9`. Angka `2` dan `3` menghilang sepenuhnya dari ekosistem dataset. Hipotesis logis kami adalah ini terjadi akibat kelalaian protokol pengumpulan data oleh periset asli, di mana perekaman untuk tingkat keparahan tertentu luput dilakukan.

### C. Anomali Visual pada Kelas Normal Asli
Di luar pengecekan skrip, inspeksi manual (*visual sampling*) terhadap folder `Normal` mengungkap adanya kontaminasi dua arah. Sejumlah sampel di folder `Normal` menampilkan coretan koreksi dan tumpang-tindih yang secara visual seharusnya masuk ke kelas `Corrected`. 

> 🖼️ **[SUGESTI VISUAL 5]**
> *Tempatkan screenshot gambar tulisan yang terlihat berantakan/banyak coretan, TAPI nama filenya "Normal-XXX.png".*
> `![Anomali Visual Kelas Normal](path/ke/gambar5.png)`

Temuan ini membuktikan bahwa arsitektur folder fisik dataset Gambo sama sekali tidak bisa dipercaya sebagai *ground truth* tunggal.

### D. Ketimpangan Distribusi (*Class Imbalance*)
Berdasarkan hasil rekapitulasi distribusi awal, ditemukan fakta bahwa kelas `Corrected` mendominasi populasi dataset secara tidak wajar. Ketimpangan kelas (*Class Imbalance*) ini adalah ancaman serius yang akan memicu bias mayoritas (*majority bias*) saat *training* model AI. Oleh karena itu, diperlukan strategi intervensi augmentasi untuk memulihkan ekuilibrium data.

> **Kesimpulan Tahap Audit:** 
> Walaupun Dataset Gambo memiliki spesifikasi teknis piksel yang mumpuni, ia menyimpan kelemahan fatal pada arsitektur semantiknya (*Label Noise* dua arah, *Severity Score* kacau, dan *Class Imbalance*). 
> 
> **Implikasi Sistem (Action Item):** Fakta temuan ini *mengharamkan* AI Engineer untuk melatih model menggunakan metode pembacaan hirarki folder standar (seperti `ImageFolder` pada PyTorch/Keras). Mengandalkan folder fisik pasti akan berujung pada *Data Poisoning*. Sebagai gantinya, tahap pembersihan (Bab 3) wajib menghasilkan sebuah master dokumen CSV terpusat yang akan bertindak sebagai otoritas mutlak *ground truth* untuk melatih AI.
