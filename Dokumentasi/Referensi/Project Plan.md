Tema Capstone	: 	Accessible & Adaptive Learning
Nama/Judul Proyek	: 	DyslexiaLens: Intelligent Handwriting Detection and Assistance for Dyslexia

A.	Ringkasan Eksekutif
Problem Statement
Deteksi disleksia saat ini umumnya masih bergantung pada observasi manual dan tes psikologis yang memerlukan waktu, biaya, serta keterlibatan tenaga ahli. Spoon dkk. (2019) menyoroti bahwa hal ini menyebabkan banyak kasus tidak teridentifikasi sejak dini, terutama pada anak-anak usia sekolah. Padahal, disleksia memiliki indikator yang dapat diamati dari tulisan tangan seperti pembalikan huruf, inkonsistensi ukuran, dan kesalahan ejaan (Jasira dkk., 2023a; Oktamarina dkk., 2022; Robaa dkk., 2024). Namun, indikator-indikator tersebut tidak selalu secara langsung merepresentasikan kondisi kognitif secara pasti, karena dapat dipengaruhi oleh berbagai faktor lain seperti kemampuan motorik, pengalaman belajar, dan konteks penulisan. Tantangan utama bukan hanya mendeteksi pola visual tersebut, tetapi juga bagaimana memanfaatkannya secara otomatis dan objektif sebagai indikasi awal melalui pendekatan berbasis analisis citra, tanpa menggantikan peran diagnosis profesional.
Selain sebagai indikator awal, tulisan tangan pada individu dengan disleksia juga sering sulit dibaca akibat distorsi bentuk huruf, pembalikan karakter, dan ketidakteraturan spasial. Hal ini tidak hanya berdampak pada proses analisis, tetapi juga pada kepercayaan diri dan efektivitas komunikasi tertulis pengguna.
Dengan memanfaatkan pendekatan computer vision, tulisan tangan berbasis grid dapat diproses sebagai citra huruf individual untuk dikenali dan diterjemahkan menjadi representasi yang lebih terstruktur. Oleh karena itu, sistem yang dikembangkan tidak hanya berfokus pada klasifikasi indikasi disleksia, tetapi juga pada penerjemahan tulisan tangan agar lebih mudah dibaca dan dipahami.
Research Question
	Untuk mengatasi permasalahan tersebut, proyek ini akan menjawab pertanyaan penelitian berikut:
1.	Apakah pola visual dalam tulisan tangan cukup kuat untuk merepresentasikan kondisi kognitif seperti disleksia, atau hanya sekadar indikasi permukaan yang ambigu?
2.	Bagaimana merancang sistem AI yang tidak hanya akurat, tetapi juga mampu menjelaskan mengapa suatu tulisan diklasifikasikan sebagai indikasi disleksia?
3.	Bagaimana merancang dan mengevaluasi sistem berbasis AI yang mampu mengenali karakter tulisan tangan dari citra berbasis grid dan menerjemahkannya menjadi huruf yang akurat dan mudah dibaca, terutama pada tulisan dengan distorsi khas disleksia?
4.	Bagaimana memodelkan dan menganalisis urutan huruf hasil pengenalan karakter untuk mengidentifikasi pola ketidakkonsistenan dalam tulisan tangan?
5.	Seberapa efektif kombinasi CNN dan sequence modeling dalam mengklasifikasikan urutan tulisan tangan menjadi indikasi disleksia dan non-disleksia?
6.	Bagaimana sistem dapat memberikan interpretasi terhadap hasil prediksi, baik dalam konteks klasifikasi disleksia maupun proses penerjemahan tulisan tangan?
Latar Belakang
Disleksia merupakan gangguan belajar yang memengaruhi kemampuan membaca, menulis, dan mengeja meskipun individu memiliki kecerdasan normal (Jasira dkk., 2023a; Peterson dkk., 2013; Rahmawati, 2025). Kondisi ini ditandai dengan kesulitan mengenali huruf dan memproses bahasa secara fonologis, yang menurut Oktamarina dkk. (2022) dan Peterson dkk. (2013), sering kali muncul dalam bentuk hambatan membedakan simbol. Penelitian terbaru oleh Jasira dkk. (2023b) serta Robaa dkk. (2024) menunjukkan bahwa analisis tulisan tangan melalui metode deep learning berbasis CNN dan LSTM memiliki potensi besar dalam mendeteksi pola-pola khas tersebut. Namun, keterbatasan dataset dan tingginya variasi gejala tetap menjadi tantangan utama dalam membangun sistem yang robust dan generalizable (Jasira dkk., 2023b; Spoon dkk., 2019).
Mengapa Tim Memilih Proyek Ini
Tim memilih proyek ini karena memiliki dampak sosial yang signifikan dalam mendukung deteksi dini disleksia secara lebih cepat, objektif, dan mudah diakses. Dengan memanfaatkan teknologi deep learning dan analisis citra, sistem yang dikembangkan diharapkan dapat menjadi alat bantu early screening, bukan diagnosis final, sehingga dapat digunakan oleh orang tua dan pendidik sebagai langkah awal sebelum pemeriksaan lebih lanjut. Selain itu, proyek ini juga relevan secara teknis karena menggabungkan computer vision, machine learning, dan explainable AI dalam satu solusi yang realistis untuk dikembangkan dalam skala tim kecil.
B.	Cakupan Proyek dan Hasil Kerja
Cakupan Proyek
Proyek ini berfokus pada pengembangan sistem early screening disleksia berbasis analisis citra tulisan tangan. Sistem yang dibangun akan menerima input berupa foto tulisan tangan, kemudian melakukan proses preprocessing seperti konversi grayscale, resizing, dan normalisasi sebelum dianalisis menggunakan model machine learning berbasis Convolutional Neural Network (CNN) yang dikembangkan dan dilatih dari awal menggunakan TensorFlow Functional API. Hasil dari sistem berupa label klasifikasi (indikasi disleksia atau non-disleksia) serta skor probabilitas sebagai tingkat keyakinan model, disertai interpretasi sederhana untuk membantu pemahaman pengguna.  
Batasan dalam proyek ini adalah penggunaan data berupa gambar statis tanpa mempertimbangkan aspek temporal seperti urutan penulisan, serta fokus pada analisis visual tanpa mengandalkan metode OCR berbasis teks. Sistem yang dikembangkan tidak ditujukan sebagai alat diagnosis medis, melainkan sebagai alat bantu early screening yang dapat digunakan oleh orang tua atau pendidik sebagai langkah awal sebelum pemeriksaan lebih lanjut. Selain itu, pengembangan dilakukan dengan memanfaatkan dataset terbatas yang tersedia secara publik dan ditingkatkan melalui teknik augmentasi, sehingga hasil sistem lebih difokuskan pada fungsionalitas dan kelayakan implementasi dalam skala proyek tim kecil.
Cakupan Tanggung Jawab
Cakupan tanggung jawab dalam tim dibagi ke dalam tiga peran utama sesuai dengan keahlian masing-masing, Yaitu sebagai berikut:
1.	Full-Stack Web Developer
●	Mengembangkan UI untuk upload gambar handwriting (web-based).
●	Membuat halaman hasil prediksi (label + skor confidence).
●	Integrasi API backend menggunakan networking call (Axios) untuk proses request–response inference
●	Validasi input (format & ukuran gambar).
●	Optimasi UX agar mudah digunakan oleh non-teknis (orang tua).
●	Mengelola alur: upload → preprocessing → model → output.
●	Integrasi model ML ke backend (model serving).
●	Logging dan error handling.
●	Deployment frontend dan backend ke hosting sederhana.

2.	Artificial Intelligence
●	Mengembangkan model CNN sebagai baseline untuk klasifikasi handwriting.
●	Implementasi pendekatan CNN dengan penggabungan metode Neural Network lain untuk mengakomodasi sequence huruf atau kata (opsional jika waktu cukup dan apabila berpengaruh signifikan terhadap akurasi model).
●	Melatih model menggunakan dataset yang telah diproses.
●	Hyperparameter tuning dan monitoring overfitting.
●	Evaluasi model dengan memilih metrik evaluasi yang sesuai dan visualisasi pergerakan metrik evaluasi model.
●	Implementasi Explainable AI sederhana (Grad-CAM) atau metode lain untuk interpretasi hasil prediksi.
●	Implementasi custom loss dan custom callback agar model lebih akurat.
●	Membangun REST API untuk inference model dengan flask atau infrastruktur sejenis.
●	Optimasi model agar ringan untuk deployment.
3.	Data Scientist
●	Mengumpulkan dan kurasi dataset handwriting (dyslexic vs non-dyslexic).
●	Melakukan labeling data (binary atau multi-class sederhana).
●	Implementasi preprocessing dan data augmentation (rotasi, scaling, resizing).
●	Menangani data imbalance dan kualitas data.
●	Split dataset (train/validation/test).
●	Analisis pola kesalahan tulisan (EDA) seperti letter reversal, spacing, dan ukuran huruf.
●	Membuat insight dari hasil prediksi dan validasi terhadap hipotesis awal.
●	Dokumentasi eksperimen dan hasil analisis.
●	Mengembangkan dashboard interaktif Streamlit untuk EDA, serta evaluasi dan interpretasi model.
Cakupan Proyek dan Milestone
1.	Persiapan Dataset dan Preprocessing
●	Durasi: 13 – 19 April
●	Penanggung Jawab: Data Scientist
●	Tugas: Mengumpulkan dataset handwriting (dyslexic vs non-dyslexic), melakukan eksplorasi sumber dataset, kurasi dan labeling data, serta melakukan preprocessing meliputi resizing, augmentasi, dan analisis awal pola kesalahan tulisan seperti letter reversal, spacing, dan ukuran huruf untuk mendukung pemahaman karakteristik data.
●	Hasil:
○	Dataset siap pakai untuk training model
○	Dokumentasi proses preprocessing dan data wrangling
○	Insight awal pola data
●	Target: Dataset bersih, terstruktur, dan siap digunakan untuk modeling
2.	Pengembangan Model Deep Learning
●	Durasi: 20 – 26 April
●	Penanggung Jawab: AI Engineer
●	Tugas: Mendesain arsitektur model CNN menggunakan TensorFlow Functional API, kemudian melakukan training model berbasis dataset yang telah diproses, termasuk eksperimen variasi arsitektur, implementasi custom loss function dan custom callback untuk meningkatkan performa, serta melakukan evaluasi dan tuning model berdasarkan metrik evaluasi model.
●	Hasil:
○	Model terlatih (format .keras / SavedModel)
○	Laporan evaluasi (accuracy, precision, recall, F1-score)
●	Target: Model siap untuk tahap integrasi
3.	Pengembangan Backend & API
●	Durasi: 27 April – 3 Mei
●	Penanggung Jawab: Full-Stack Developer
●	Tugas: Membangun REST API menggunakan Flask atau framework sejenis untuk menangani alur inference model, termasuk upload gambar, preprocessing request, integrasi model deep learning ke backend, serta pengelolaan response hasil prediksi berupa probabilitas dan label klasifikasi.
●	Hasil:
○	Endpoint API untuk inference model
○	Dokumentasi API
○	Sistem backend yang terhubung dengan model
●	Target: Backend berjalan dan API dapat diakses
4.	Pengembangan Frontend (UI/UX)
●	Durasi: 4 – 10 Mei
●	Penanggung Jawab: Full-Stack Developer
●	Tugas: Mengembangkan antarmuka web untuk upload gambar handwriting, menampilkan hasil prediksi berupa label dan confidence score, serta menyediakan visualisasi sederhana seperti highlight area penting dari model atau hasil Explainable AI. Selain itu melakukan integrasi frontend dengan backend menggunakan networking call untuk komunikasi API secara real-time.
●	Hasil:
○	Halaman upload gambar
○	Halaman hasil prediksi (label + confidence score)
○	Integrasi UI dengan backend
●	Target: Frontend terintegrasi dengan backend
5.	Integrasi Sistem & Testing
●	Durasi: 11 – 17 Mei
●	Penanggung Jawab: Seluruh Tim
●	Tugas: Melakukan integrasi end-to-end antara frontend, backend, dan model machine learning, melakukan pengujian sistem secara menyeluruh, debugging error, validasi hasil prediksi, serta perbaikan berdasarkan hasil testing untuk memastikan sistem berjalan stabil dan konsisten.
●	Hasil:
○	Laporan testing dan bug fixing
○	Sistem yang berjalan stabil
●	Target: Sistem siap untuk finalisasi
6.	Finalisasi & Dokumentasi Proyek
●	Catatan: Fase ini berada di luar cakupan utama pengembangan, dan difokuskan pada penyelesaian akhir proyek serta kebutuhan submission.
●	Durasi: 18 Mei – 4 Juni
●	Penanggung Jawab: Seluruh Tim
●	Tugas: Menyusun dokumentasi akhir proyek, membuat slide presentasi, video demo penggunaan sistem, serta finalisasi seluruh komponen aplikasi termasuk perbaikan minor sebelum submission.
●	Hasil:
○	Slide presentasi
○	Video demo & tutorial penggunaan
●	Target: Proyek selesai dan siap dikumpulkan
C.	Jadwal Pengerjaan

Jadwal Pengerjaan
+----------+-------------------------------------+-------+-------+-------+
| Division |           Milestone/Task            | April |  Mei  | Juni  |
|          |                                     | 1 2 3 4| 1 2 3 4| 1 2 |
+----------+-------------------------------------+-------+-------+-------+
| SEMUA    | Inisialisasi Proyek & Perumusan Ms. | B B . .| . . . .| . . |
| SEMUA    | Finalisasi scope dan alur sistem    | . B . .| . . . .| . . |
|          | CHECKPOINT 1                        | . G . .| . . . .| . . |
+----------+-------------------------------------+-------+-------+-------+
| DS       | Eksplorasi sumber dataset           | . R R .| . . . .| . . |
| DS       | Kurasi dan pelabelan data           | . . R R| . . . .| . . |
| DS       | Analisis awal pola kesalahan        | . . R R| . . . .| . . |
| DS       | Dashboard Streamlit (EDA awal)      | . . . R| . . . .| . . |
+----------+-------------------------------------+-------+-------+-------+
| AI       | Desain arsitektur model CNN         | . . . .| Y Y . .| . . |
| AI       | Training & eksperimen model         | . . . .| Y Y . .| . . |
| AI       | Evaluasi & tuning model             | . . . .| Y Y . .| . . |
|          | CHECKPOINT 2                        | . . . .| . G . .| . . |
+----------+-------------------------------------+-------+-------+-------+
| FS       | Setup backend & desain API          | . . . .| . O O .| . . |
| FS       | Integrasi model ke layanan backend  | . . . .| . O O .| . . |
| FS       | Pengembangan Antarmuka Pengguna     | . . . .| . . T T| . . |
| FS       | Desain tampilan upload & hasil      | . . . .| . . T T| . . |
| FS       | Integrasi frontend dengan API       | . . . .| . . T T| . . |
+----------+-------------------------------------+-------+-------+-------+
| SEMUA    | Pengujian alur sistem end-to-end    | . . . .| . . . B| B . |
| SEMUA    | Evaluasi hasil dan perbaikan        | . . . .| . . . B| B . |
| SEMUA    | Pengujian akhir                     | . . . .| . . . .| B . |
| DS       | Penyusunan Dashboard Streamlit Final| . . . .| . . . .| P P |
| SEMUA    | Penyusunan slide presentasi         | . . . .| . . . .| P P |
| SEMUA    | Pembuatan video demo & tutorial     | . . . .| . . . .| P P |
| SEMUA    | Finalisasi dokumen & submission     | . . . .| . . . .| . P |
|          | CHECKPOINT 3                        | . . . .| . . . .| . G |
| SEMUA    | Presentasi Website & Peer Review    | . . . .| . . . .| . G |
+----------+-------------------------------------+-------+-------+-------+

Keterangan Kode Warna:
B = Biru (Persiapan/Testing)   R = Merah (Data Science)
G = Hijau (Checkpoint/Final)   Y = Kuning (AI/Modeling)
O = Oranye (Backend/FS)        T = Toska (Frontend/FS)
P = Pink (Dokumentasi)         . = Kosong


D.	Uraian Rencana Penugasan/Job Desk Setiap Learning Path
	Pembagian tugas dalam tim disusun berdasarkan tiga learning path utama, yaitu Full-Stack Web Developer, Artificial Intelligence, dan Data Science, yang saling terintegrasi dalam pengembangan sistem secara end-to-end.
	Full-Stack Web Developer bertanggung jawab dalam pengembangan antarmuka aplikasi berbasis web, termasuk fitur upload gambar handwriting dan tampilan hasil prediksi berupa label klasifikasi dan confidence score. Selain itu, sistem dapat menyediakan dukungan visualisasi tambahan seperti Explainable AI apabila memungkinkan. Peran ini juga mencakup integrasi frontend dengan backend melalui REST API serta pengelolaan alur request–response inference.
	Artificial Intelligence bertugas merancang dan mengembangkan model berbasis Convolutional Neural Network (CNN) untuk mendeteksi indikasi disleksia dari tulisan tangan. Proses ini meliputi training model, eksperimen dan tuning hyperparameter, evaluasi performa menggunakan berbagai metrik, serta implementasi Explainable AI seperti Grad-CAM atau metode lain untuk memberikan interpretasi hasil prediksi. Model yang telah dilatih kemudian disiapkan dalam format siap produksi agar dapat diintegrasikan ke dalam sistem backend. Selain itu, pembuatan arsitektur model penerjemah tulisan berbasis CNN untuk memetakan foto tulisan penderita disleksia ke tulisan huruf normal.
	Sementara itu, Data Scientist berperan dalam memastikan kualitas dan kesiapan data yang digunakan dalam pengembangan model. Tugas utamanya meliputi pengumpulan dan kurasi dataset handwriting, proses data wrangling seperti cleaning dan labeling, serta melakukan Exploratory Data Analysis (EDA) untuk mengidentifikasi pola kesalahan tulisan seperti inkonsistensi spacing, variasi ukuran huruf, dan ketidakteraturan bentuk tulisan. Selain itu, Data Scientist juga bertanggung jawab dalam menangani permasalahan data seperti ketidakseimbangan kelas serta mendokumentasikan insight yang diperoleh dari proses analisis.
E.	Sumber Daya Proyek
	Sumber daya yang digunakan dalam pengembangan proyek ini mencakup beberapa komponen utama yang saling terintegrasi untuk mendukung proses pembangunan sistem secara end-to-end:
1.	Bahasa Pemrograman
a.	Python: Digunakan untuk pengembangan model machine learning, preprocessing data, serta layanan inference model menggunakan Flask.
b.	JavaScript: Digunakan untuk membangun antarmuka pengguna (frontend) dan backend API menggunakan Node.js serta integrasi dengan layanan machine learning.
2.	Framework
a.	(Frontend Tools)
1)	React/Vue.js: Digunakan untuk membangun UI berbasis komponen yang interaktif dan responsif.
2)	Vite: Digunakan sebagai module bundler untuk membangun dan mengoptimasi aplikasi frontend selama proses development dan build.
b.	(Backend Tools)
1)	Node.js: Digunakan sebagai runtime environment untuk menjalankan backend berbasis JavaScript.
2)	Express.js:  Digunakan untuk membangun RESTful API utama yang menangani request dari frontend, termasuk proses upload gambar dan pengelolaan response.
3)	Flask: Digunakan sebagai layanan khusus (microservice) untuk menjalankan model machine learning (inference), yang terintegrasi dengan backend utama melalui REST API.
3.	API & Integrasi Sistem (RESTful API): Berfungsi sebagai penghubung antara frontend dan backend, serta sebagai media komunikasi antara Express dan Flask dalam proses inference model secara real-time.
4.	Dataset (Dataset Handwriting Dyslexia (Public Dataset + Augmentasi): Digunakan sebagai data utama untuk melatih model dalam mengenali pola tulisan tangan yang mengindikasikan disleksia. Dataset akan diperkaya melalui teknik augmentasi seperti rotasi ringan (±5–10 derajat), scaling, dan translasi kecil, dengan menghindari transformasi yang dapat mengubah makna visual tulisan seperti flipping horizontal untuk meningkatkan variasi data.
5.	Tools Kolaborasi & Manajemen
a.	Github: Digunakan untuk version control dan kolaborasi kode antar anggota tim.
b.	Google Docs & Google Drive: Digunakan untuk dokumentasi dan penyimpanan file proyek.
c.	Vercel / Netlify: Digunakan untuk deployment frontend agar aplikasi dapat diakses secara online.
d.	Google Colab: Digunakan untuk menjalankan kode, eksperimen, dan pengolahan data secara online.
e.	Kaggle: Digunakan untuk mencari dataset, melakukan analisis data, serta eksperimen machine learning.
f.	Streamlit: Digunakan untuk membangun dan menyebarkan (deploy) dashboard interaktif untuk visualisasi data dan evaluasi model.
g.	Discord: Digunakan untuk koordinasi tim, pengingat deadline, dan komunikasi harian.
h.	SQLite: Digunakan sebagai database ringan untuk menyimpan hasil prediksi, logging input gambar, serta mendukung proses debugging sistem.
F.	Rencana Manajemen Risiko dan Isu
Dalam pengembangan proyek ini, terdapat beberapa risiko yang berpotensi menghambat jalannya pengerjaan maupun mempengaruhi kualitas hasil akhir sistem yang dikembangkan. Salah satu risiko utama adalah keterbatasan dataset handwriting disleksia yang relatif sedikit dan kurang beragam, sehingga dapat berdampak pada kemampuan generalisasi model dalam mengenali pola tulisan tangan yang bervariasi. Untuk mengatasi hal ini, tim akan memanfaatkan teknik data augmentation seperti rotasi ringan, scaling, dan translasi, serta menggabungkan beberapa sumber dataset publik dengan tetap memperhatikan konsistensi distribusi data, sehingga variasi data dapat meningkat tanpa mengubah karakteristik visual utama dari tulisan tangan.
Selain itu, terdapat risiko overfitting pada model machine learning akibat keterbatasan variasi data yang tersedia. Model berpotensi hanya menghafal pola pada data training tanpa mampu melakukan generalisasi dengan baik pada data baru. Oleh karena itu, proses pelatihan akan dilengkapi dengan pembagian dataset yang jelas (train, validation, test), monitoring performa model secara berkala, serta penerapan teknik seperti regularisasi, dropout, dan early stopping untuk menjaga keseimbangan antara akurasi dan kemampuan generalisasi model.
Risiko lain juga muncul pada tahap integrasi sistem antara frontend, backend berbasis Express, dan layanan machine learning berbasis Flask, yang berpotensi menimbulkan error saat proses inference berlangsung. Perbedaan format data, ketidaksesuaian preprocessing, maupun kegagalan komunikasi antar layanan dapat menyebabkan hasil prediksi tidak akurat atau bahkan sistem tidak berjalan. Untuk mengantisipasi hal ini, tim akan melakukan pengujian API secara bertahap, memastikan konsistensi format request–response, dan menjaga stabilitas aplikasi.
Dari sisi manajemen waktu, durasi pengerjaan yang terbatas menjadi tantangan tersendiri yang dapat menyebabkan tidak semua fitur dapat diimplementasikan secara optimal. Oleh karena itu, tim akan berfokus pada pengembangan Minimum Viable Product (MVP) dengan memprioritaskan fitur utama, yaitu klasifikasi tulisan tangan berbasis CNN, serta memastikan sistem berjalan dengan stabil sebelum mempertimbangkan pengembangan fitur tambahan.
Aspek lain yang perlu diperhatikan adalah kualitas input dari pengguna, di mana gambar tulisan tangan yang kurang jelas, buram, atau tidak sesuai dengan kondisi data training dapat mempengaruhi hasil prediksi model. Untuk itu, sistem akan dilengkapi dengan validasi input serta pipeline preprocessing yang terstandarisasi agar konsistensi hasil tetap terjaga.
Terakhir, terdapat risiko kesalahan interpretasi hasil oleh pengguna yang menganggap sistem sebagai alat diagnosis medis. Untuk itu, disediakan disclaimer bahwa sistem hanya berfungsi sebagai alat bantu early screening dan tidak menggantikan diagnosis profesional. Dengan mitigasi ini, pengembangan diharapkan lebih terarah dan menghasilkan sistem yang stabil. 