# 🌐 Dokumen Konteks — Full-Stack Engineer: User Flow & Error Flow
**Dibuat:** 1 Juni 2026  
**Tujuan:** Mendokumentasikan alur pengguna (*User Flow*) dan penanganan error (*Error Flow*) yang dirancang oleh tim Full-Stack Engineer untuk aplikasi web DyslexiaLens, beserta catatan koreksi terbaru dari tim pengembang.  
**Status:** 🟡 Dalam Progres — Pengembangan UI/UX dan Integrasi Sistem

---

## 🖼️ Referensi Diagram Visual
Diagram asli dari desain awal dapat dilihat pada tautan file berikut (berada di dalam repositori):
- **User Flow:** `Dokumentasi/Referensi/Full-Stack/User_Flow.png`
- **Error Flow:** `Dokumentasi/Referensi/Full-Stack/Error_Flow.png`

---

## 🔄 Pembaruan & Koreksi Alur (Update Terbaru)
Berdasarkan konfirmasi dan diskusi langsung dengan tim Full-Stack, diagram visual yang ada secara garis besar sudah sesuai arahannya, namun kurang mendetail. Terdapat **dua koreksi penting** pada implementasi aktual yang menganulir desain lama:

1. **Penghapusan Tahap Verifikasi Email:** 
   Alur pendaftaran (*Register*) dipangkas menjadi lebih ringkas. Pengguna tidak lagi perlu membuka email untuk menekan tautan verifikasi. 
   - **Alur Baru:** Halaman Register → Input Data → **Langsung Register Success**.

2. **Pencabangan Fitur Edit Profile:** 
   Menu Edit Profile dibuat lebih modular dan mendetail, dipecah menjadi **dua cabang terpisah**:
   - Cabang 1: **Edit Informasi Akun** (Mengubah kredensial dasar, nama, dll.)
   - Cabang 2: **Edit Alamat** (Mengubah detail domisili)

---

## 🚶‍♂️ Detail User Flow (Berdasarkan Diagram Asli & Koreksi)

Berdasarkan diagram `User_Flow.png`, alur pengguna dibagi menjadi dua persona: **Flow Guest** (Pengguna belum login) dan **Flow User** (Pengguna sudah login). Berikut adalah kesimpulan alurnya beserta koreksinya:

### 1. Flow Guest (Pengguna Belum Login)
- **Akses Landing Page:** Guest memiliki 2 opsi utama yaitu Auth (Login/Register) dan Mulai Analisis.
- **Alur Auth (Koreksi):** 
  - **Register:** Input data diri (Nama, Email, Password, Konfirmasi) ➔ *(Berdasarkan koreksi, tahap Verifikasi Email dihapus)* ➔ Langsung diarahkan ke halaman Login.
  - **Login:** Input Email & Password ➔ Masuk Landing Page sebagai User.
  - **Lupa Password:** Input Email ➔ Input OTP ➔ Input Password Baru ➔ Login.
- **Alur Mulai Analisis (Deteksi & Translate):**
  - Guest mengunggah (Input) Foto.
  - Sistem mengeluarkan **Output** (Hasil Analisis / Terjemahan).
  - Saat Guest mencoba **Simpan Hasil**, sistem akan mengarahkan mereka untuk **Login** terlebih dahulu agar hasil tersimpan ke Riwayat.

### 2. Flow User (Pengguna Sudah Login)
- **Akses Landing Page:** User memiliki opsi tambahan yaitu Profil Saya, Riwayat, serta tombol Logout.
- **Alur Mulai Analisis:** Sama dengan Guest, namun ketika menekan **Simpan Hasil**, data langsung tersimpan tanpa perlu login ulang.
- **Alur Riwayat:** User dapat melihat hasil Output (Deteksi atau Translate) yang sudah disimpan sebelumnya.
- **Alur Profil Saya (Koreksi):**
  - Berdasarkan diagram asli, Edit Profile memiliki cabang "Edit Informasi Akun", "Ganti Password", dan "Lupa Password".
  - **[KOREKSI TIM FULL-STACK]:** Edit Profile kini diubah menjadi 2 cabang utama: **Edit Informasi Akun** dan **Edit Alamat**. (Cabang untuk keamanan akun seperti password mungkin disatukan atau ditangani terpisah).

---

## 🎨 Desain UI Result Page (Hasil Analisis & Translate)

Berdasarkan *mockup* UI terbaru yang telah dirilis, desain halaman hasil (Output) dipisah menjadi dua tampilan spesifik, namun menggunakan struktur *layout* yang konsisten:

### 1. UI Hasil Terjemahan (Translate / OCR)
- **Header Top:** Judul "Hasil Terjemahan", status (Selesai), tanggal, dan tombol **Export PDF**.
- **Komparasi Visual (Split Screen):** 
  - **Tulisan Asli (Kiri):** Menampilkan gambar tulisan tangan asli (diambil dari proses *crop/scan*).
  - **Teks Normal (Kanan):** Menampilkan teks digital hasil konversi model OCR.
- **Teks Lengkap:** Menggabungkan seluruh hasil teks normal menjadi satu kalimat penuh/utuh.
- **Catatan Sistem:** *Disclaimer* bahwa terjemahan berdasarkan pola dan mungkin perlu diperiksa kembali untuk konteks akurasi penuh.
- **Action Buttons:** "Simpan ke Riwayat" dan "Translate Lagi".

### 2. UI Hasil Analisis (Deteksi Disleksia & Severity)
- **Header Top:** Judul "Hasil Analisis" beserta **Badge Persentase Indikasi** (cth: *84% Indikasi*, yang berkorelasi dengan Severity Score dari model Regresi), tanggal, dan tombol **Export PDF**.
- **Visual Asli:** Menampilkan *preview* gambar tulisan tangan yang dievaluasi.
- **Seksi "Temuan" (Penerjemahan XAI ke Bahasa Awam):** Menampilkan hasil deteksi fitur-fitur matematis/geometris dari model menjadi bahasa visual yang mudah dimengerti:
  - *Contoh Temuan Kritis:* **Pembalikan Huruf** (Badge Merah / Tinggi) — *Terdeteksi beberapa kebingungan huruf 'b/d' dan 'p/q'. Ini adalah indikator awal yang umum.*
  - *Contoh Temuan Moderat:* **Jarak Tidak Teratur** (Badge Oranye / Sedang) — *Jarak antar kata tidak konsisten.*
- **Action Buttons:** "Simpan ke Riwayat" dan "Analisis Lagi".
- **Disclaimer Medis (Krusial):** Terdapat *footer bar* bertuliskan: *"Disclaimer: Ini bukan diagnosis medis. Konsultasikan dengan profesional untuk evaluasi klinis."* (Ini memenuhi SLA *ethical AI* proyek ini).

---

## ⚠️ Detail Error Flow (Kesimpulan Diagram Error Asli)

Berdasarkan diagram `Error_Flow.png`, berikut adalah kesimpulan komprehensif terkait bagaimana sistem menangani berbagai *error* yang mungkin terjadi:

### 1. Error Autentikasi (Login & Register)
- **Validasi Form Login/Register Gagal:** Jika format email salah, form kosong, atau password lemah ➔ *Highlight field error* merah & tampilkan pesan perbaikan (misal: "Format Tidak Sesuai" atau "Password Tidak Cocok").
- **Kredensial Salah (Login):** 
  - Email tidak terdaftar ➔ Tampilkan pesan & beri **Link Register**.
  - Password salah ➔ Tampilkan sisa percobaan. Jika gagal 3x berturut-turut ➔ **Akun Terkunci** dan arahkan ke fitur "Lupa Password".
- **Email Duplikat (Register):** Email sudah ada di database ➔ Tampilkan pesan & beri **Link Login**.

### 2. Error pada Proses Lupa Password & Verifikasi OTP
- OTP Salah atau Kadaluarsa (*Expired*) ➔ Munculkan tombol/opsi **Kirim Ulang OTP**.

### 3. Error Fitur Utama (Mulai Analisis - Input Foto)
- **Format File:** File bukan foto/gambar (Format Tidak Didukung) ➔ Tampilkan pesan error batas maksimal ukuran / format & kembali ke halaman upload.
- **Ukuran File:** File terlalu besar ➔ Tampilkan "File Terlalu Besar" & minta coba lagi.
- **Error Pemrosesan / Timeout Server AI:** Server gagal merespon atau terjadi *timeout* saat memproses gambar (baik di Computer Vision maupun FastAPI) ➔ Tampilkan "Server Error / Timeout" & "Pesan Error + Coba Lagi".

### 4. Error Edit Profil
- Format email baru tidak valid ➔ *Highlight field error*.
- Email baru ternyata sudah digunakan orang lain ➔ Tampilkan pesan untuk mengganti email lain.
- Validasi OTP gagal saat mencoba menyimpan profil baru ➔ Kirim ulang OTP.
- **Validasi Ganti Password (Jika masih dipertahankan):** 
  - Password lama salah ➔ Beri link Lupa Password.
  - Password baru terlalu lemah ➔ Tampilkan syarat password.

---

## 📌 Status & Hal yang Masih Perlu Dikonfirmasi

| Hal | Status |
|---|---|
| Revisi User Flow (Hapus Verifikasi Email & Ubah Cabang Edit Profile) | ✅ Dikonfirmasi (via tim Full-Stack) |
| Desain UI/UX untuk *Result Page* (Deteksi & Translate) | ✅ Telah diselesaikan secara terpisah dengan konsistensi *layout* |
| Error handling untuk kertas grid yang tidak terdeteksi oleh *Computer Vision* (belum ada di diagram) | ⚠️ Perlu didiskusikan dengan Backend |
| Mekanisme *retry* otomatis saat terjadi Timeout di server AI | ⚠️ Perlu dikonfirmasi |
