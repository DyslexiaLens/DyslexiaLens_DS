# Diskusi Arsitektur: Paradoks OCR dan Sistem Translasi (DyslexiaLens)

Berdasarkan diskusi ide untuk menambahkan fitur **Scan & Translate Abjad**, muncul sebuah pertanyaan kritis dalam rekayasa data (*Data Engineering*): 
> *"Bisakah kita mengotomatisasi pelabelan A-Z untuk 121.000 data Disleksia menggunakan mesin OCR (Optical Character Recognition)? Karena hanya data Normal yang memiliki label A-Z."*

Dokumen ini merangkum analisis mengapa ide tersebut berbahaya (*Paradoks OCR*), dan merumuskan **DUA SOLUSI TERBAIK** yang realistis untuk dicapai dalam batas waktu *Capstone Project*.

---

## 🚫 Akar Masalah: "The OCR Paradox" (Paradoks OCR)

Secara insting, memberikan gambar tulisan anak ke mesin pembaca huruf (seperti *Tesseract OCR* atau *Google Vision*) terdengar sangat logis. Namun, bagi penderita disleksia/disgrafia, cara ini akan membunuh *dataset*-mu sendiri!

**Contoh Kasus:**
1. Anak *(Penderita disleksia/Reversal)* berniat menulis huruf **'b'**.
2. Karena ia penderita disleksia, tangannya malah menggambar bentuk huruf **'d'**.
3. Kamu *scan* gambar tulisan anak tersebut menggunakan skrip OCR otomatis.
4. Mesin OCR melihat bentuknya murni seperti 'd', lalu melabeli gambar tersebut sebagai label **'d'**.
5. Kamu menyimpan gambar itu di CSV dengan label 'd'.

**Akibat Fatal:** 
Kamu mendaftarkan gambar "usaha penulisan huruf 'b'" ke dalam folder kelas 'd'. Ketika AI buatanmu (*DyslexiaLens*) mencoba belajar, ia diajarkan kebohongan (informasi yang menyesatkan). Hal yang lebih buruk terjadi pada *Severity 6 (Corrected)*; karena bentuknya abstrak, mesin OCR akan *error* atau melabelinya sebagai simbol aneh (`@`, `#`, `?`).

> **Inti Paradoks:** Jika mesin OCR standar sudah bisa membawa penderita disleksia secara akurat, maka sistem DyslexiaLens ini tidak perlu pernah diciptakan!

---

## 💡 Solusi Arsitektur: Bagaimana Model Bisa "Translasi" Tanpa Melabeli Ulang Data?

Karena kamu **MURNI TIDAK BISA** melabeli ulang dataset secara otomatis menggunakan teknik OCR yang buta arah, berikut adalah pilihan arsitektur logis untuk divisimu:

### SOLUSI 1: "The Smart Grid Assessment" (Paling Cerdas, Realistis, & Termudah)
Ini adalah ide kertas kotak-kotak yang pernah kamu singgung sebelumnya.
- **Konsep:** Pengguna diwajibkan *print* template khusus. Di template itu sudah diinstruksikan anak tersebut harus nulis karakter apa di kotak tersebut. Misal, ada *Watermark* tipis huruf 'A' di Kotak Nomor 1 yang memintanya menebalkan (atau instruksi "Tulis A di sini").
- **Tugas Backend/Fullstack:** Memotong gambar menggunakan *OpenCV*. Komputer **TIDAK PERLU BERTANYA** "Ini huruf apa?", karena dari indeks nomor letak kotak tersebut di-crop, aplikasi (Backend) **sudah tahu pasti** itu adalah tempat menulis huruf 'A'.
- **Tugas AI Engineer (DyslexiaLens):** Mengukur *Confidence Score* dan menentukan seberapa parah tingkatannya (*Severity*).
- **Hasil Translasi di Layar Web:** Program secara deterministik hanya tinggal mencetak: *"Huruf A di urutan pertama (Skor Keparahan 5)"* -> Cepat, Akurat, dan Tanpa perlu AI pengenalan huruf.

### SOLUSI 2: "Free-writing Tandem + NLP Spellchecker" (Sangat Keren, Tapi Butuh Tambahan AI)
Gunakan opsi ini jika tim-mu bersikeras membiarkan anak merangkai/menulis kata bebas dari **kotak kosong**.
- **Konsep:** Anak menulis 1 kata dalam 5 kotak secara acak. (Contoh ia ingin menulis "M A K A N").
- **Langkah 1 (OCR Buta):** Masukkan 5 crop gambar itu dari *OpenCV* menuju *Model OCR Pre-trained* milik Pihak Ketiga (yang umum bisa mendeteksi huruf). 
- **Langkah 2 (Spellchecker/AutoCorrect):** Karena anak disleksia sering salah (*Reversal*), Model OCR biasa ini mungkin akan membaca tulisannya menjadi: *"N A K A N"* atau *"M A K A M"*. Di titik inilah temanmu di AI/Backend harus memasang algoritma **NLP Spellchecker (.dll)** yang bisa "memaknai secara konteks" lalu otomatis mengoreksi: *"Oh, yang benar secara konteks kamus bahasa indonesia itu M A K A N"*. 
- **Langkah 3 (DyslexiaLens Evaluation):** Secara bersamaan, 5 gambar kotak tersebut diuji melalui model buatanmu khusus untuk melihat *pola goresannya*. Jika huruf 'N' di awal kotak dideteksi memiliki tingkat *Severity 4* (keparahan koreksi/coretan banyak), maka artinya anak tersebut kesulitan ketika mengeja 'M'.
- **Hasil Translasi:** Di layar pengguna tampil teks "MAKAN", dimana huruf M dicetak stabilo warna merah, menandakan deteksi indikasi kesulitan oleh AI mu.

### 📝 Kesimpulan untuk DS (Data Scientist)
Apapun pilihan arsitektur yang diambil kelompokmu (Solusi 1 atau Solusi 2), **kamu sebagai Data Scientist TIDAK PERLU melabeli dataset disleksiamu dengan Abjad (A-Z)**. Bagian menterjemahkan teks jatuh sepenuhnya kepada *OpenCV Deterministic Position* (Solusi 1) ATAU *Algoritma AutoCorrect NLP* (Solusi 2); karena Model Disleksia kamu mutlak secara khusus berfungsi mendiagnosis "*Pola Kepelikan Goresan Tulisan*", dan **Bukan Pengenal Teks!**
