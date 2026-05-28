## Progres Saat Ini (Status Data Science)

| Item | Status |
|---|---|
| Audit & Data Wrangling Dataset Gambo | ✅ Selesai |
| EDA & Visualisasi Explanatory (Heatmaps, KDE, Boxplot) | ✅ Selesai |
| Stratified Split (Train/Validation/Test, tanpa Data Leakage) | ✅ Selesai |
| Integrasi EMNIST + Fair Pruning Balancing | ✅ Selesai |
| Feature Engineering (6 Fitur XAI) | ✅ Selesai |
| Executive Dashboard Streamlit | ✅ Selesai |
| Deployment Dashboard ke Streamlit Cloud | ✅ Selesai |
| Handover Dataset ke AI Engineer (CSV + ZIP) | ✅ Selesai |
| A/B Testing (NoAugment vs EMNIST via Mann-Whitney & Cohen's d) | ✅ Selesai |
| Technical Report Komprehensif (SLA Handover) | ✅ Selesai |

---

## Analisis Revisi Pertanyaan (Internal Notes)

Berikut adalah alasan mengapa beberapa pertanyaan lama dari dokumen sebelumnya dihapus atau dilebur ke dalam format baru:

1. **Terkait A/B Testing (Pertanyaan lama #6, #7, #8):** 
   - *Faktanya:* Kita **sudah** mengeksekusi uji beda distribusi fitur. Kita menghadapi anomali *Large N Effect* (di mana *p-value* pasti < 0.05 karena datanya raksasa), dan kita berhasil menyelamatkan integritas eksperimen dengan membuktikan bahwa *Effect Size* (Cohen's d) bernilai *Negligible* (< 0.2).
   - *Tindakan:* Pertanyaan-pertanyaan kebingungan ("Bagaimana kalau gagal?", "Bagaimana narasinya?") dilebur menjadi satu pertanyaan validasi (Pertanyaan Baru #2) yang menegaskan bahwa kita **sudah tahu** cara menjawabnya (menggunakan perbandingan *Practical vs Statistical Significance*).
2. **Terkait Format Laporan & Pemilihan EMNIST (Pertanyaan lama #1 & #2):**
   - *Faktanya:* Kita telah memutuskan untuk tidak memakai *snippet code* pada Laporan Teknis demi menjaga format *Executive SLA Handover*. Kita juga memiliki argumen medis yang sangat kuat untuk menolak augmentasi sintesis (rotasi/flip mengubah makna huruf dan menciptakan *Label Noise* bagi pendeteksi disleksia).
   - *Tindakan:* Pertanyaan ini dilebur menjadi Pertanyaan Baru #1, bukan untuk meminta petunjuk cara mengerjakan, melainkan untuk memvalidasi bahwa strategi *bold* (berani) yang kita ambil ini dinilai tinggi oleh Dicoding.

---

## High-Value Questions for Advisor (Pasca-Penyelesaian Pipeline)

Berdasarkan *pipeline* Data Science yang telah sepenuhnya rampung, berikut adalah pertanyaan strategis untuk memastikan arah kami sejalan dengan standar maksimal penilaian Capstone:

### A. Validasi Laporan & Keputusan Klinis
1. **Laporan & Argumen Medis:** Laporan Teknis kami (*Final.md*) difokuskan penuh pada narasi klinis, justifikasi keputusan, dan SLA Handover (tanpa menyertakan *snippet code* algoritma). Kami juga menyertakan argumen medis untuk **menolak augmentasi rotasi** (karena memanipulasi rotasi sama dengan merusak orientasi huruf *Reversal*) dan memilih injeksi data EMNIST. Apakah pendekatan *Executive Report* tanpa kode dan argumen klinis penolakan augmentasi seperti ini sudah sesuai ekspektasi penilai tinggi?

### B. Validasi Metode A/B Testing
2. **Evaluasi *Effect Size*:** Untuk eksperimen A/B Testing, kami telah mengeksekusi uji beda distribusi fitur. Kami menemukan bahwa meskipun secara statistik berbeda (*p < 0.05* karena *Large N Effect* pada 150.000+ sampel), efek perubahannya ternyata berstatus **Negligible** (*Cohen's d < 0.2*). Kesimpulannya: augmentasi EMNIST terbukti aman secara klinis dan tidak merusak DNA gambar asli. Apakah narasi pembuktian "Practical vs Statistical Significance" yang kami susun ini sudah sangat cukup untuk memenuhi kriteria rubrik A/B Testing Dicoding?

### C. Kesiapan Explainable AI (XAI)
3. **Standar Fitur:** Kami telah mengekstrak 6 fitur matematis-geometri (*ink density*, *center_of_mass x & y*, *bounding box ratio*, *stroke transitions*, *horizontal symmetry*) sebagai landasan arsitektur *Explainable AI* (XAI). Apakah keenam fitur murni matematis ini sudah memadai untuk memenuhi standar rubrik penilaian transparansi AI di proyek ini?
4. **Metode Validasi Performa:** Kedepannya, bagaimana metode terbaik yang disarankan bagi tim AI Engineer untuk membuktikan secara empiris bahwa penambahan 6 fitur XAI ini benar-benar berhasil meningkatkan performa model akhir? (Misalnya, haruskah kami menggunakan *Ablation Study* atau *McNemar Test*?)

### D. Strategi AI Engineering Lanjutan
5. **Upscaling Ekstrem:** Rencananya, tim AI Engineer kami akan melakukan *upscale* ekstrem gambar dari resolusi 28x28 menjadi 224x224 (demi menggunakan arsitektur *pre-trained model* seperti VGG/ResNet). Apakah pendekatan ini dianggap *overkill* untuk gambar MNIST/Gambo yang sederhana, atau ini justru lumrah di industri?

### E. Evaluasi Kritis Penutup
6. **Common Mistakes:** Berdasarkan pengalaman Anda mengevaluasi capstone sebelumnya, apa saja kesalahan fatal (*common mistakes*) di tahap *Data Science* & *Data Engineering* yang paling sering menyebabkan kelompok mendapatkan pengurangan nilai besar?
7. **Kelemahan Kritis Proyek:** Dengan melihat status progres *pipeline* kami di atas, adakah "blind spot" atau area kelemahan *Data Science* yang dirasa paling kritis di proyek kami untuk segera kami perbaiki sebelum masa submisi final?

---

## Lampiran Tambahan: Skrip Presentasi A/B Testing (*Elevator Pitch*)

*(Gunakan skrip ini sebagai panduan narasi saat mempresentasikan atau menjelaskan apa fungsi utama dari notebook **AB_Testing.ipynb** ke Advisor tanpa harus terjebak menjelaskan baris kode satu per satu).*

> "Pak/Bu, di tahap Data Science ini, kami menghadapi isu **Class Imbalance** yang cukup parah (rasio 3.35 : 1). Untuk mengatasinya, kami memutuskan menolak teknik augmentasi spasial seperti rotasi (karena merotasi huruf itu sama dengan merusak diagnosis klinis *Reversal* disleksia), dan memilih untuk **menginjeksi dataset eksternal EMNIST** sebagai perwakilan kelas Normal.
>
> Namun, karena ini adalah proyek medis, kami tidak mau sembarangan mencampur data. Oleh karena itu, kami merancang **A/B Testing** khusus ini. Kami membandingkan distribusi 6 fitur matematis-geometris pada Dataset Asli (Grup A) versus Dataset Campuran EMNIST (Grup B).
> 
> Saat kami uji menggunakan *Mann-Whitney U Test*, kami menemukan fenomena **'Large N Effect'**. Karena sampel datanya ratusan ribu, perbedaan sekecil debu pun dianggap signifikan secara statistik (*p-value < 0.05*). 
> 
> Untuk membuktikan secara praktis bahwa augmentasi kami aman, kami memvalidasinya menggunakan metrik **Cohen's d (Effect Size)**. Hasilnya memuaskan: keenam fitur kami memiliki skor Cohen's d di bawah 0.2 (*Negligible*). Artinya, selisih atau perbedaan antara data asli dan data campuran itu sangat kecil sehingga bisa diabaikan.
> 
> **Kesimpulannya:** Notebook ini membuktikan secara empiris bahwa teknik injeksi EMNIST kami berhasil menyeimbangkan kelas menjadi 1:1, **tanpa merusak sedikitpun 'DNA' atau karakteristik klinis tulisan tangan asli penderita disleksia.**"
