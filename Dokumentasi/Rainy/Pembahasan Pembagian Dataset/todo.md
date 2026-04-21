# TODO & Rencana Strategi: Fitur Scanning & Translation Berbasis Grid

## ⚠️ Masalah Utama
Kita ingin sistem yang bisa membaca tulisan penderita disleksia (A, B, C...) lalu menerjemahkannya.
Tetapi, **data Disleksia kita (~120.000 gambar) HANYA berisi label skor (1-6)**. Kita sama sekali **TIDAK TAHU** mana gambar huruf 'A', mana huruf 'B', dst. 
Melakukan pelabelan (labeling) manual huruf A-Z untuk ratusan ribu gambar sangat tidak mungkin dalam sisa waktu Capstone. Apalagi, model AI *Optical Character Recognition* (OCR) biasa akan buta/error jika disuruh membaca tulisan disleksia yang bentuknya jungkir balik (Reversal).

## 💡 Solusi Elegan: Deterministic Grid Approach (CV Tanpa Deep Learning Tambahan)
Ide kamu tentang **"pengguna ngeprint kertas kotak"** itu **sangat brilian dan merupakan solusi TEPAT**! Pendekatan ini dinamakan *Deterministic Template Matching*.

Dengan sistem ini, **AI (Deep Learning) kita tidak perlu tahu huruf apa itu!** AI hanya fokus mendeteksi, *"Apakah tulisan ini Disleksia atau Normal? Berapa tingkat keparahannya?"* 

Sedangkan yang bertugas mencari tahu *"Ini huruf apa?"* adalah **Desain Template Kertas dan OpenCV**, bukan Deep Learning.

---

### 🔄 Alur Kerja Sistem (Bagaimana ini bekerja)

1. **Pembuatan Kertas Template (UI/UX)**
   Pengguna mengunduh (print) template spesifik dari web kita. Kotak-kotak di kertas sudah ditentukan urutannya mutlak.
   - Kotak baris 1, kolom 1 ➔ **Pasti tempat menulis huruf 'A'**
   - Kotak baris 1, kolom 2 ➔ **Pasti tempat menulis huruf 'B'**

2. **OpenCV Auto-Crop (Backend/CV)**
   Saat kertas diunggah, Backend menjalankan **OpenCV (Python)** untuk mencari kontur (garis kotak) dan memotong-motong kertas menjadi kotak-kotak kecil (`28x28` pixel). Karena urutannya tetap, *Backend secara otomatis tahu bahwa crop pertama adalah huruf 'A'*.

3. **Inference & "Terjemahan" (AI Pipeline)**
   - Backend melempar *Crop Kotak ke-1* ke Model CNN DyslexiaLens.
   - Model CNN mengevaluasi: *"Oh, ini indikasi Disleksia, Severity Score 5!"*
   - Backend menggabungkan informasi: *"Kotak ke-1 (yaitu huruf 'A') terindikasi Disleksia tingkat 5."*
   - Di UI Frontend, sistem menampilkan: **"Terjemahan Huruf Berikut: 'A'"**. (Karena kita sudah tahu itu kotak untuk 'A')

---

## ✅ Action Items (To-Do List untuk Tim)

### A. Untuk Data Scientist (Kamu)
- [x] **Jangan lakukan relabeling abjad!** Evaluasi menunjukkan hal ini tidak diperlukan jika menggunakan template kertas grid.
- [ ] Buat **Visualisasi Peragaan (Mockup)** di Streamlit Dashboard. Tunjukkan skenario di mana pengguna memasukkan foto "Grid/Kotak-kotak", seolah-olah OpenCV sudah memotongnya jadi beberapa gambar, lalu diteruskan ke Model.
- [ ] Dokumentasikan alur OpenCV + CNN ini di dalam dokumentasi akhir agar Reviewer Dicoding paham bahwa arsitekturnya efisien dan pintar.

### B. Untuk Backend & AI Engineer
- [ ] Buat endpoint API yang menerima upload gambar 1 halaman penuh (foto A4).
- [ ] Tulis skrip Python dengan `cv2` (OpenCV):
  - Mengurutkan kotak dari Kiri-Atas ke Kanan-Bawah.
- [ ] Kirim hasil potongan kotak secara batch ke model CNN DyslexiaLens (`model.predict()`).

### C. Untuk Fullstack Developer (Frontend / UI/UX)
- [ ] Desain file PDF Kertas Grid (seperti Lembar Jawab Komputer) bergaris tebal.
- [ ] Pasang margin/sensor hitam di ujung kertas (*fiducial markers*) agar OpenCV mudah melakukan luruskan (*warp perspective*).
- [ ] UI Hasil: Tampilkan tabel urutan kotak dan terjemahan komputer, serta skor disleksianya.

---

# 🚀 Diskusi Fitur: Gabungan "Early Screening" & "Translasi Kata"

Kamu menyinggung ide yang luar biasa soal menyatukan abjad / translasi kata dari kotak-kotak tersebut dengan menggunakan **KERTAS YANG SAMA**. Mari bedah konsep yang sangat mungkin digunakan:

### Konsep Kertas: "The DyslexiaLens Smart Grid"
Bayangkan kita punya satu jenis kertas (*Smart Grid*), namun memiliki **dua Fungsi/Mode yang berbeda di dalam Web**.

#### Mode 1: Early Screening (Assessment Mode)
*(Sesuai dengan idemu: Baris 1 kolom 1-9 isinya khusus Latihan A, Baris 2 untuk B, dst.)*
- **Skenario:** Pengguna (anak) diminta fokus latihan kelenturan menulis abjad berulang-ulang untuk dites keakuratannya. 
- **Tugas Backend:** Murni *Deterministic* (sudah tahu pasti Baris 1 kolom 2 itu huruf A). Tidak perlu AI pengenal tulisan.
- **Tugas AI DyslexiaLens:** Hanya mengecek *"Ini disleksia atau bukan? Severity berapa?"*

#### Mode 2: Free-Writing Translation (Assistive Mode)
*(Hanya kotak-kotak grid kosong tanpa ada arahan harus nulis huruf apa. Dibiarkan bebas merangkai kata).*
- **Skenario:** Pengguna ingin menulis kata sembarang, misalnya ingin menulis "B U K U", dengan menempatkan setiap abjad pada tiap-tiap kotak kosong.
- **Tugas Backend:** Tentu *Deterministic* GAGAL dipakai di sini, karena komputer tidak tahu user menulis abjad apa di kotak 1.
- **Solusi untuk AI Engineer (Sangat Penting):** Membutuhkan **TANDEM DUA MODEL**.
  1.  **Model 1 (Pihak Ketiga / OCR Bawaan):** Model pengenal abjad dari image (seperti Model EMNIST, *Tesseract OCR*, atau Google Vision API) untuk bertugas menebak *"Oh ini huruf B"*.
  2.  **Model 2 (DyslexiaLens):** Bersamaan dengan itu memprediksi *"Bentuk huruf ini memiliki severity 5"*.
- **Output Frontend (Translasi):** Menyusun Array hasil dari prediksi Model 1 menjadi kalimat komputer `[B, U, K, U]`, sambil menghighlight warna merah muda pada huruf "K" karena Model 2 mendeteksi Severity yang besar (*reversal*/terbalik).

### 🤔 Saran Pembawaan Ide ke Tim:
Katakan kepada tim bahwa ide translasi per-kotak (merangkai kata) **SANGAT MASUK AKAL dan INOVATIF**, tetapi **pastikan AI Engineer sadar** bahwa untuk mode kedua (*Free-writing*), mereka harus mencari API OCR (Pihak ketiga atau model ringan *pre-trained*) tambahan sebagai Model Penerjemahnya. 
Dataset 120.000 (DyslexiaLens) murni hanya bertugas sebagai **Reviewer Pola (Mendeteksi Kepelikan Tulisan Tangan)** karena tidak punya label kelas A-Z pada sampel abnormalnya.

---

# 🚀 Diskusi Fitur: Strategi Menangani Imbalance (Severity 1-6 vs Binary)

Kekhawatiran temanmu **100% sangat valid**. Ini adalah masalah klasik di *Machine Learning*: *"Jika kita memaksakan keseimbangan kelas sub-kategori (severity), kita malah merusak keseimbangan kelas utama (Normal vs Disleksia)!"*

Terkait pergeseran ide untuk **menyatukan saja skor 1-6 menjadi 1 kelas (Hanya 'Disleksia')**, menurutku itu **IDE YANG SANGAT CEMERLANG UNTUK CAPSTONE INI**. Berikut perbandingan jika diskusi ini dibawa ke tim:

### Opsi 1: Menyatukan Severity jadi 1 Kelas "Disleksia" (⭐ SANGAT DIREKOMENDASIKAN)
- **Konsep:** Kita buang jauh-jauh skor kepelikan 1-6. Model HANYA melakukan *Binary Classification* (Normal vs Disleksia).
- **Keuntungan:**
  1. **TIDAK PERLU AUGMENTASI FISIK SAMA SEKALI!** Kelas Disleksia (~121k) lebih banyak dari Normal (~58k). Kita tinggal melakukan teknik **Undersampling** (mengambil acak 58k dari 121k gambar Disleksia). Hasil akhirnya dataset akan seimbang sampurna: **58k Normal vs 58k Disleksia (1:1)**.
  2. Training model CNN akan berkali-kali lipat lebih cepat karena dataset hanya setengahnya dan seimbang.
- **TAPI BAGAIMANA CARA MENGUKUR KEPARAHAN (LEVEL)?** 
  - AI Engineer bisa menggunakan hasil **Probability / Confidence Score** dari prediksi model.
  - Jika Confidence *Disleksia* = **98%** ➔ Level Parah (setara skor 6 dulunya).
  - Jika Confidence *Disleksia* = **55%** ➔ Level Ringan (setara skor 1 dulunya).
  - Ini jauh lebih elegan dan sesuai dengan poin di *Project Plan* yang menjanjikan "Confidence Score".

### Opsi 2: Tetap pakai Severity 1-6, dan Mengaugmentasi Normal (❌ TIDAK DISARANKAN)
- **Konsep:** Mengaugmentasi kelas Normal dari 58k menjadi ~150k agar bisa mengimbangi kelas Disleksia yang membengkak karena augmentasi skor 2-5.
- **Kelemahan Fatal:**
  1. Dataset kamu akan membengkak total menjadi **300.000+ gambar**. Komputer dan Google Colab gratisan akan *crashing* / kehabisan RAM saat training CNN yang sangat lama (bisa memakan waktu berminggu-minggu).
  2. Mengaugmentasi kelas "Normal" (memiring-miringkan tulisan Normal) justru menipu model, karena tulisan Normal yang dimiringkan bisa dianggap model *sebagai indikasi goresan Disleksia*.
  3. Rentan sekali menyebabkan masalah *Overfitting*.

### 📝 Action Items Baru (Jika Mengambil Opsi 1):
- [ ] Sepakati dulu dengan tim apakah merelakan target kelas `severity_score` 1-6 itu boleh dilakukan.
- [ ] Ubah Data Preprocessing notebook di bagian akhir dengan menambahkan kodingan *Undersampling*, yaitu menyeimbangkan jumlah baris Disleksia target_class 1 agar persis jumlahnya dengan jumlah target_class 0 (Normal).
- [ ] Setelah *Undersampling*, Train / Test Split akan berjalan mulus dan murni. Dataset akhirnya akan lebih ramping dan garansi lolos uji validasi!