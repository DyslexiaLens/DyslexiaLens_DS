# Rencana Tindakan & Gerakan Lanjutan Tim Data Scientist (DyslexiaLens)

Berdasarkan *Checklist* proyek dan evaluasi progres saat ini, sebagian besar *Main Quest* (seperti Data Wrangling dasar dan pembuatan Dashboard Streamlit) telah diselesaikan. Dokumen ini merumuskan **gerakan-gerakan lanjutan** (baik eksperimen baru maupun *Side Quest*) yang **belum dilakukan** dan bisa dieksekusi selanjutnya untuk memaksimalkan performa dan nilai tambah proyek.

---

### 1. Augmentasi Rotasi Skala Kecil (±10 Derajat)
**Rencana Eksekusi:** Menambahkan volume dataset dengan memperbanyak data (*Offline Augmentation*) murni melalui rotasi gambar secara dinamis sebesar **10 derajat ke kanan** dan **-10 derajat ke kiri**. 
**Tujuan:** Mencapai rasio target kelas yang ideal tanpa merusak makna struktural huruf (tetap menghindari *horizontal flip* yang bisa mengubah 'b' menjadi 'd'), sehingga AI dapat mengenali pola tulisan anak disleksia yang seringkali miring.

### 2. Eksperimen Pelabelan Abjad dari Skor Keparahan
**Rencana Eksekusi:** Mencoba melakukan pelabelan ulang (*re-labeling*) pada data gambar yang sebelumnya hanya dikategorikan berdasarkan *Severity Score* (skor keparahan disleksia) menjadi penamaan label berabjad spesifik (A-Z).
**Tujuan:** Membangun set data eksperimental untuk menguji apakah model AI nantinya mampu mengenali huruf spesifik secara bersamaan saat mengukur tingkat keparahannya (menjembatani batas fungsional antara diagnostik penyakit dan sistem OCR).

### 3. Eksperimen Feature Engineering (Side Quest)
**Rencana Eksekusi:** Melakukan rekayasa fitur matematis untuk menghasilkan variabel turunan dari data matriks piksel gambar 28x28.
**Tujuan:** Alih-alih hanya memberi AI gambar mentah, Data Scientist akan mengekstrak fitur seperti **kepadatan piksel hitam-putih**, **centroid goresan**, atau **rasio ketebalan tinta per kuadran**. Fitur tambahan ini dapat memperkaya informasi tabular yang mungkin meningkatkan kepekaan model terhadap goresan halus.

### 4. Pelaksanaan A/B/C Testing Dataset (Side Quest)
**Rencana Eksekusi:** Merancang dan mengeksekusi metode pengujian A/B/C (*Multivariate Testing*) menggunakan Python murni di tahap analisis evaluasi tanpa melangkahi wewenang koding AI Engineer.
**Tujuan:** Membandingkan secara saintifik manakah dari 3 versi dataset yang menghasilkan performa AI terbaik:
- **Skenario A (Baseline):** Model yang dilatih dengan Dataset Original Gambo.
- **Skenario B (EMNIST):** Model yang dilatih dengan Dataset Gambo + EMNIST.
- **Skenario C (Augmented):** Model yang dilatih dengan Dataset Gambo + Rotasi ±10 Derajat.

**SOP Eksekusi Lintas-Peran (Batas Data Scientist vs AI Engineer):**
1. **Perancangan Ujian (Ranah Data Scientist):** DS mengunci *Test Set* yang sama persis (Standar Emas) untuk diujikan pada ketiga model. DS menetapkan metrik keberhasilan utama (misalnya: *Recall* harus naik untuk mengurangi *False Negative*).
2. **Tahap Training Model (Ranah AI Engineer):** AI Engineer bertugas merakit arsitektur CNN di TensorFlow dan melatih Model A, Model B, dan Model C. DS **tidak** perlu ikut campur urusan *Hyperparameter Tuning* (*learning rate*, *epochs*, dsb).
3. **Penyerahan Hasil Tebakan (Kewajiban AI Engineer):** Setelah *training* selesai, AI Engineer tidak membuat kesimpulan sendiri. Tugas mereka adalah menyerahkan tebakan mentah (*inference*) model kepada DS dalam satu tabel CSV (Berisi 4 kolom: `Label_Asli`, `Pred_Model_A`, `Pred_Model_B`, `Pred_Model_C`).
4. **Analisis Statistik A/B/C (Ranah Data Scientist):** Menggunakan file CSV dari AI Engineer, DS melakukan analisis Uji Hipotesis. Karena membandingkan 3 model sekaligus, DS menggunakan **Uji Cochran's Q** (*Cochran's Q Test* via `statsmodels` Python) untuk melihat apakah ada perbedaan signifikan di antara ketiganya. Jika signifikan, dilanjutkan dengan **Uji McNemar** untuk membandingkan sang pemenang (misal Model C) dengan *baseline* (Model A). DS lalu memvisualisasikannya di Dashboard Streamlit.

### 5. Deployment Dashboard ke Cloud (Side Quest)
**Rencana Eksekusi:** Mempublikasikan dashboard `app.py` yang saat ini hanya berjalan di *localhost* (komputer lokal) ke layanan *hosting* awan.
**Tujuan:** Menggunakan **Streamlit Community Cloud** untuk meng- *hosting* dashboard secara publik. Ini akan mempermudah *stakeholder*, dosen, atau penilai Dicoding untuk berinteraksi langsung dengan *insight* EDA tanpa perlu melakukan instalasi Python di komputer mereka.

### 6. Penyusunan Laporan Teknis Komprehensif PDF (Side Quest)
**Rencana Eksekusi:** Merangkum seluruh perjalanan data.
**Tujuan:** Menyusun laporan formal berformat PDF yang mendokumentasikan proyek dari hulu ke hilir (mulai dari tahap *Problem Discovery*, proses pembersihan data, penemuan pola via EDA, hingga rekomendasi arsitektur ke tim AI). Hal ini merupakan syarat krusial untuk meraih nilai maksimal (akumulasi poin tambahan) pada evaluasi Capstone Dicoding.
