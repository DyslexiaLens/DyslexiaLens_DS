# Laporan Eksekusi Rencana Tindakan & Gerakan Lanjutan

Dokumen ini melacak eksekusi dari rencana yang disusun sebelumnya pada dokumen `Peran_dan_Tindakan_Data_Scientist.md`.

---

### ❌ 1. Augmentasi Rotasi Skala Kecil (±10 Derajat)
**Status:** Dibatalkan
**Alasan:** Setelah dievaluasi, penambahan data melalui augmentasi rotasi skala kecil dirasa tidak memberikan variasi yang cukup bagus dan signifikan. Daripada melakukan rotasi, diputuskan bahwa mengambil data eksternal dari EMNIST atau **tidak menambahkan data augmentasi sama sekali** akan menghasilkan kualitas model yang lebih baik dan menjaga kealamian data.

### ❌ 2. Eksperimen Pelabelan Abjad dari Skor Keparahan
**Status:** Dibatalkan
**Alasan:** Sangat tidak memungkinkan untuk dilakukan. Keterbatasan teknologi saat ini menyulitkan otomatisasi proses pelabelan abjad pada tulisan anak penderita disleksia. Eksperimen pelabelan manual pun sudah dicoba, namun dibatalkan karena bentuk tulisan dan abjad pada keparahan tinggi sudah sangat tidak beraturan sehingga membingungkan untuk diidentifikasi secara manual sekalipun manusia.

---

### ✅ 3. Eksperimen Feature Engineering
**Status:** Selesai
**Tindakan:** Eksperimen ini berhasil dieksekusi dengan sangat baik. Skrip telah berhasil mengekstrak 5 fitur turunan matematis dari matriks piksel gambar. Berikut adalah penjelasan untuk masing-masing fitur yang diekstrak:

| Fitur | Deskripsi |
|---|---|
| `ink_density` | Persentase piksel hitam (tinta) terhadap total area gambar (784 piksel). Fitur ini berguna mendeteksi penebalan tulisan akibat coretan berulang (*over-tracing*) yang sering terjadi pada penderita disleksia. Tulisan yang banyak dicoreng akan memiliki kepadatan tinta lebih tinggi. |
| `center_of_mass_x` | Posisi titik tengah goresan pada sumbu horizontal (0-27). Membantu mendeteksi distorsi orientasi; huruf yang miring, asimetris, atau menyimpang jauh ke kiri/kanan akan memiliki *centroid* yang melenceng. |
| `center_of_mass_y` | Posisi titik tengah goresan pada sumbu vertikal (0-27). Berguna untuk mendeteksi masalah spasi dan letak vertikal, seperti tulisan yang "melayang" terlalu tinggi atau "anjlok" secara tidak wajar melewati garis bayangan. |
| `bounding_box_ratio` | Rasio tinggi/lebar area goresan setelah *whitespace* luar dipangkas. Sangat efektif untuk mengidentifikasi distorsi proporsi huruf (misal: huruf 'o' menjadi sangat pipih). Huruf yang direvisi berulang kali cenderung melebar (rasio < 1). |
| `stroke_transitions` | Rata-rata frekuensi perubahan warna (putih ↔ hitam) per baris horizontal. Angka transisi yang tinggi mengindikasikan goresan yang terputus-putus, berantakan, atau bergetar (tremor) akibat kesulitan motorik halus penderita. |

---

### 🔄 4. Pelaksanaan A/B Testing Dataset
**Status:** Masih dalam proses (In Progress) — Terdapat dua opsi *pipeline* eksekusi (A dan B) sesuai kesiapan tim AI Engineer.

#### Dua Jalur Pengujian
Sesuai rancangan pada `DyslexiaLens_AB_Testing_Plan.md`, pengujian dipisah menjadi dua opsi:
- **Opsi A (Fokus Integritas Data):** Dieksekusi **mandiri oleh Data Scientist** menggunakan *Mann-Whitney U Test*.
- **Opsi B (Fokus Performa Model):** Dieksekusi secara **kolaboratif** jika AI Engineer sudah berhasil melatih dua model (*baseline* vs EMNIST). Menguji akurasi menggunakan *McNemar Test*.

**Langkah Terdekat:** Mengeksekusi **Opsi A** (Uji Mann-Whitney) pada *Jupyter Notebook* karena datanya sudah siap 100%.

#### Rincian Eksekusi Opsi A (Mandiri oleh DS)
Yang dibandingkan pada langkah ini adalah **karakteristik statistik dua dataset** yang sudah tersedia.

| | Dataset A (Kontrol) | Dataset B (Perlakuan) |
|---|---|---|
| **File** | `master_dataset_final_balanced_rill_featured.csv` | `master_dataset_emnist_balanced_final_featured.csv` |
| **Sumber** | Gambo saja (~180k) | Gambo + EMNIST (~273k) |

**Perumusan Hipotesis (Opsi A)**
- **H₀:** Tidak ada perbedaan signifikan pada distribusi 6 fitur XAI antara Dataset A dan Dataset B.
- **H₁:** Ada perbedaan signifikan — augmentasi EMNIST mengubah karakteristik data secara nyata.
- **Alpha (α):** 0.05

**Metrik yang Dibandingkan**
Enam fitur XAI yang sudah diekstrak di tahap Feature Engineering:
`ink_density`, `center_of_mass_x`, `center_of_mass_y`,
`bounding_box_ratio`, `stroke_transitions`, `horizontal_symmetry`

**Uji Statistik: Mann-Whitney U Test (Non-Parametrik)**
Dipilih karena distribusi fitur gambar tidak bisa diasumsikan normal. Membandingkan dua grup independen (Dataset A vs Dataset B) untuk setiap fitur.

#### SOP Eksekusi A/B Testing
1. Load kedua CSV featured ke notebook
2. Jalankan Mann-Whitney U Test (Opsi A) untuk masing-masing dari 6 fitur
3. Buat tabel ringkasan P-value per fitur
4. Visualisasikan perbandingan distribusi (boxplot / violin plot)
5. Tulis interpretasi & rekomendasi untuk Technical Report
6. Tampilkan di Dashboard Streamlit (tab A/B Testing)
7. *(Cadangan)* Jika model AI sudah siap sebelum deadline, jalankan *McNemar Test* (Opsi B).

> 📄 Detail metodologi, kode Python, dan aturan keputusan lengkap tersedia di:
> `Dokumentasi/Referensi/Rainy/DyslexiaLens_AB_Testing_Plan.md`

### ✅ 5. Deployment Dashboard ke Cloud
**Status:** Selesai — Dashboard berhasil dideploy ke Streamlit Cloud
