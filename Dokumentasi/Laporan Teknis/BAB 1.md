# BAB 1: Pendahuluan & Konteks Bisnis

## 1.1 Latar Belakang Masalah
Disleksia adalah gangguan belajar neurologis yang ditandai dengan kesulitan dalam membaca, menulis, dan mengeja. Diagnosis disleksia umumnya lambat karena ketergantungan pada evaluasi psikologis klinis yang memakan waktu dan biaya tinggi. Namun, berbagai penelitian medis menunjukkan bahwa penderita disleksia sering memanifestasikan gangguan motorik halus saat menulis. Gejala ini terekam secara persisten dalam pola fisik tulisan tangan, seperti bentuk huruf yang asimetris, goresan yang terputus-putus (*tremor*), hingga distorsi orientasi ruang (*letter reversal*) **(Isa et al., 2019; Rosli et al., 2021; Seman et al., 2021)**. 

Dalam proyek **DyslexiaLens**, kami mengajukan pendekatan deteksi dini alternatif: memanfaatkan teknologi *Computer Vision* dan *Machine Learning* untuk menganalisis pola goresan tulisan tangan sebagai *biomarker* kuantitatif. Perlu ditekankan secara tegas bahwa **sistem ini bukan alat diagnosis medis definitif**, melainkan alat skrining awal (*early screening*) guna memberikan indikasi probabilitas kepada orang tua dan pendidik sebelum dirujuk ke profesional klinis.

Tantangan utama dalam mewujudkan sistem skrining ini adalah kelangkaan dataset tulisan tangan disleksia yang terstruktur, seimbang, dan terbebas dari bias label. Oleh karena itu, proyek ini memanfaatkan **dataset publik 'Gambo' dari Kaggle** sebagai bahan baku utama. Laporan ini secara spesifik mendokumentasikan proses *end-to-end Data Science* untuk merestorasi dan menyusun *pipeline dataset* yang bersih dan tangguh (*robust*), sebagai pondasi esensial sebelum model kecerdasan buatan dilatih oleh tim AI.

## 1.2 Tujuan Proyek
Fokus dari *Technical Report* Data Science ini adalah:
1. Mengaudit, membersihkan, dan merekonstruksi dataset publik "Gambo" agar terbebas dari anomali *label noise* dan metrik keparahan yang cacat.
2. Melakukan *Feature Engineering* (pendekatan *Explainable AI / XAI*) untuk menerjemahkan karakteristik goresan gambar mentah menjadi metrik matematis yang dapat diinterpretasi.
3. Membangun strategi penyeimbangan kelas (*Dual-Track Dataset*) melalui augmentasi cerdas berbasis dataset eksternal (EMNIST), serta memvalidasi keamanan augmentasi tersebut menggunakan uji statistik (*A/B Testing*).
4. Menghasilkan *master dataset* akhir yang terstandarisasi dan siap didistribusikan (*handover*) ke tim AI Engineer.

## 1.3 Pertanyaan Bisnis
Rangkaian eksperimen Data Science dalam proyek ini didesain untuk menjawab empat pertanyaan analitis krusial:
1. **Apakah dataset asli (Gambo) sudah cukup representatif dan seimbang untuk melatih model AI?**
   *(Fokus: Memvalidasi integritas data, mengecek potensi bias kelas, dan memutuskan urgensi injeksi dataset eksternal seperti EMNIST).*
2. **Apakah pola visual dalam tulisan tangan cukup kuat untuk merepresentasikan kondisi kognitif disleksia, atau sekadar indikasi ambigu?**
   *(Fokus: Membuktikan secara empiris bahwa disleksia meninggalkan jejak visual fisik seperti tremor dan asimetri ruang yang terukur).*
3. **Bagaimana cara mengekstrak metrik visual secara matematis agar model klasifikasi AI di fase selanjutnya tidak menjadi *'black-box'* (pendekatan *Explainable AI*)?**
   *(Fokus: Mengembangkan 6 fitur matematis / XAI sebagai pondasi transparansi interpretasi pola).*
4. **Bagaimana merekonstruksi dan mengamankan metrik keparahan (*Severity Score*) bawaan yang anomali agar layak menjadi target prediksi?**
   *(Fokus: Memastikan *pipeline* mendefinisikan label target yang bersih dan logis, sehingga model kelak mampu mendeteksi tingkat keparahan disleksia secara berjenjang).*
