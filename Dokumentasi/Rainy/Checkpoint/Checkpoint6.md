# Checkpoint 6 — Standardisasi EMNIST, Pembersihan Pipeline, & Optimasi Dashboard (DyslexiaLens)
**Tanggal:** 04 Mei 2026  
**Peran:** Data Scientist  

---

## 🎯 Ringkasan Eksekutif Sesi
Sesi ini berfokus pada resolusi dari tantangan *Class Imbalance* yang membayangi dataset kita, sekaligus menjadi titik pembersihan kode-kode historis (legacy) yang kurang efisien. Kita resmi mengadopsi integrasi **Gambo + EMNIST ByClass** sebagai *Single Source of Truth* untuk dataset training yang diaugmentasi.

Selain perombakan pipeline dataset, sesi ini juga menyembuhkan *Dashboard Streamlit* kita dari penyakit kronis berupa kebocoran memori (*Memory Leak*) yang terjadi dalam dua gelombang — crash saat pindah tab, dan crash saat memilih kelas Disleksia di Viewer. Keduanya telah ditangani hingga dashboard serah terima (*Handover Dashboard*) kini kokoh, stabil, dan siap mendemonstrasikan analisis piksel secara *real-time*.

---

## 1. Perombakan Pipeline Dataset (Resolusi Keseimbangan EMNIST)
**Konteks:** Pada fase riset awal yang dilakukan kolega kita (w0pal), ekstraksi EMNIST memiliki potensi *data leakage* dan proses penggabungannya ke dalam arsitektur folder Gambo kurang mulus secara indeks penamaan. Selain itu, penambahan data EMNIST mentah menyebabkan ledakan pada kelas "Normal", menggeser isu *Class Imbalance* dari yang awalnya didominasi "Disleksia" kini menjadi didominasi "Normal".

**Tindakan Resolusi:**
- Kita membuat *Jupyter Notebook* baru yang ramping dan terotomatisasi penuh: `notebooks/Dyslexia_EMNIST.ipynb`. Notebook ini menggantikan script lama.
- Seluruh sampel abjad EMNIST kini di-ekstrak, difilter (membuang data numerik 0-9), lalu disuntikkan secara sekuensial (misal: `A-524.png`) agar selaras dengan skema penamaan bawaan dataset Gambo.
- **Implementasi Algoritma Pemangkasan (Balancing):** Untuk menekan lonjakan kelas Normal, sebuah sel algoritma *Binary Search* ditambahkan di akhir *pipeline*. Algoritma ini secara cerdas mencari *cap* (batas maksimal) dan memangkas jumlah huruf EMNIST yang berlebih (dimulai dari huruf yang populasinya paling bengkak). 
- **Hasil:** Rasio final berlabuh pada angka yang hampir sempurna yaitu **1:1** (~142.000 Disleksia berbanding ~131.000 Normal).

---

## 2. Operasi Penyembuhan Dashboard Streamlit (Memory Leak Fix — Gelombang 1)
**Konteks:** Dashboard eksplorasi `app.py` sering mengalami *Crash/Force Close* mendadak saat pengguna berpindah-pindah tab.

**Diagnosa & Penanganan Akar Masalah:**
1. **Matplotlib Figure Leak:** Perenderan grafik (*plot*) menggunakan `matplotlib` tidak ditutup dengan benar, menyebabkan penumpukan *figure* di RAM. **Solusi:** Seluruh eksekusi grafik kini dibungkus secara ketat menggunakan blok `try/finally` dengan perintah absolut `plt.close(fig)`.
2. **Global State Conflict:** Penggunaan sintaks global `plt.title()` atau `plt.ylabel()` menyebabkan Streamlit kebingungan meletakkan label saat *rerun* UI terjadi. **Solusi:** Migrasi secara masif ke *Object-Oriented Plotting* dengan spesifikasi sumbu absolut (`ax.set_title()`, `ax.set_ylabel()`).
3. **Redeklarasi Cache:** Penempatan *decorator* `@st.cache_data` di dalam lingkup `with tab:` memaksa memori untuk mengompilasi ulang fungsi. **Solusi:** Semua *decorator cache* dipindahkan ke area teratas (Global Scope) skrip.

---

## 3. Penyelarasan Aset Visual, Penamaan, dan Kuantifikasi Heatmap
Untuk menjaga profesionalisme dan standar repositori *Data Science* yang bersih, seluruh *assets* visual dan *file gzip* ditata ulang agar nomenklaturnya jelas bagi siapapun yang membaca.

- **Pembersihan Nama File:** Nomenklatur ambigu `*_rainy.*` diganti secara universal menjadi `*_noAugmentation.*`. Sementara itu, label `*_emnist.*` distandarisasi menjadi huruf kapital `*_EMNIST.*`.
- **Kuantifikasi Intensitas (Heatmap Bukti):** Dashboard kini menampilkan narasi matematis yang konkret dari perbandingan piksel pasien disleksia *Severity 1* vs *Severity 6*:
  - Rata-rata selisih ketebalan goresan (*ink intensity*) untuk dataset No Augmentation adalah **~16.57**.
  - Rata-rata untuk dataset EMNIST adalah **~14.00**.
  - Angka ini memvalidasi hipotesis bisnis kita bahwa *"Tingkat keparahan (Severity) berbanding lurus dengan ketebalan goresan akibat perilaku mengulang/mencoreng (Reversal/Corrected)."*
- **Eksplorasi Luring (Gzip):** File `csv_metadata/dyslexialens_test_EMNIST.csv.gz` terbaru (~23.1 MB) berhasil di- *generate*. File pipih ini memuat 94.671 matriks piksel *test set* yang menjadi tulang punggung dari fitur "Analisis Piksel Interaktif" di Dashboard Tab 4. Berkas ini juga telah dirapikan ke dalam folder `csv_metadata`.

---

## 4. Operasi Penyembuhan Dashboard Streamlit (Crash Fix — Gelombang 2)
**Konteks:** Setelah perbaikan Gelombang 1 berhasil menghilangkan crash saat pindah tab, ditemukan bahwa **Tab 4 (Viewer Compressed CSV)** masih crash secara konsisten ketika pengguna mengganti filter kelas dari *"Normal (0)"* ke *"Dyslexia (1)"*. Kelas Normal tetap berfungsi normal, tetapi kelas Disleksia selalu memicu *"Oh no. Error running app."* — baik pada dataset `noAugmentation` maupun `EMNIST`.

**Akar Masalah yang Ditemukan:**
1. **Positional Slicing Fragile (`row.values[1:]`):** Kode lama mengambil piksel dari setiap baris menggunakan *slicing* posisi (`row.values[1:]`). Pendekatan ini rentan gagal jika urutan kolom DataFrame berubah saat Streamlit melakukan *rerun*, karena Streamlit tidak menjamin urutan kolom setelah *filtering* dan *sampling* berulang kali di sesi yang sama.
   - **Solusi:** Diganti dengan `row.drop('label').values.astype(np.float64)` — secara eksplisit membuang kolom `label` berdasarkan nama (bukan posisi), lalu *cast* ke `float64` untuk menjamin konsistensi tipe data saat `.reshape(28, 28)`.

2. **Memory Bloat pada Subset Besar:** Saat kelas Disleksia dipilih, subset bisa mencapai **37.166 baris** (EMNIST) atau **24.159 baris** (noAugmentation). Operasi `.sample(500)` → `.iloc[:, 1:].values` → `.flatten()` pada jumlah sebesar ini menghasilkan array NumPy raksasa (500 × 784 = 392.000 elemen) yang menumpuk di memori karena tidak pernah di-*deallocate*.
   - **Solusi:** Jumlah sampel diturunkan dari 500 menjadi **300**, dan seluruh array besar (`pixel_data`, `flat_pixels`, `stroke_pixels`, `avg_image`) secara eksplisit dihapus menggunakan `del` setelah selesai digunakan.

3. **Tidak Ada Error Boundary:** Seluruh blok rendering Tab 4 tidak dibungkus dalam penanganan *exception*, sehingga error sekecil apapun (tipe data, reshape, atau memory) langsung menjatuhkan seluruh aplikasi Streamlit.
   - **Solusi:** Seluruh logika rendering (sampling gambar, Ghost Image, Histogram) kini dibungkus dalam blok `try/except` yang menampilkan pesan error informatif (`st.error(...)`) alih-alih mematikan aplikasi.

---

## 📁 Hasil Akhir & Berkas Kunci
- `notebooks/Dyslexia_EMNIST.ipynb`: Pipeline data wrangling EMNIST end-to-end yang baru dan seimbang.
- `app.py`: Dashboard yang sudah stabil (2 gelombang perbaikan crash), referensi file lama dihapus.
- `csv_metadata/dyslexialens_test_EMNIST.csv.gz` & `csv_metadata/dyslexialens_test_noAugmentation.csv.gz`: Dataset *compressed* untuk eksplorasi piksel di dashboard secara efisien.
- `assets/*`: Visualisasi EDA (distribusi kelas, severity, heatmap) untuk EMNIST maupun versi No Augmentation, dengan format penamaan yang telah disempurnakan.

---

## 🚀 Rencana / Rekomendasi Aksi Lanjut (Next Action)
Dengan stabilnya Dashboard dan kokohnya integritas *Dataset EMNIST*, maka **Tugas Pokok Data Scientist dalam mempersiapkan data telah mencapai garis finis absolut (100% Selesai).** 

Fase Data Wrangling & EDA resmi ditutup. 

Langkah selanjutnya adalah penyerahan tongkat estafet kepada tim **Artificial Intelligence (AI Engineer)** untuk:
1. Mengimpor file zip `Dataset_Gambo_EMNIST.zip` yang telah dikompresi oleh sistem.
2. Memulai rancang bangun arsitektur **Convolutional Neural Network (CNN)**.
3. Melakukan eksperimen *Hyperparameter Tuning* dengan memantau pergerakan metrik *F1-Score* dan *Recall* untuk mengurangi laju *False Negative*.
