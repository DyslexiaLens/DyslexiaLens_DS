# Checkpoint 9 — Finalisasi Dashboard Eksekutif, XAI Feature Engineering, & Serah Terima Proyek
**Tanggal:** 17 Mei 2026  
**Role:** Data Scientist  
**Status Proyek:** `95% COMPLETE` (Hanya Tersisa objective yang bersifat Opsional)

---

## 🎯 Ringkasan Eksekutif Sesi
Sesi ini menandai **titik akhir (finish line)** dari seluruh tanggung jawab *Data Science* dalam proyek DyslexiaLens. Setelah fondasi data (`Gambo` dan `EMNIST`) dikunci pada *Checkpoint* sebelumnya, beban kerja di sesi ini sangatlah masif. Kami harus menjembatani gap antara *raw data* menuju presentasi bisnis yang *actionable* dan interpretasi AI klinis.

Sesi yang padat ini dihabiskan untuk merumuskan **5 Fitur Matematika Geometri (Explainable AI/XAI)**, mengeksekusi visualisasi statis canggih (*Heatmap, KDE, Boxplot*), mengelola arsitektur *asset caching*, merekonstruksi UI/UX *Executive Dashboard* Streamlit, serta melakukan sterilisasi akhir pada 3 *Jupyter Notebook* utama.

---

## 🚨 Pencapaian & Resolusi Besar Sesi Ini

### 1. Merumuskan 5 Fitur Geometri untuk Explainable AI (XAI)
**(Referensi: `csv_metadata/` & Streamlit Tab 3)**
**Konteks:** Model *Deep Learning* standar (seperti ResNet/VGG) terkenal sebagai *"Black Box"*, yang mana sangat berbahaya di ranah medis/skrining klinis karena mereka tidak bisa menjelaskan *mengapa* seseorang diklasifikasikan sebagai Disleksia.
**Tindakan Resolusi:** 
- Kami merancang dan mengekstrak **5 fitur matematis turunan** dari matriks piksel 28x28 untuk menangkap sinyal motorik halus ( *fine motor control* ) penderita disleksia:
  1. `ink_density`: Menghitung rasio tinta hitam untuk mendeteksi anomali penekanan pena berlebih (*over-tracing*).
  2. `center_of_mass_x` & `y`: Menghitung pergeseran gravitasi tarikan garis untuk mendeteksi ketidakstabilan spasial.
  3. `bounding_box_ratio`: Mengukur rasio panjang-lebar kotak imajiner untuk mendeteksi proporsi huruf yang terdistorsi.
  4. `horizontal_symmetry`: Indikator utama (*Golden Feature*) untuk menangkap anomali pencerminan huruf (*Reversal* / efek cermin).
  5. `stroke_transitions`: Menghitung frekuensi perubahan warna (putih ke hitam) yang secara akurat memetakan tingkat getaran (*Tremor*) atau keraguan saat menulis.
- **Hasil:** Berkat kerja keras ekstraksi matematis ini, AI kita kelak bisa memberikan justifikasi logis layaknya pakar grafologi.

### 2. Arsitektur Aset Visual & Caching Strategy
**(Referensi: Folder `assets/`)**
**Konteks:** Menjalankan komputasi *Heatmap* atau *KDE Plot* dari dataset berukuran >273.000 sampel secara *real-time* di Streamlit akan menyebabkan *server crash* atau jeda *loading* yang tidak dapat ditoleransi oleh audiens.
**Tindakan Resolusi:** 
- Membangun strategi *Pre-calculated Assets*. Seluruh visualisasi berat di-*generate* terlebih dahulu melalui *Notebook* dan disimpan sebagai gambar `.png`.
- Membangun direktori dinamis `assets/EMNIST/` dan `assets/noAugmentation/`.
- Memprogram *script* `app.py` agar melakukan *routing* gambar secara cerdas berdasarkan pilihan *Dataset Toggle* (Murni vs Augmentasi) yang dipilih pengguna di *sidebar*.
- **Hasil:** Dashboard memuat visualisasi kompleks dalam hitungan milidetik tanpa membebani RAM sama sekali.

### 3. Merombak Streamlit menjadi "Executive Dashboard"
**(Referensi: `app.py`)**
**Konteks:** Aplikasi Streamlit sebelumnya terasa kaku bak laporan metrik biasa. Tabel angka desimal membuat audiens non-teknis kesulitan mencerna pembuktian hipotesis klinis kita.
**Tindakan Resolusi:** 
- **Arsitektur 5 Tab Interaktif:** Memecah antarmuka menjadi 5 ruang fokus: *Dataset Summary, Computer Vision, XAI Profiling, Stratification,* dan *Interactive Viewer*.
- **Data Storytelling UI:** Mengganti deretan tabel dengan visualisasi konklusif. Menambahkan UI Callout (*Kotak Pesan* interaktif) yang menyandingkan visual grafik dengan jawaban atas **4 Pertanyaan Bisnis** utama secara gamblang.
- **Dark-Mode Native UX:** Membuang blok *hardcode* HTML statis dan mengimplementasikan komponen bawaan Streamlit (`st.info`, `st.warning`, `st.success`) yang 100% responsif dan elegan di *Dark Mode*.
- **Hasil:** Aplikasi kini merupakan *Showcase* level eksekutif yang berhasil menerjemahkan angka-angka matematika rumit menjadi kesimpulan klinis yang intuitif.

### 4. Kurasi Skala Besar & Standarisasi Dokumentasi Notebook
**(Referensi: `Dyslexia_EMNIST.ipynb`, `Dyslexia_NoAugmentation.ipynb`, `EMNIST_to_Gambo.ipynb`)**
**Konteks:** Ketiga *Jupyter Notebook* utama menyimpan logika pemrosesan data yang krusial, namun narasi dokumentasinya berantakan dan rawan membingungkan *engineer* selanjutnya.
**Tindakan Resolusi:** 
- Menggunakan pendekatan cerdas dengan **mengekstrak sel Markdown secara paralel** ke file eksternal sementara (folder `MD/`) demi kemudahan kurasi massal.
- Membersihkan total *bug redundant code* ratusan baris di bagian eksekusi *balancing* tanpa merusak logika algoritma *Fair Pruning* (Top-Down Indexing).
- Menyeragamkan (*standardize*) seluruh diksi dokumentasi menggunakan terminologi Data Engineering (*Boolean Masking, Data Stratification, dll*).
- Mengembalikan (*re-integrate*) Markdown yang sudah disterilkan ke dalam *Notebook* aslinya.
- **Hasil:** Ketiga Notebook utama kita kini layak disebut sebagai *Playbook* berstandar industri.

### 5. Finalisasi README.md & Penegasan Peran
**(Referensi: `README.md`)**
**Konteks:** Deskripsi awal repositori tertinggal jauh dari progres riil (belum mencakup EMNIST dan XAI). Posisi pekerjaan juga membingungkan karena mencampur aduk porsi spesialis *Data Science* dengan *CNN Modeling*.
**Tindakan Resolusi:** 
- Penulisan ulang total manifesto `README.md` untuk menegaskan bahwa rasio 1:1 (~273k gambar) telah tercapai dan AI tidak akan terkena penyakit *Majority Class Bias*.
- Menegaskan batas wilayah kerja *Data Science*:
  - **Rainy (Lead):** *Dataset Auditing, Data Wrangling, Stratified Splitting, XAI Feature Eng., & Dashboarding.*
  - **w0pal:** *EMNIST-GAMBO Integration (Balancing), Metadata Construction, & Pipeline Automation.*
- **Hasil:** Repositori menjadi portofolio *masterpiece* yang secara akurat memetakan jerih payah tim memformulasikan sistem.

---

## 🧠 Evolusi Filosofi Proyek
Sesi ini menjadi mahkota dari seluruh fase *Data Science*. Anda membuktikan bahwa seorang *Data Scientist* yang hebat tidak hanya berhenti di tahap membersihkan tabel atau menyeimbangkan kelas data (seberat apa pun itu). Dengan membangun fitur matematis (XAI) dan merancang arsitektur presentasi (*Streamlit Data Storytelling*), Anda memastikan bahwa kerja keras tim bisa dipahami, dipercaya secara klinis, dan membawa dampak nyata bagi *stakeholders*.

---

## 🚀 Dampak Strategis & Status Akhir
Dengan diselesaikannya Checkpoint 9 yang epik ini, maka:
- Tabel CSV *Train/Test* murni maupun augmentasi sudah memiliki fitur matematis siap latih (*Machine Learning Ready*).
- Repositori telah disterilkan dari kode sampah.
- Presentasi akhir sudah siap ditunjukkan ke dosen atau investor via Dashboard.

Fase **Data Science Preparation** dinyatakan: **100% COMPLETE**. Estafet tugas selanjutnya kini murni diserahkan ke *AI/Machine Learning Engineer* untuk fase konstruksi *Late Fusion CNN Architecture*.
