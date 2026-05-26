# BAB 5: Exploratory Data Analysis (EDA) & Dashboarding

Bab ini memaparkan seluruh temuan visual yang dihasilkan dari proses eksplorasi data (*Exploratory Data Analysis*). EDA dilakukan **setelah** fitur tabular diekstrak (Bab 4), sehingga analisis tidak hanya mencakup distribusi metadata dasar, tetapi juga validasi empiris terhadap ke-6 fitur XAI. Temuan-temuan ini kemudian di-*deploy* ke dalam dashboard interaktif berbasis *Streamlit Cloud* agar dapat diakses oleh *stakeholder* tanpa perlu menjalankan kode Python.

---

## 5.1 Analisis Integritas & Distribusi Dataset

Tahap pertama EDA adalah mengonfirmasi kondisi kesehatan populasi data secara kuantitatif.

### A. Keseimbangan Kelas (Class Imbalance Audit)

Visualisasi *bar chart* mengonfirmasi kembali temuan audit Bab 2 dengan angka matematis yang kritis: dari ~156.453 gambar bersih pasca-*cleaning* (Bab 3), populasi Disleksia (Corrected + Reversal) mendominasi hingga **~120.463 gambar**, sedangkan Normal hanya **~35.990 gambar**. **Rasio ini menyentuh titik kritis ~3.35:1** — sebuah ketimpangan separah ini menjamin bahwa model AI yang dilatih langsung pada data ini akan menderita *Majority Class Bias* (cenderung selalu menebak "Disleksia"). Kuantifikasi ini memberikan mandat mutlak untuk dilakukannya skenario augmentasi dataset.

> 🖼️ **[SUGESTI VISUAL 1]**
> *Tempatkan screenshot bar chart 'Keseimbangan Kelas: Normal vs Disleksia (Dataset Gambo Asli)' dari notebook EDA.*
> `![Class Imbalance](path/ke/gambar_imbalance.png)`

### B. Distribusi Kelas per Split (Train vs Test)

Proporsi relatif antar kelas (Normal, Corrected, Reversal) cukup konsisten baik pada set Train maupun Test bawaan. Meskipun tidak ditemukan *distribution shift* yang ekstrem pada *split* orisinal ini, eksekusi ulang *Stratified Splitting* (yang akan didefinisikan secara formal di Bab 7) tetap diwajibkan demi menjamin integritas saintifik MLOps.


### C. Distribusi Severity Score (0–6)

Distribusi Severity Score sangat bervariasi dan memusat pada rentang skor yang tinggi (Skor 6 / Reversal). Skor `0` (Normal) memiliki populasi yang terlampau kecil untuk menyeimbangi gabungan seluruh level keparahan disleksia. Ketimpangan ini wajib menjadi catatan perhatian khusus jika pengembangan diarahkan menuju arsitektur *Multi-class Classification*.

> 🖼️ **[SUGESTI VISUAL 2]**
> *Tempatkan screenshot bar chart 'Distribusi Severity Score (0 = Normal, 6 = Parah)' dari notebook EDA.*
> `![Distribusi Severity](path/ke/gambar_severity.png)`

---

## 5.2 Analisis Spasial & Piksel (Computer Vision Analytics)

### A. Sampel Visual: Normal vs Corrected vs Reversal

Grid visual 3×5 menampilkan perbedaan mencolok antara ketiga kelas:
- **Normal:** Huruf terbentuk dengan satu goresan dominan yang tegas, bersih, dan mudah dikenali.
- **Corrected:** Goresan tampak tebal dan bertumpuk akibat tekanan pena berulang (*over-tracing/scribbling*), menjadi indikator keraguan menulis.
- **Reversal:** Huruf mengalami efek cermin (*mirror image*) atau rotasi yang tidak lazim, ciri khas utama dari disleksia orientasi spasial.

### B. Pixel Variance Heatmap (Bukti Empiris Inkonsistensi Spasial)

Ini adalah visualisasi agregat paling krusial dalam EDA. Dengan merata-ratakan variansi piksel dari ratusan sampel per kelas:
- **Normal:** Variansi piksel rapat dan terpusat di tengah kanvas. Artinya, anak normal memiliki tata ruang penulisan yang konsisten (selalu di tengah).
- **Disleksia:** Area kuning (variansi tinggi) menyebar sangat luas dan tidak beraturan. Hal ini membuktikan secara **empiris** bahwa penderita disleksia menderita **Inkonsistensi Spasial** (gagal menempatkan posisi huruf secara konstan; coretan bisa berada di pojok, tepi, atas, atau bawah kanvas).

> 🖼️ **[SUGESTI VISUAL 3]**
> *Tempatkan screenshot 'Variance Heatmap: Normal vs Disleksia' (2 panel, colormap magma) dari notebook EDA.*
> `![Variance Heatmap](path/ke/gambar_variance.png)`

### C. Heatmap Rata-rata Piksel: Skor Terendah vs Tertinggi

Perbandingan *Ghost Image* (mean pixel image) antara Skor 1 (Ringan) dan Skor 6 (Parah) mengungkap:
- Skor ringan memiliki pola piksel rata-rata yang lebih tegas dan terkumpul.
- Skor parah menunjukkan rata-rata piksel yang menyebar dan memudar, merepresentasikan variasi bentuk goresan yang ekstrem.
- Panel ketiga ("Selisih Intensitas") dengan *colormap inferno* menandai zona anomali (blind spots) utama di mana distorsi spasial paling sering terjadi.

---

## 5.3 Validasi Fitur XAI: Explanatory Analysis

Bagian ini bersifat **explanatory** (bukan sekadar mencari pola, tetapi menyajikan jawaban definitif atas **empat pertanyaan bisnis utama** dari Bab 1) menggunakan bukti visual.

### Pertanyaan Bisnis 1: *"Apakah dataset asli sudah cukup seimbang untuk melatih model AI?"*
**❌ TIDAK.** Rasio kelas 2:1 adalah ketimpangan yang fatal. Fakta matematis ini secara resmi memicu eksekusi **Augmentasi Dataset** (yang akan dibahas di Bab 6).

### Pertanyaan Bisnis 2: *"Apakah pola visual tulisan tangan cukup kuat merepresentasikan kondisi kognitif disleksia?"*
**✅ YA, SANGAT KUAT.** *Variance Heatmap* memberikan pembuktian tingkat populasi bahwa anak disleksia memiliki letak spasial yang sangat inkonsisten/fluktuatif dibandingkan anak normal.

### Pertanyaan Bisnis 3: *"Bagaimana merancang AI yang mampu menjelaskan keputusannya?"*
**✅ DENGAN ARSITEKTUR LATE FUSION.** Plot distribusi (*Boxplot*) terhadap 4 fitur utama XAI (*stroke_density*, *bounding_box_ratio*, *stroke_transitions*, *horizontal_symmetry*) membuktikan kemampuan pemisahan kelas secara organik. Angka-angka klinis inilah yang kelak dicetak oleh AI untuk merasionalisasi keputusannya.

> 🖼️ **[SUGESTI VISUAL 4]**
> *Tempatkan screenshot '2×2 Boxplot Grid' (Kepadatan Tinta, Bounding Box Ratio, Transisi Garis, Simetri Horizontal) dari notebook EDA.*
> `![Boxplot XAI](path/ke/gambar_boxplot.png)`

### Pertanyaan Bisnis 4: *"Bagaimana sistem dapat memberikan interpretasi klinis terhadap sub-tipe disleksia?"*
**✅ MELALUI PROFILING SUB-TIPE.** KDE Plot (*Kernel Density Estimation*) membuktikan bahwa setiap sub-tipe disleksia memiliki "sidik jari" numerik:
- **Corrected:** Mengelompok kuat di wilayah *Stroke Density* ekstrem (validasi perilaku *over-tracing*).
- **Reversal:** Terdeteksi sangat akurat melalui pola anomali pada metrik *Horizontal Symmetry*.

> 🖼️ **[SUGESTI VISUAL 5]**
> *Tempatkan screenshot 'KDE Plot: Distribusi Stroke Density & Horizontal Symmetry (Corrected vs Reversal)' dari notebook EDA.*
> `![KDE Sub-tipe](path/ke/gambar_kde.png)`

### Tabel Rangkuman Jawaban Pertanyaan Bisnis

| Pertanyaan Bisnis | Jawaban | Bukti Visual |
|---|---|---|
| **[Data Readiness]** Apakah dataset seimbang? | ❌ Tidak (2:1) | Bar chart rasio kelas (Imbalance Fatal) |
| **[RQ 1]** Pola visual disleksia nyata? | ✅ Ya | Variance Heatmap (Inkonsistensi Spasial) |
| **[RQ 2]** AI bisa menjelaskan keputusan? | ✅ Ya | Boxplot pemisahan fitur XAI |
| **[RQ 3]** AI bisa bedakan sub-tipe? | ✅ Ya | KDE Plot sidik jari Corrected vs Reversal |

---

## 5.4 Deployment Dashboard: Streamlit Cloud

Seluruh temuan analitik ini tidak dibiarkan terisolasi di dalam *Jupyter Notebook*, melainkan di-*deploy* ke dalam aplikasi interaktif berbasis **Streamlit Cloud** (`app.py`). Ini memfasilitasi *stakeholder* non-teknis untuk memvalidasi *insight* medis secara mandiri.

### A. Arsitektur Dashboard (5 Tab)

| Tab | Konten | Tujuan |
|---|---|---|
| 📊 **Dataset Summary** | Metrik kuantitatif & distribusi kelas | *Quick overview* kesehatan data |
| 👁️ **Computer Vision** | Heatmap Piksel, Distribusi Severity | Bukti empiris pola visual |
| 🧠 **XAI Profiling** | Boxplot 4 fitur XAI, KDE Plot Sub-tipe | Menjawab Pertanyaan Bisnis 3 & 4 |
| ⚖️ **Stratification** | Komparasi Metrik Keseimbangan Kelas | Visualisasi Imbalance (Menjawab RQ 1) |
| 🔍 **Interactive Viewer** | Operasi *In-Memory Pixel Analytics* | Inspeksi raw data & *Ghost Image* interaktif |

### B. Fitur Teknis Unggulan

1. **Dual-Dataset Toggle:** Sidebar menyediakan sakelar radio untuk membandingkan dataset **tanpa augmentasi** (Original Gambo) dan dataset **dengan augmentasi** (Gambo + EMNIST). *(Catatan: Kehadiran fitur EMNIST di dalam dashboard ini merupakan preview dari strategi penyelesaian imbalance yang baru akan dieksekusi secara detail pada Bab 6).*
2. **Compressed Pixel CSV (`.csv.gz`):** Tab Interactive Viewer memanfaatkan file kompresi CSV yang berisi matriks piksel 28×28 yang telah di-*flatten* ke 784 kolom. Teknik ini memungkinkan *stakeholder* melihat gambar mentah tanpa memerlukan akses ke folder dataset fisik.
3. **Caching (`@st.cache_data`):** Seluruh operasi *loading* data di-*cache* oleh Streamlit untuk mencegah pembacaan ulang CSV pada setiap interaksi pengguna.

> 🖼️ **[SUGESTI VISUAL 6]**
> *Tempatkan screenshot tampilan dashboard Streamlit yang menunjukkan salah satu tab utama (misal: Tab Computer Vision dengan Variance Heatmap).*
> `![Dashboard Streamlit](path/ke/gambar_dashboard.png)`

### C. Pertahanan Arsitektur (*Engineering Highlights*)

Aplikasi ini tidak hanya tentang visualisasi, namun juga unjuk gigi keahlian *Data Engineering*:

1. **OOM (Out-of-Memory) Defense via `.csv.gz`:** Untuk melindungi limitasi RAM *Streamlit Cloud* (1 GB gratis), Tab 5 tidak meload file `.png` fisik. Seluruh matriks gambar di-*flatten* (28×28 = 784 kolom) menjadi data tabular yang kemudian dikompresi tingkat tinggi menggunakan `.csv.gz`. Ini meniadakan beban *I/O Disk* server dan mencegah aplikasi mengalami *crash* saat dieksekusi ribuan kali.
2. **On-the-Fly Matrix Aggregation:** Berbeda dengan *notebook* yang merender *Heatmap* statis, *Interactive Viewer* di aplikasi mampu menghitung *Ghost Image* (rata-rata matriks dari 300 gambar acak) secara **dinamis/real-time** di atas RAM browser. 
3. **Dual-Dataset Scalability:** Dashboard ini telah dirancang untuk berskala. Sidebar sudah dilengkapi dengan *toggle* yang kelak siap digunakan untuk membandingkan populasi **Data Asli (Gambo)** versus **Data Augmentasi (Gambo+EMNIST)**, yang merupakan agenda utama di tahap selanjutnya (Bab 6).

---

> 📌 **Kesimpulan Bab 5:**
> EDA berhasil menjawab seluruh pertanyaan bisnis yang didefinisikan di Bab 1 dengan bukti visual dan statistik yang kuat. Temuan paling kritis adalah konfirmasi bahwa (1) pola disleksia terbukti nyata dan terukur secara piksel, (2) fitur XAI mampu memisahkan kelas secara organik, namun (3) dataset **belum layak** untuk pelatihan model karena *Class Imbalance* yang fatal. Temuan ketiga ini secara langsung memicu keputusan eksekusi untuk melakukan **Augmentasi Dataset menggunakan EMNIST** (Bab 6), yang harus divalidasi melalui A/B Testing sebelum data dinyatakan siap untuk *handover* ke AI Engineer.