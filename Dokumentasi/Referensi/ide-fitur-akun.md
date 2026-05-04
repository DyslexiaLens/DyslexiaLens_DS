# 💡 100 Urgensi & Fitur Esensial Sistem Login (DyslexiaLens)

Dokumen ini difokuskan secara spesifik pada pertanyaan: **"Mengapa kita membutuhkan fitur Login di aplikasi DyslexiaLens?"** Apa *value* (nilai tambah) yang tidak bisa dilakukan jika *user* hanya sekadar berkunjung secara anonim?

Berikut adalah **100 ide pemanfaatan fitur berbasis akun**, yang telah diurutkan dari yang paling masuk akal (mudah dibuat) hingga yang paling ambisius (sulit) untuk skop *Capstone Project*.

*Keterangan Skala:*
🟢 **Mudah/Sangat Realistis (4-5 Bintang)**
🟡 **Menengah (3 Bintang)**
🔴 **Sulit/Ambisius (1-2 Bintang)**
⚫ **Riset & Ekstrem (1 Bintang)**

---

## 🟢 Kategori Sangat Realistis (Mudah & Esensial)

### 1. Privasi & Keamanan Data Medis (Data Privacy)
**Ide:** Mengunci URL `/dashboard` hanya untuk pengguna terautentikasi agar data medis anak tidak bisa diakses publik.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Fungsi absolut dari Authentication. Mengunci *route* hanya untuk sesi yang valid sangat mudah di-*framework* mana pun.

### 2. Preferensi Aksesibilitas Permanen
**Ide:** Sistem menyimpan pengaturan *font* OpenDyslexic atau *Dark Mode* di *database* agar UI otomatis menyesuaikan tiap kali *login*.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Sangat mudah, cukup simpan data *boolean* `dyslexic_font_enabled: true` di profil *user* pada *database*.

### 3. Fitur Lupa Password & Reset Akun
**Ide:** Alur keamanan standar menggunakan pengiriman OTP via Email untuk mengembalikan akses akun.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Standar industri web modern, menggunakan *library* bawaan *backend*.

### 4. Avatar Profil Anak Kustom
**Ide:** Orang tua bisa mengunggah foto atau memilih avatar kartun untuk profil anaknya agar aplikasi terasa personal.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Hanya membutuhkan fungsi unggah gambar dasar (CRUD) ke ID profil.

### 5. Pencarian Riwayat Cepat (*Search Bar*)
**Ide:** Akun memungkinkan pencarian hasil tes lama berdasarkan tanggal atau nama anak langsung di *dashboard*.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Kueri SQL `LIKE` sederhana pada tabel riwayat *user*.

### 6. Mode Privasi Layar (*Blur Toggle*)
**Ide:** Tombol di akun untuk menge- *blur* skor medis secara otomatis jika sedang membuka web di tempat umum.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Sepenuhnya dikelola di UI (CSS `filter: blur`) yang preferensinya disimpan di akun.

### 7. Pengaturan Bahasa Aplikasi (i18n)
**Ide:** Menyimpan preferensi bahasa pengguna (Indonesia/Inggris) di dalam akun mereka.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** *State* sederhana yang dimasukkan ke skema tabel pengguna.

### 8. Tombol Hapus Akun Permanen (Delete Account)
**Ide:** Hak asasi pengguna (GDPR) untuk melenyapkan semua data riwayat tulisan anaknya dari server secara permanen.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Eksekusi `DELETE FROM users WHERE id = X` yang dilakukan secara kaskade (otomatis menghapus tabel relasi).

### 9. Ganti Email Terdaftar
**Ide:** Pengguna bisa memperbarui alamat email login mereka di menu pengaturan.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Fitur keamanan CRUD paling dasar di *framework* manapun.

### 10. Profil Biodata Anak Lengkap
**Ide:** Akun menyimpan detail seperti tanggal lahir dan umur, sehingga AI bisa mengaitkan umur dengan skor keparahan.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐⭐
**Alasan:** Kolom ekstra (tanggal) di dalam tabel profil.

### 11. Integrasi SSO (Login with Google)
**Ide:** Menggunakan *library* seperti Firebase/NextAuth agar *user* bisa *login* 1-klik tanpa membuat *password*.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Dipermudah oleh berbagai layanan pihak ketiga (*OAuth2*).

### 12. Riwayat & Progress Tracking Berkelanjutan
**Ide:** Setiap tes disimpan, memungkinkan web menampilkan grafik garis (*line-chart*) perkembangan *Severity Score* bulanan.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Membuat tabel relasi `Users` -> `Assessments` di *database* sangat standar.

### 13. Log Perangkat Keluar (*Logout Everywhere*)
**Ide:** Keamanan untuk mematikan seluruh sesi (*session*) jika akun terdeteksi dibuka di perangkat tidak dikenal.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Memanipulasi *session token* menggunakan Redis/JWT *Blacklisting*.

### 14. Audit Log Akses Medis (*Audit Trail*)
**Ide:** Mencatat *"Diakses dari IP Anda pada 2 Mei 2026"* di tabel log setiap kali data anak dibuka.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Melakukan operasi *Insert* ke tabel Log setiap *endpoint* diakses.

### 15. Penyimpanan Cloud Pribadi (History Backup)
**Ide:** Memberikan limit penyimpanan 1GB per pengguna (*user_id*) untuk riwayat foto tulisan secara permanen.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Logis jika menggunakan AWS S3 / Google Cloud Storage.

### 16. Gamifikasi & Sistem Poin Otomatis
**Ide:** Menambah nilai `points` pada tabel *user* setiap kali anak selesai tes untuk ditukar lencana.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Logika tambah nilai sederhana di DB setelah tes berhasil.

### 17. Bookmark Hasil Tes (*Starred Assessments*)
**Ide:** Fitur "Bintangi" hasil tes (misal: tulisan membaik drastis) agar selalu muncul di atas riwayat.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Tambah kolom *boolean* `is_starred` pada tabel riwayat.

### 18. Klasifikasi Tagging Kustom
**Ide:** Pengguna bisa memberi *tag* seperti `#LatihanMalam` atau `#TugasSekolah` pada tes mereka.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Tabel relasi *Many-to-Many* sederhana.

### 19. Catatan Harian Anak (*Daily Diary*)
**Ide:** Kolom input *text* untuk orang tua mencatat suasana hati anak hari itu bersamaan dengan tes.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Penambahan kolom `notes` bertipe teks panjang.

### 20. Pencapaian Streak Harian (Daily Streak)
**Ide:** Akun melacak "Api Menyala" 🔥 (Streak) jika anak rutin melakukan evaluasi tulisan tiap hari tanpa bolong.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Kalkulasi selisih hari terakhir *login* dengan hari ini di *backend*.

### 21. Statistik Akurasi Harian
**Ide:** Akun mendata berapa kali tes diproses hari ini untuk memantau performa latihan si anak.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Kueri *Count* berbasis tanggal hari ini.

### 22. Status Berlangganan (Pro Badge)
**Ide:** UI menampilkan *badge* Mahkota/Pro jika akun tersebut aktif berlangganan fitur penuh.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Pengecekan kolom `is_pro` yang mengatur render UI kondisional.

### 23. Mode Tampilan List/Grid Terhapal
**Ide:** Sistem akun mengingat apakah *user* lebih suka melihat riwayatnya dalam bentuk daftar (List) atau kotak (Grid).
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Kolom status *UI preference* di *database*.

### 24. Fitur Kontak Darurat Klinik
**Ide:** Orang tua bisa menyimpan nomor HP darurat terapis di dalam pengaturan akun mereka.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** Kolom *String* di tabel Profil.

### 25. Export Hasil Prediksi Tunggal
**Ide:** Daripada ekspor semua data, pengguna *login* bisa mencetak satu lembar hasil tes spesifik sebagai bukti evaluasi hari ini.
**Tingkat Realistis:** 🟢 ⭐⭐⭐⭐
**Alasan:** *Backend/Frontend* membuat PDF dari *View* tes spesifik menggunakan pustaka pembuat dokumen.

---

## 🟡 Kategori Menengah (Butuh Usaha Lebih)

### 26. Satu Akun, Multi-Profil (Therapist Mode)
**Ide:** 1 akun Terapis memuat 10 "Profil Anak", memisahkan direktori riwayat untuk tiap pasien berbeda.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Logika *database* (*One-to-Many*) mudah, tapi butuh waktu merancang UI navigasi yang aman.

### 27. Filter & Sort Riwayat Mahir
**Ide:** Tombol untuk mengurutkan riwayat dari *Severity Score* tertinggi atau memfilter bulan tertentu.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Implementasi parameter kueri dinamis yang sinkron dengan komponen visual di Web.

### 28. Laporan PDF & Ekspor Data Pribadi (GDPR)
**Ide:** Pengguna bisa mengunduh riwayat lengkap mereka dalam bentuk *file* ZIP (gambar + CSV skor AI).
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Butuh *script* pembungkus *file* yang tidak membuat *server* kehabisan RAM.

### 29. Sistem Persetujuan Riset (Data Consent)
**Ide:** Menyimpan perizinan *"Boleh dipakai latih AI"* di akun, bisa dicabut sewaktu-waktu.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Memerlukan arsitektur penghapusan data otomatis dari repositori pelatihan *Machine Learning*.

### 30. Secure Share to Expert (Tautan Aman)
**Ide:** *Generate* tautan URL JWT berbatas waktu (24 jam) untuk dikirimkan ke dokter tanpa harus *login*.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Pembuatan token *expiring* kriptografi dan validasi *middleware* ekstra.

### 31. Tanda Terima Baca Rujukan (*Read Receipts*)
**Ide:** Orang tua mendapat notifikasi di akunnya ketika tautan *Secure Share* benar-benar dibuka oleh dokter.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Merancang *WebHooks* pelacak tayangan URL.

### 32. Notifikasi Email Berkala (*Cron Reminders*)
**Ide:** Integrasi SendGrid untuk mengirimi email pengingat latihan tulisan tangan setiap minggu.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Pengaturan *Cron Jobs* (Celery/Node-Cron) yang memeriksa kapan terakhir kali anak tes.

### 33. Integrasi Kalender Google
**Ide:** Menyambungkan akun dengan Google Calendar API untuk menjadwalkan kunjungan dokter berdasarkan skor tes.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Pendaftaran Oauth 2.0 dan *handling token* integrasi pihak ketiga.

### 34. Laporan Berkala Otomatis (*Monthly Email Digest*)
**Ide:** Sistem mengompilasi statistik infografis sebulan ke email orang tua.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Perenderan *template* HTML dinamis yang dikirimkan via *cron job*.

### 35. Pembatasan Kuota (Paywall SaaS)
**Ide:** Membatasi 5 deteksi gratis per akun. Untuk *unlimited*, harus *upgrade* ke premium.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Integrasi *Payment Gateway* (Midtrans/Stripe) dan pengelolaan Webhook struk pembayaran.

### 36. Penghargaan Sertifikat Digital (*Auto-Generate*)
**Ide:** Akun mencetak sertifikat PDF *"Lulus Skor Normal!"* ketika anak berhasil menurunkan skornya berturut-turut.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Beban RAM untuk perenderan PDF dinamis di atas *template* sertifikat gambar.

### 37. Personalisasi Ambang Batas AI (Custom Thresholds)
**Ide:** Terapis menyimpan pengaturan *threshold* di akunnya (misal: "Jika probabilitas AI > 60%, anggap Dyslexia").
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Modifikasi alur prediksi (pipeline) CNN berdasarkan konstanta yang diambil dari *database user*.

### 38. Analitik Kelas / Grup (Teacher Dashboard)
**Ide:** Untuk akun Guru, dasbor memuat nilai rata-rata keparahan seluruh anak dalam satu kelas.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Membutuhkan kueri *Aggregations* (`AVG`, `SUM`) multi-tabel.

### 39. Penghapusan Akun Otomatis (*Data Retention*)
**Ide:** Skrip menghapus akun dan rekam medis yang pasif 1 tahun.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Skrip harus memastikan semua file terikat (*Cascade*) terhapus dari *Cloud Bucket*.

### 40. Badge Pakar Terverifikasi (Kredensial)
**Ide:** Akun dokter mengunggah lisensi untuk divalidasi admin demi "Centang Biru".
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Perlu membuat *Admin Dashboard* terpisah di dalam ekosistem aplikasi.

### 41. Sistem Rujukan Berafiliasi (*Referral Program*)
**Ide:** Poin tambahan jika pengguna mengundang orang lain via *link referral* akun mereka.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Manajemen kode kupon dan tabel referensi *user-to-user*.

### 42. Custom Dashboard Layout
**Ide:** Terapis bisa *drag-and-drop* tata letak dasbor web; posisinya disimpan.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Komponen UI *Frontend* kompleks yang diterjemahkan menjadi JSON ke *backend*.

### 43. Anotasi Gambar Manual
**Ide:** Dokter bisa mencoret-coret (memberi tanda) di atas foto unggahan anak, disimpan sebagai revisi.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Melibatkan Canvas HTML5 untuk menggambar dan operasi simpan ulang gambar.

### 44. Perbandingan Multi-Anak (*Siblings Comparison*)
**Ide:** Menampilkan dua grafik perkembangan anak (kakak dan adik) bersebelahan.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Pemanggilan data *time-series* dari entitas ganda secara bersamaan.

### 45. Rekomendasi Terapi Generatif (LLM Integration)
**Ide:** Mengirim skor AI CNN ke GPT-4 untuk menghasilkan paragraf saran terapi khusus di profil anak.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Menggunakan Prompt Engineering dan pemahaman arsitektur pemanggilan LLM eksternal.

### 46. Modul Edukasi Orang Tua Berjenjang
**Ide:** Konten artikel kesehatan yang baru terbuka jika skor anak melewati level keparahan tertentu.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Logika akses CMS artikel berbasis kondisi akun pengguna.

### 47. Leaderboard Gamifikasi Privat
**Ide:** Papan peringkat yang membandingkan poin latihan anak-anak asuhan seorang guru.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Skema pemeringkatan agregat antar pengguna satu jaringan sekolah.

### 48. Fitur Donasi Untuk Pengembangan AI
**Ide:** Pengguna bisa mengirim dana sukarela yang tercatat di akun mereka sebagai lencana Donatur.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Penggunaan integrasi pembayaran donasi (*One-Time Payment*).

### 49. Kuis Psikologis Terintegrasi (Pra-Asesmen)
**Ide:** Kuis ganda kuesioner kebiasaan anak yang skornya ditambahkan sebagai bahan pertimbangan AI gambar.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Membangun antarmuka ujian kuis dan skoring di atas *pipeline* utama AI tulisan.

### 50. Watermark PDF Rumah Sakit / Klinik
**Ide:** Terapis pro dapat mengunggah logo kliniknya, yang kemudian otomatis menjadi *watermark* tiap kali ia mencetak laporan anak.
**Tingkat Realistis:** 🟡 ⭐⭐⭐
**Alasan:** Pengaturan *setting profile* ekstra dan modifikasi *script generation* PDF.

---

## 🔴 Kategori Sulit & Ekstrem (Sangat Ambisius)

### 51. Kolaborasi Lintas Pengguna (*Invite Collaborator*)
**Ide:** Orang tua mengundang akun dokter spesifik agar bisa mengakses profil anaknya secara kolaboratif (Multi-Parenting).
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Implementasi ACL (*Access Control List*) kompleks untuk skema Many-to-Many.

### 52. Manajemen Hak Akses File Berjenjang
**Ide:** Pengguna bisa mengatur riwayat tes sebagai "Publik", "Link Saja", atau "Proteksi Password".
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** *Middleware permission server* untuk setiap gambar yang di-GET. Sangat merepotkan.

### 53. Sistem Pesan Internal (*In-App Chat*)
**Ide:** Chatting *real-time* antar orang tua dan terapis langsung di aplikasi.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Pengembangan aplikasi *WebSocket* murni dari nol. Berbeda total dengan fokus AI gambar.

### 54. Sinkronisasi Data Offline (PWA Sync)
**Ide:** Memfoto tanpa sinyal, lalu tersinkronisasi ke akun saat terhubung internet.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Konflik sinkronisasi dan manajemen memori browser (IndexedDB) tingkat mahir.

### 55. Video Playback Proses Menulis
**Ide:** Menyimpan *time-series* kecepatan titik coretan tangan menjadi "Video Replay" gerak lambat tulisan anak.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Perekaman *milisecond* gerakan tetikus/layar HP yang membutuhkan *database* format JSON ekstra tebal.

### 56. Integrasi Wearable (Smartwatch Anak)
**Ide:** Memasukkan parameter tidur anak dari *smartwatch* ke akun untuk dianalisis korelasinya dengan disleksia.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Sinkronisasi API perangkat *Hardware IoT* pihak ketiga.

### 57. Pelacakan Waktu Tes (*Time-Spent Analysis*)
**Ide:** Akun mencatat durasi mili-detik anak mengerjakan penulisan tes untuk mendeteksi keraguan.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Metrik *telemetry Frontend* rentan meleset karena koneksi.

### 58. Mode Kios (*Kiosk Mode* Klinik)
**Ide:** Sesi spesifik tablet ruang tunggu klinik agar banyak pasien tes mandiri tanpa melihat data orang lain.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Manajemen siklus sesi *login* yang tidak biasa (*auto-reset state*).

### 59. Rekaman Suara Sesi Membaca
**Ide:** Akun mendukung fitur mengeja (*Speech-to-Text*) suara anak selain foto gambar.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** AI berlapis. Pemrosesan ukuran fail WAV/MP3 memakan memori *Cloud* yang amat besar.

### 60. API Key Personal (*Developer Mode*)
**Ide:** Akun mem-*generate* Token API khusus agar peneliti bisa menarik data mereka secara terprogram (B2B).
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Harus membuat arsitektur *Public API Gateway* bersistem perlindungan *Rate Limit* khusus.

### 61. Autentikasi Biometrik Langsung (WebAuthn)
**Ide:** *Login* dengan Face ID atau pemindai sidik jari perangkat, meninggalkan *password* kuno.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Integrasi FIDO2 *standard* yang sering menyebabkan *bug* di berbagai macam OS HP *user*.

### 62. Verifikasi Identitas via KTP (eKYC)
**Ide:** Dokter harus memfoto KTP dan wajah mereka ke sistem pihak ketiga untuk menekan tombol "Validasi Dokter Medis Asli".
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Harus membeli layanan API mahal seperti Verihubs/PrivyID untuk OCR biometrik pemerintahan.

### 63. Video Call / Telemedicine Integrasi
**Ide:** Ruang konferensi video bawaan aplikasi agar orang tua berkonsultasi virtual dengan dokter.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Pemrograman *WebRTC Peer-to-Peer* streaming video.

### 64. Sistem Inventaris Alat Terapi (Untuk Akun Klinik)
**Ide:** Dokter bisa merekap inventaris alat tes fisik mereka (seperti blok kayu braille) dalam akun yang sama.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Berubah arah dari aplikasi med-tech pasien menjadi aplikasi ERP klinik (kehilangan fokus MVP).

### 65. Sinkronisasi Data Lintas Pasangan (Co-Parenting Link)
**Ide:** Ayah dan Ibu memiliki akun berbeda namun tersinkronisasi murni pada 1 profil anak yang sama secara paritas penuh.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Kerumitan penyatuan *ID Object* pada *NoSQL/SQL* ganda.

### 66. Transkripsi Suara Terapis (Voice Notes to Text)
**Ide:** Dokter yang sibuk cukup berbicara untuk mengisi form medis, dan AI langsung menuliskannya di catatan akun.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Implementasi Model *Whisper* AI secara mandiri.

### 67. Pemantauan Gerak Mata Terintegrasi Web (Eye-Tracking)
**Ide:** Mengakses *webcam* anak untuk melihat arah pandangan matanya saat ia kesulitan membaca huruf di layar.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Algoritma presisi tinggi *Computer Vision Real-time* di *browser* sanga lambat dan memberatkan CPU pengguna.

### 68. Penjadwalan *Booking* Offline Layaknya Traveloka
**Ide:** Dokter mengatur jam kerja di akun, dan pasien bisa memesan kursi jadwal evaluasi klinis tatap muka dari *dashboard*.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Algoritma alokasi waktu dan antrean bentrok jadwal yang super rumit.

### 69. Rekomendasi Teman Sebaya Ter-otomasi (*Community Matching*)
**Ide:** AI menyarankan, *"Ada pasien anak umur 7 tahun dengan kondisi mirip di kota Anda, ingin menyapa keluarganya?"*.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Menyinggung privasi super ketat dan fitur ala jejaring sosial (*Social Media Matchmaking*).

### 70. Fitur Pelacakan Kesalahan Huruf Spesifik (*Heatmap Per Huruf*)
**Ide:** DB tidak hanya mencatat Skor AI, tapi menyimpan rekap *"Anak Anda 10x salah di huruf P dan 5x di huruf B"*.
**Tingkat Realistis:** 🔴 ⭐⭐
**Alasan:** Mengharuskan model Object Detection (YOLO) berlapis, merombak total *pipeline* Dataset Gambo yang saat ini hanya berupa klasifikasi gambar utuh.

### 71. Peer-to-Peer Encrypted Data (E2EE)
**Ide:** Hanya *user* yang bisa mendeskripsi file gambar medis mereka, *admin* server hanya melihat data terenkripsi.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Secara fundamental mematikan cara kerja CNN Server karena Server juga tidak bisa melihat gambar yang hendak diprediksi! (Terkecuali menggunakan *Homomorphic Encryption* yang super lambat).

### 72. Model Prediktif Putus Sekolah Dasar (Dropout Prediction)
**Ide:** AI tambahan di *dashboard* yang memprediksi persentase kemungkinan anak putus sekolah akibat keparahan disleksianya.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Membutuhkan miliaran data longitudinal anak yang Anda belum punya, serta memiliki risiko etika sangat fatal.

### 73. Sistem Pelatihan Model AI Lokal Kustom (Federated Learning)
**Ide:** Setiap akun klinik mempunyai *model AI kecil* yang belajar khusus pada data anak di desa mereka, lalu menyetorkan ilmunya ke server pusat tanpa mengirim gambarnya.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Teknik *Federated Learning* komputasi tinggi level Google/Apple R&D lab S3.

### 74. Asisten Voice Bot Interaktif Pribadi
**Ide:** Chatbot 3D yang langsung mengobrol riang via suara dengan anak menggunakan data profil mereka.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Gabungan TTS, STT, LLM, dan perenderan Avatar 3D WebGL (Overkill untuk MVP diagnostik).

### 75. Terapi VR/AR Integrasi Web (WebXR)
**Ide:** Anak memakai kacamata VR dan web memproyeksikan huruf yang mengambang di ruang tamu mereka berdasar status akun.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Pemrograman *Spatial Computing* dan perangkat *hardware* yang di luar kemampuan aplikasi *Data Science* reguler.

### 76. Integrasi Sistem Rekam Medis Nasional (EMR SATUSEHAT RI)
**Ide:** Menjadikan akun pengguna *DyslexiaLens* tersinkron langsung ke *database* rekam medis Kementrian Kesehatan berstandar HL7 FHIR.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Proses perizinan kementrian dan implementasi *security* standar rumah sakit yang mustahil ditembus oleh riset Capstone kampus.

### 77. Analisis Gelombang Otak Eksternal (EEG/BCI API)
**Ide:** Menghubungkan akun anak dengan API bando pemindai gelombang otak komersial (NeuroSky) saat mereka menulis huruf di kertas.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** *Hardware IoT Neuro-tech* yang datanya sangat bising (Noisy) untuk diproses Web Server biasa.

### 78. Rekam Medis Genetik / DNA
**Ide:** Akun menerima *upload file sequencing* DNA anak (23andMe) untuk mencari korelasi gen FOXP2 dengan Disleksia yang mereka alami.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Bio-Informatika level murni (DNA *parsing*). Tidak ada sangkut pautnya dengan fokus utama CNN *Computer Vision* aplikasi ini.

### 79. Pendeteksi AI Tingkat Stres Suara Otot Jari (EMG Data)
**Ide:** Mengintegrasikan pena bersensor yang melacak tekanan otot jari berkeringat ke *dashboard* pasien.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Harus memanufaktur purwarupa pulpen *Hardware IoT* sendiri menggunakan mikrokontroler Arduino/ESP32.

### 80. Intervensi Stimulasi Saraf Vagus Berbasis Web
**Ide:** Terapis pro menekan tombol di profil anak untuk menembakkan frekuensi getar relaksasi pada perangkat kalung terapi yang digunakan sang anak secara jarak jauh.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** *Cyber-physical medical systems* dengan risiko tinggi kegagalan peranti.

### 81. Model AI Pembuat Font Personal Spesifik (Auto-Typography)
**Ide:** AI *Generative* mempelajari cara anak salah menggambar huruf, lalu me-*generate* file `.ttf` font eksklusif hanya untuk mata anak tersebut.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Pembuatan *Generative Adversarial Network* (GAN) vektor *font* berbasis 1 data orang adalah area R&D eksklusif.

### 82. Analisis Sentimen Psikologis Catatan Buku Harian
**Ide:** Menjalankan model *Natural Language Processing* tingkat lanjut pada catatan harian orang tua (Ide #19) untuk mendeteksi depresi/burnout di pihak orang tua.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Anda harus mendeploy dua AI model besar sekaligus (CNN untuk gambar anak + NLP Psikologi Orang Tua) dan akan sangat menghabiskan *budget* *cloud server*.

### 83. Pelacakan Trajektori Mouse Prediktif (Dyslexic Pointer)
**Ide:** Menganalisis cara kursor tetikus/mouse *user* bergerak saat membaca web (yang biasanya terputus-putus pada penderita) untuk menebak disleksia pasif.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Analisis fraktal dari API gerakan *mouse* JS membuahkan jutaan baris matriks koordinat per detiknya.

### 84. Metaverse Therapy Room (3D Multiplayer Web)
**Ide:** Dokter dan Pasien tidak *video call*, melainkan berubah jadi avatar 3D berjelajah di sebuah ruang kelas VR yang dirender di Web Browser.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Pembangunan mesin *Game Engine* (Three.js/Babylon.js) lengkap dengan *Physics* dan Server *Multiplayer* jaringan tingkat gim *online*.

### 85. Integrasi Token Kripto Medis (Web3 / Blockchain)
**Ide:** Identitas *user* dan riwayat medis tidak disimpan di MySQL, melainkan dienkripsi sebagai *Smart Contract* (NFT) di jaringan Ethereum/Polygon.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Berubah arah dari arsitektur *Web 2.0 HealthTech* menjadi *Web3 DApp* desentralisasi dengan kendala lambat dan mahalnya "Gas Fee".

### 86. Algoritma Pembentukan "Kelompok Kelas Anak Pintar" Otomatis
**Ide:** AI otomatis merekomendasikan anak pasien ke grup sekolah luar biasa negeri dengan menghitung probabilitas IQ sekunder berdasar tes mereka.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Kebijakan seleksi pendidikan sangat berisiko bias AI (*AI Bias*) dan rawan gugatan tuntutan hukum diskriminasi.

### 87. Real-Time Hologram Projection API
**Ide:** Output sistem tidak merender 2D *Heatmap* piksel di browser, melainkan memproyeksikannya sebagai hologram 3D via *Looking Glass API*.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** *Hardware* tampilan *Sci-Fi* tidak dimiliki satupun masyarakat umum.

### 88. Sistem Validasi Fakta Berbasis Graf Terdesentralisasi (Knowledge Graph)
**Ide:** Akun Dokter disandingkan dengan ensiklopedia penyakit graf vektor jutaan *node* yang tervalidasi publik setiap kali memberi *Severity Score*.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Penyiapan *Graph Database* Neo4J yang besar tidak realistis untuk sekadar web tes deteksi CNN gambar.

### 89. Opsi Menjual Data ke Perusahaan Riset secara Anonim (Data Broker)
**Ide:** Orang tua mengaktifkan *slider* di profil untuk melelang gambar anonim mereka ke lembaga S3 Internasional dan dibayar royalti.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Masalah *Legal/Compliance* (Hukum Tata Niaga Data Medis) yang belum ada *framework* legal pastinya untuk mahasiswa *Capstone*.

### 90. Rekonstruksi Emosi Berbasis Wajah Mikro (Micro-Expression AI)
**Ide:** Sambil web meng-*upload* kertas tes, *webcam* merekam mikro-ekspresi wajah anak untuk menentukan tingkat rasa frustrasi (Marah, Sedih, Bingung).
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Menggunakan model AI emosi berlapis dengan beban komputasi CPU 100% pada peramban klien.

### 91. Sinkronisasi Cerdas ke Aplikasi *Smart Home* (Lampu Philips Hue)
**Ide:** Jika akun anak menunjukkan *Severity Score* parah hari ini, web DyslexiaLens memerintahkan bola lampu rumah anak berubah jadi warna biru kalem.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Interaksi *Smart Home API* yang melampaui fokus alat medis menjadi fiksi ilmiah (*lifestyle app*).

### 92. Algoritma Prediksi Kidal atau Tangan Kanan Otomatis
**Ide:** CNN tidak hanya mendeteksi skor keparahan, tapi bisa menebak secara terbalik apakah tulisan dibuat dengan tangan kiri (kidal) atau kanan (berdasarkan arah noda gesekan tangan).
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Tidak ada anotasi kelas "Kidal/Kanan" pada *Dataset Gambo* Anda sekarang. Membutuhkan anotasi 100 ribu data ulang.

### 93. Pembuatan Lagu Terapi Otomatis Terkustomisasi (AI Music Generator)
**Ide:** Dari skor hasil CNN yang tinggi, web membuat alunan nada *binaural beats* rileks kustom yang hanya tersimpan di profil si anak untuk menenangkannya.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Mengerahkan model API kreasi audio tingkat MusicLM/Suno AI yang super mahal biayanya.

### 94. Pencetakan 3D Alat Bantu Tulis Relief (*3D Printing API*)
**Ide:** Jika anak dinyatakan parah di huruf 'A', akun mem-*generate file* model 3D (STL) huruf A bertekstur kasar untuk dikirim ke *printer* 3D rumah sakit setempat.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Bergeser dari produk piranti lunak (*Software*) menjadi produk piranti keras mekanik (G-Code generation).

### 95. Auto-Translate Catatan Terapis ke Bahasa Ibu Langka
**Ide:** Catatan spesialis otomatis di-*translate* ke dialek pedalaman / bahasa isyarat video 3D avatar sesuai *setting* asal orang tua di pedesaan.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Terbatasnya API terjemahan dialek langka yang bersertifikasi medis (agar tidak salah instruksi mematikan).

### 96. Model Pembaca Tulisan Melayang (In-Air Tracing CNN)
**Ide:** Anak tidak menulis di kertas maupun layar, melainkan melambaikan jari mereka di udara depan *webcam*, dan sistem merender hurufnya lalu men-skoring disleksianya.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** *Computer Vision Body Pose Estimation* presisi mili-sentimeter 3 dimensi (Sangat mustahil untuk ujung jari di kamera beresolusi rendah).

### 97. Modifikasi Skoring Berbasis Gelembung Oksigen Darah (SpO2)
**Ide:** DyslexiaLens menurunkan *Severity Score* jika oksigen darah anak di bawah rata-rata (anak sekadar mengantuk, bukan disleksia permanen).
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Perangkat oxymeter klinis harus diprogram sinkronisasi Bluetooth ke Web API via protokol GATT yang jarang stabil di browser.

### 98. Laporan Uji Diagnostik Keterikatan Pemasaran
**Ide:** Akun secara paksa membandingkan hasil medis anak dengan kecenderungan klik iklan orang tua mereka.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Praktik pelacakan data paling *illegal* yang dilarang keras di aplikasi pengujian pendidikan *Cambridge Analytica*.

### 99. AI Pendeteksi Tanda Tangan Orang Tua Palsu
**Ide:** Anak yang mengunggah kertas dengan cap/tanda tangan persetujuan palsu orang tua akan ditolak oleh AI penilai dokumen pendukung akunnya.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Model Verifikasi Forensik Grafologi Signature berbeda alam dengan klasifikasi Dyslexia, menuntut *Dataset Forensik Kepolisian*.

### 100. Pembangkitan Laporan Kembar Digital Medis (Full Digital Twin)
**Ide:** Aplikasi membangun replika 3D utuh dari anatomi sistem syaraf tiruan si anak pada *database* berdasarkan simulasi matematika riwayat unggahan puluhan tahun mereka ke depan.
**Tingkat Realistis:** ⚫ ⭐
**Alasan:** Hanya bisa dilakukan oleh super-komputer spesifik di MIT/Stanford untuk mensimulasikan dinamika fluida & neuron seumur hidup manusia.
