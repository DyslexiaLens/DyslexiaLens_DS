# Checkpoint 11 — Final Closure: Dashboard Polish & Project Handover Complete
**Tanggal:** 31 Mei 2026  
**Role:** Data Scientist & Software Engineer  
**Status Proyek:** `✅ FINAL CLOSED — DELIVERED`

---

## 🎉 Selamat! Proyek Capstone DyslexiaLens Resmi Selesai

Ini adalah checkpoint terakhir dari perjalanan panjang yang luar biasa. Setelah melewati 10 sesi intensif sebelumnya — dari audit dataset mentah, preprocessing, feature engineering, A/B Testing, hingga penyusunan laporan teknis komprehensif — sesi penutup ini berfokus pada satu hal yang tidak kalah penting: **keindahan dan keterbacaan antarmuka dashboard** sebagai wajah terdepan seluruh pekerjaan riset yang telah dilakukan.

---

## 🛠️ Pekerjaan yang Diselesaikan di Sesi Ini

### 1. Perbaikan Visual: Rata-Rata Goresan (Ghost Image)
**Konteks:** Visualisasi *Ghost Image* dan histogram *Distribusi Ketebalan Tinta* di Tab Viewer tampil terlalu besar sehingga merusak proporsi layout secara keseluruhan.  
**Tindakan:**
- Memperkecil `figsize` matplotlib untuk kedua grafik secara proporsional.
- Bereksperimen dengan rendering *Base64 PNG* vs `st.pyplot()` native, kemudian memilih `st.pyplot()` agar teks label sumbu tetap tajam dan terbaca (*vector-crisp*).
- Menggunakan `st.columns([1, 1.2, 1])` dan `st.columns([0.5, 3, 0.5])` untuk memaksa posisi grafik berada tepat di tengah kontainer.

### 2. Perbaikan Visual: 10 Sampel Acak
**Konteks:** Deretan 10 gambar sampel piksel tampil dalam satu baris penuh yang terlalu mepet ke kiri dan terasa tidak proporsional.  
**Tindakan:**
- Mengubah susunan dari `1×10` menjadi **`2×5` (2 baris × 5 kolom)** menggunakan `st.columns(5)` dengan `cols[i % 5]`.
- Membungkus grid tersebut di dalam `st.columns([1, 4, 1])` sebagai kontainer centering agar grid berada di tengah halaman secara simetris.
- Mempertahankan ukuran `figsize=(0.4, 0.4)` agar gambar tetap kecil namun tetap *crisp*.

### 3. Perbaikan: Status Saat Ini (Imbalance) Card
**Konteks:** Bullet list pada kartu *"Status Saat Ini (Imbalance)"* tampil miring ke kiri akibat *default padding* elemen `<ul>` HTML, sehingga teks tidak benar-benar terpusat meski kontainernya sudah diatur `text-align: center`.  
**Tindakan:**
- Mengganti `<ul>/<li>` menjadi elemen `<div>` dengan simbol `•` manual.
- Hasilnya teks sekarang benar-benar sejajar di tengah tanpa indentasi paksa dari browser.

### 4. Clean Code: Modularisasi & Refactoring Final
**Konteks:** Kode `Dashboard.py` semula dipenuhi ratusan baris HTML mentah yang berulang, membuat file sulit dibaca dan dimaintain.  
**Tindakan yang sudah dilakukan di sesi-sesi sebelumnya dan disempurnakan di sesi ini:**
- Seluruh konfigurasi CSS dipindahkan ke `Assets/Styles.css` dan dimuat via `load_custom_css()`.
- Fungsi `render_section_header(subtitle, title, description)` menggantikan 6 blok HTML berulang di setiap Tab.
- Dictionary `DATASET_OPTIONS` menggantikan kondisi `if/else` berulang untuk memilih path CSV dan folder aset.
- `get_dataset_assets(choice)` sebagai *single point of access* untuk konfigurasi dataset.
- Seluruh *Section Header* di Tab 1–6 menggunakan fungsi yang seragam — menerapkan prinsip **DRY** (*Don't Repeat Yourself*) dan **Separation of Concerns**.

---

## 🏆 Rekap Seluruh Pencapaian Proyek (Checkpoint 1–11)

| Fase | Pencapaian |
|---|---|
| **CP 1–2** | Audit integritas dataset Gambo, deteksi label noise & duplikasi |
| **CP 3–4** | Pipeline preprocessing: binarisasi, normalisasi, resize 28×28 |
| **CP 5–6** | Feature Engineering 6 Fitur XAI (Kepadatan Tinta, Transisi Garis, dll) |
| **CP 7** | Stratified Split 70/15/15 & validasi proporsi antar-split |
| **CP 8** | Augmentasi EMNIST + Fair Pruning → rasio kelas 1:1 |
| **CP 9** | Exploratory Data Analysis (EDA) menyeluruh — visualisasi KDE, Boxplot, Heatmap |
| **CP 10** | A/B Testing: Mann-Whitney U + Cohen's d → terbukti aman secara klinis |
| **CP 10** | Laporan Teknis Final 51 Halaman + SLA Handover ke tim AI Engineer |
| **CP 11** | Dashboard polish, clean code, UI centering, final delivery ✅ |

---

## 🧩 Arsitektur Repositori Akhir

```
Dataset Disleksia/
├── Dashboard.py            # Pusat kendali dashboard Streamlit
├── Assets/
│   ├── Styles.css          # Semua CSS kustom (dark theme, navbar, cards)
│   ├── noAugmentation/     # Visualisasi pre-augmentasi (PNG)
│   ├── EMNIST/             # Visualisasi post-augmentasi (PNG)
│   └── Logo DyslexiaLens.png
├── Data/
│   ├── Dataset_Dyslexia_NoAugmentation_FeatureEngineering.csv
│   ├── Dataset_Dyslexia_EMNIST_FeatureEngineering.csv
│   ├── dyslexialens_test_noAugmentation.csv.gz
│   └── dyslexialens_test_EMNIST.csv.gz
└── Dokumentasi/
    └── Rainy/
        ├── Checkpoint/     # CP 1–11 (file ini)
        ├── Final.md        # Laporan Teknis Master
        └── Data Scientist Checklist.md
```

---

## 💡 Catatan Teknis untuk Masa Depan

> **Bagi tim AI Engineer yang menerima handover ini:**
> - Dataset final ada di `Data/` dalam dua varian: *Original* dan *Augmented*.
> - Seluruh justifikasi teknis mengapa augmentasi aman ada di Tab *A/B Testing* dashboard dan di `Final.md` Bab 5.
> - **Jangan** gunakan augmentasi rotasi/flip spasial — ini akan merusak sinyal Reversal (huruf terbalik) yang menjadi fitur kritis deteksi disleksia.
> - Model **WAJIB** dilatih dengan metrik *Weighted F1-Score*, bukan *Accuracy*, karena target akhir adalah deteksi klinis yang adil terhadap kelas minoritas.

---

## 🌟 Refleksi Akhir

Dari sebuah folder berisi gambar-gambar tulisan tangan yang kacau balau, penuh *label noise*, *class imbalance*, dan tanpa dokumentasi apapun — kita berhasil membangunnya menjadi sebuah **pipeline data medis berstandar industri** yang:

- 🔬 **Saintifik:** Setiap keputusan dapat dibuktikan dengan uji statistik.
- 🧠 **Explainable:** Setiap prediksi model di masa depan dapat dijelaskan lewat 6 fitur XAI yang telah kita rancang.
- 🏥 **Klinis:** Dataset tidak mengandung *Domain Shift* yang berbahaya — sudah divalidasi via A/B Testing.
- 💻 **Maintainable:** Kode dashboard ditulis mengikuti prinsip *Clean Code* sehingga mudah dikembangkan lebih lanjut.
- 🎨 **Presentable:** Dashboard tampil profesional dan siap didemonstrasikan ke *Reviewer* maupun *Advisor*.

---

Fase **Data Science, Data Engineering, dan Dashboard Development** untuk proyek DyslexiaLens Capstone Semester 6 ini secara resmi dinyatakan:

> ## 🎓 `SELESAI. CLOSED. DELIVERED.`
> **Terima kasih telah berjuang tanpa menyerah dari awal hingga akhir. Ini bukan sekadar nilai — ini adalah karya. Semoga DyslexiaLens suatu hari bisa benar-benar membantu anak-anak yang membutuhkan. 🧠💙**
