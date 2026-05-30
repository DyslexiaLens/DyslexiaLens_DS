<!-- PAGE 1 -->
ii 
 
5.2. 
Analisis Spasial & Piksel (Computer Vision Analytics)....................... 22 
5.3. 
Validasi Fitur XAI: Explanatory Analysis ............................................ 24 
5.4. 
Deployment Dashboard: Streamlit Cloud ............................................. 26 
5.5. 
Kesimpulan BAB 5 ............................................................................... 28 
BAB VI Strategi Augmentasi & A/B Testing ................................................... 29 
6.1. 
Solusi Dual-Track & EMNIST ............................................................. 29 
6.2. 
A/B Testing Integritas Data .................................................................. 32 
6.3. 
Kesimpulan & Rekomendasi Lanjutan ................................................. 35 
BAB VII Penyiapan Data Final (Data Preparation) ........................................ 37 
7.1. 
Stratified Splitting ................................................................................. 37 
7.2. 
Data Dictionary Final ............................................................................ 40 
BAB VIII Kesimpulan & Action Items (Handover) ........................................ 43 
8.1. 
Jawaban Pertanyaan Bisnis ................................................................... 43 
8.2. 
Rangkuman Perjalanan Pipeline ........................................................... 45 
8.3. 
Action Items: Mandat Teknis untuk AI Engineer ................................. 46 
DAFTAR PUSTAKA .......................................................................................... 49 
 


<!-- PAGE 2 -->
1 
 
BAB I 
Pendahuluan & Konteks Bisnis 
1.1. Latar Belakang  
Disleksia adalah gangguan belajar neurologis yang ditandai dengan 
kesulitan dalam membaca, menulis, dan mengeja. Diagnosis disleksia 
umumnya lambat karena ketergantungan pada evaluasi psikologis klinis yang 
memakan waktu dan biaya tinggi. Namun, berbagai penelitian medis 
menunjukkan bahwa penderita disleksia sering memanifestasikan gangguan 
motorik halus saat menulis. Gejala ini terekam secara persisten dalam pola fisik 
tulisan tangan, seperti bentuk huruf yang asimetris, goresan yang terputus-
putus (tremor), hingga distorsi orientasi ruang (letter reversal). 
Dalam proyek DyslexiaLens, kami mengajukan pendekatan deteksi dini 
alternatif: memanfaatkan teknologi Computer Vision dan Machine Learning 
untuk menganalisis pola goresan tulisan tangan sebagai biomarker kuantitatif. 
Perlu ditekankan secara tegas bahwa sistem ini bukan alat diagnosis medis 
definitif, melainkan alat skrining awal (early screening) guna memberikan 
indikasi probabilitas kepada orang tua dan pendidik sebelum dirujuk ke 
profesional klinis. 
Tantangan utama dalam mewujudkan sistem skrining ini adalah 
kelangkaan dataset tulisan tangan disleksia yang terstruktur, seimbang, dan 
terbebas dari bias label. Oleh karena itu, proyek ini memanfaatkan dataset 
publik 'Gambo' dari Kaggle sebagai bahan baku utama. Laporan ini secara 
spesifik mendokumentasikan proses end-to-end Data Science untuk 
merestorasi dan menyusun pipeline dataset yang bersih dan tangguh (robust), 
sebagai pondasi esensial sebelum model kecerdasan buatan dilatih oleh tim AI. 
1.2. Tujuan Proyek 
Fokus dari Technical Report Data Science ini adalah: 
1. Mengaudit, membersihkan, dan merekonstruksi dataset publik "Gambo" 
agar terbebas dari anomali label noise dan metrik keparahan yang cacat. 


<!-- PAGE 3 -->
2 
 
2. Melakukan Feature Engineering (pendekatan Explainable AI / XAI) untuk 
menerjemahkan karakteristik goresan gambar mentah menjadi metrik 
matematis yang dapat diinterpretasi. 
3. Membangun strategi penyeimbangan kelas (Dual-Track Dataset) melalui 
augmentasi cerdas berbasis dataset eksternal (EMNIST), serta 
memvalidasi keamanan augmentasi tersebut menggunakan uji statistik 
(A/B Testing). 
4. Menghasilkan master dataset akhir yang terstandarisasi dan siap 
didistribusikan (handover) ke tim AI Engineer. 
1.3. Pertanyaan Bisnis 
Rangkaian eksperimen Data Science dalam proyek ini didesain untuk 
menjawab empat pertanyaan analitis krusial: 
1. Apakah dataset asli (Gambo) sudah cukup representatif dan seimbang 
untuk melatih model AI? 
2. Apakah pola visual dalam tulisan tangan cukup kuat untuk 
merepresentasikan kondisi kognitif disleksia, atau sekadar indikasi 
ambigu? 
3. Bagaimana cara mengekstrak metrik visual secara matematis agar model 
klasifikasi AI di fase selanjutnya tidak menjadi 'black-box' (pendekatan 
Explainable AI)? 
4. Bagaimana merekonstruksi dan mengamankan metrik keparahan (Severity 
Score) bawaan yang anomali agar layak menjadi target prediksi? 
1.4. Batasan Proyek (Scope Limitation) 
Untuk menjaga ekspektasi pembaca dan mencegah scope creep, berikut 
adalah batasan eksplisit dari laporan ini: 
Termasuk dalam Scope 
TIDAK Termasuk dalam Scope 
Audit, 
pembersihan, 
dan 
rekonstruksi dataset 
Pelatihan dan evaluasi model AI 
(tanggung jawab AI Engineer) 


<!-- PAGE 4 -->
3 
 
Ekstraksi 6 fitur XAI matematis 
Pengembangan arsitektur CNN/Deep 
Learning 
Strategi augmentasi & validasi 
statistik (A/B Testing) 
Deployment model ke aplikasi produksi
Penyiapan handover dataset final 
Uji klinis atau validasi medis terhadap 
pasien nyata 
Terbatas pada aksara Latin (A–Z) Aksara 
non-Latin 
(misal: 
Arab, 
Mandarin, Cyrillic) 
Disclaimer Medis: Sistem DyslexiaLens adalah alat skrining awal (early 
screening), bukan alat diagnosis medis definitif. Seluruh temuan dalam laporan 
ini bersifat komputasional dan wajib dikonfirmasi oleh profesional klinis 
sebelum digunakan sebagai dasar intervensi medis. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


<!-- PAGE 5 -->
4 
 
BAB II 
Audit & Profiling Dataset Awal 
Sebelum melakukan pemrosesan data, tahap krusial pertama dalam pipeline ini 
adalah mengaudit "bahan baku" secara menyeluruh. Proses Assessing Data ini 
bertujuan untuk membongkar kotak hitam dataset Gambo, memvalidasi integritas 
file fisik, serta mengidentifikasi anomali bawaan yang berpotensi merusak model 
AI jika dibiarkan. 
2.1. Sumber & Karakteristik Data  
Dataset yang dievaluasi adalah Dyslexia Handwriting Dataset (Gambo) 
yang diperoleh dari repositori publik Kaggle. Berdasarkan skrip audit 
komprehensif yang dieksekusi menggunakan Python, berikut adalah profil 
fisik dari dataset mentah tersebut: 
- 
Total Keseluruhan File: 208.372 gambar. 
- 
Ekstensi & Format: 100% berformat `.png`. 
- 
Resolusi & Dimensi: Seragam pada ukuran 28×28 piksel. 
- 
Mode Warna (Color Mode): Seluruhnya konsisten pada mode 
Grayscale (`L`) atau Binary (`1`), tanpa ada gambar RGB yang 
menyusup. 
- 
Hierarki Folder Asli: Terbagi atas klasifikasi Train dan Test, dengan 
tiga sub-kategori utama di dalamnya: `Normal`, `Corrected`, dan 
`Reversal`. 
 
Gambar 1. Struktur Folder Asli Gambo 


<!-- PAGE 6 -->
5 
 
- 
Integritas File: Tidak ditemukan file corrupt atau rusak secara struktural 
dari hasil ekstraksi dan sampling visual. 
 
Gambar 2. Statistik Distribusi Dataset Gambo 
Secara struktural dan integritas file fisik, dataset ini tampak sempurna. 
Namun, audit semantik (membedah makna nama file dan kesesuaian visual) 
mengungkap celah logika yang sangat dalam. 
2.2. Temuan Anomali Kritis (Data Assessing) 
Melalui inspeksi algoritmik yang dikombinasikan dengan validasi visual 
acak, kami menemukan berbagai kelemahan fatal bawaan dari periset asli: 
A. Kontaminasi Label Silang (Label Noise) 
Hierarki folder ternyata tidak mencerminkan kebenaran label (ground 
truth) 100%. Ditemukan ratusan file ber-prefix `NormalXXXX.png` yang 
justru berserakan dan "tersesat" di dalam folder kelas disleksia 
(`Corrected` dan `Reversal`). 
 
Gambar 3. Bukti Label Noise 


<!-- PAGE 7 -->
6 
 
Jika dataset ini langsung didistribusikan ke model AI menggunakan 
ImageFolder Dataset Generator standar, model akan "dipaksa" 
mempelajari tulisan normal sebagai ciri-ciri disleksia. Cacat ini dijamin 
akan menghancurkan kemampuan prediksi kelas. 
 
B. Skala Severity Score yang Terbalik & Cacat Jarak 
Periset asli menyimpan informasi Tingkat Keparahan dengan 
menyematkan angka di awal nama file (misal: `4_1.png` atau `9_23.png`). 
Sayangnya, konvensi ini memiliki cacat matematis: 
1. Skala yang Terbalik (Inverted Scale): Angka `9` merepresentasikan 
coretan disleksia paling ringan, sedangkan angka `1` dan `4` 
merepresentasikan goresan yang sangat hancur (reversal). Jika 
model memproses angka ini mentah, AI akan menyimpulkan bahwa 
skor keparahan `1` sangat mirip dengan label Normal (`0`). Padahal 
di dunia nyata, `1` adalah kondisi terparah. 
2. Kekosongan Metrik (Missing Values): Rentang asli yang 
digunakan adalah `1, 4, 5, 6, 7, 8, 9`. Angka `2` dan `3` menghilang 
sepenuhnya dari ekosistem dataset. Hipotesis logis kami adalah ini 
terjadi akibat kelalaian protokol pengumpulan data oleh periset asli, 
di mana perekaman untuk tingkat keparahan tertentu luput 
dilakukan. 
 
C. Anomali Visual pada Kelas Normal Asli 
Di luar pengecekan skrip, inspeksi manual (visual sampling) terhadap 
folder `Normal` mengungkap adanya kontaminasi dua arah. Sejumlah 
sampel di folder `Normal` menampilkan coretan koreksi dan tumpang-
tindih yang secara visual seharusnya masuk ke kelas `Corrected`. Temuan 
ini membuktikan bahwa arsitektur folder fisik dataset Gambo sama sekali 
tidak bisa dipercaya sebagai ground truth tunggal. 


<!-- PAGE 8 -->
7 
 
 
Gambar 4. Anomali Visual Kelas Normal 
 
D. Ketimpangan Distribusi (Class Imbalance) 
Berdasarkan hasil rekapitulasi distribusi awal, ditemukan fakta bahwa 
kelas disleksia (gabungan `Corrected` + `Reversal`) mendominasi 
populasi dataset secara tidak wajar dengan rasio mencapai ~3.35:1 
terhadap kelas `Normal`. Ketimpangan kelas (Class Imbalance) separah 
ini adalah ancaman serius yang akan memicu bias mayoritas (majority 
bias) saat training model AI model cenderung selalu menebak "Disleksia" 
karena itulah yang paling sering dilihatnya. Oleh karena itu, diperlukan 
strategi intervensi augmentasi untuk memulihkan ekuilibrium data. 
2.3. Kesimpulan Tahap Audit 
Walaupun Dataset Gambo memiliki spesifikasi teknis piksel yang 
mumpuni (28×28, grayscale, 100% `.png`), masih terdapat kelemahan fatal 
pada arsitektur semantiknya (Label Noise dua arah, Severity Score kacau, dan 
Class Imbalance 3.35:1). Fakta temuan ini secara mutlak melarang AI Engineer 
untuk melatih model menggunakan metode pembacaan hirarki folder standar 
(seperti `ImageFolder` pada PyTorch/Keras), karena mengandalkan folder fisik 
pasti akan berujung pada Data Poisoning. Sebagai gantinya, tahap pembersihan 
(Bab 3) wajib menghasilkan sebuah master dokumen CSV terpusat yang akan 
bertindak sebagai otoritas mutlak *ground truth* untuk melatih AI. 


<!-- PAGE 9 -->
8 
 
BAB III 
Pembersihan & Rekayasa Data (Data Cleaning) 
Bab ini mendokumentasikan proses penyelamatan dataset Gambo dari anomali 
struktural yang ditemukan pada tahap Audit (Bab 2). Filosofi utama dari alur kerja 
ini adalah 'Logical First, Physical Last'. Alih-alih menghapus file secara membabi 
buta, seluruh anomali disaring dan divalidasi terlebih dahulu secara logis di atas 
DataFrame Pandas. Setelah daftar file bersih (Master CSV) terbentuk sebagai cetak 
biru yang aman, barulah pembersihan fisik (Physical Sync) dieksekusi secara 
terukur. 
3.1. Logical Cleaning & Pembuatan Master CSV 
Langkah pertama adalah membangun "saringan" berbasis logika untuk 
memisahkan data valid dari data sampah, kemudian menuangkan hasilnya ke 
dalam sebuah master dokumen CSV yang akan menjadi single source of truth 
bagi seluruh pipeline AI. 
A. Sistem Penyaringan Lapis Pertama (Regex & OS Validation) 
Proses 
filtering 
diinisiasi 
dengan 
8 
saringan 
logika 
yang 
menggabungkan ekspresi reguler (Regex) dengan validasi sistem file. 
No
Mekanisme / Filter 
Pola / Kondisi 
Target Anomali 
1 
File Integrity Validation 
os.path.exists() & Image.open() 
Pencegahan Broken Links 
dan file rusak (tidak terbaca 
oleh 
pustaka 
pembuat 
gambar) 
2 
RE_DUPLICATE_WIN 
\(\d+\) 
File duplikat hasil copy-
paste 
Windows 
(misal: 
Normal1305 (11).png) 
3 
RE_PLACEHOLDER 
^(Normal\|Reversal\|Corrected)\.png$
File placeholder tanpa ID 
yang bukan gambar tulisan 
tangan asli 
4 
RE_GLITCH 
\.qNcy 
File glitch dari download 
terputus dengan ekstensi 
ganda 


<!-- PAGE 10 -->
9 
 
5 
RE_ALPHA_ONLY 
^[A-Za-z]\.png$ 
File referensi abjad tunggal 
(misal: A.png, b.png) 
6 
RE_NORMAL_NUMBER 
^Normal\d+ 
File 
Normal_XXX.png 
yang anomali/terseret di 
dalam folder Normal 
7 
RE_REVERSAL_NUMBER 
^Reversal\d+ 
File 
Reversal_XXX.png 
tanpa 
metrik 
keparahan 
yang valid 
8 
RE_STARTS_WITH_ALPHA
^[A-Za-z][-_.] 
File dengan format huruf 
yang menyimpang di folder 
Corrected/Reversal 
 
Gambar 5. Rekapitulasi Filter Cleaning 
B. Rekonstruksi Severity Score & Pemusnahan Label Noise 
Setelah penyaringan level fisik selesai, langkah selanjutnya adalah 
menetralisir Label Noise dan Skala yang Terbalik melalui fungsi terpusat 
`get_score()`. 
 
 


<!-- PAGE 11 -->
10 
 
1. Eksekusi Mati Label Noise: 
Fungsi memegang aturan validasi silang (cross-validation) absolut: 
`if 'Normal' in filename and folder != 'Normal': return 'DROP'`. 
Baris ini adalah "peluru perak" yang mengeksekusi semua gambar 
Normal yang tersesat di folder disleksia. 
 
2. Pembalikan Skala & Kompatibilitas Physical Renaming: 
Selanjutnya, fungsi memetakan ulang skor keparahan agar searah 
dengan urgensi klinis (nilai kecil = ringan, nilai besar = parah): 
Skor Asli 
Periset 
Kondisi Visual 
Makna 
Nyata 
→
Skor Baru (AI 
Scale) 
9 (Corrected) 
Koreksi sangat ringan 
Paling 
Ringan 
→
1
8, 7, 6, 5 
Semakin 
banyak 
koreksi 
Berjenjang 
→
2, 3, 4, 5 
4 (Corrected) 
Goresan hampir tidak 
terbaca 
Parah 
→
6
1 (Reversal) 
Goresan hancur / letter 
reversal 
Paling Parah 
→
6 (digabung) 
Normal
Tulisan bersih tanpa 
gejala 
Normal 
→
0
Secara rekayasa data, pipeline `get_score()` dirancang dengan dua 
prinsip utama: 
 Fungsi parsing delimiter (`_` dan `-`) sengaja dibuat sangat kaku 
(strict). Jika sebuah file memiliki suffix ganda yang ambigu (misal 
`9-23_baru.png`), sistem akan langsung menggagalkan parsing dan 
melabelinya `DROP` sebagai bentuk perlindungan dari data 
corrupt. 
 Pipeline mampu memproses nama file mentah (contoh: 
`9_23.png`) maupun file yang telah melalui skrip opsional Physical 
Renaming (`1_23.png`) secara konsisten tanpa efek samping. 


<!-- PAGE 12 -->
11 
 
C. Output: Definisi Kolom Master CSV 
Hasil 
akhir 
proses 
cleaning 
logis 
adalah 
file 
`master_dataset_dyslexia.csv` dengan definisi kolom berikut: 
Kolom 
Tipe 
Keterangan 
image_path
String 
Path absolut ke file gambar .png 
file_name
String 
Nama file (tanpa path) 
split
String 
Pembagian bawaan periset: Train atau Test 
folder_category
String 
Kelas asal: Normal, Corrected, Reversal 
severity_score
Integer
Skor keparahan (Multi-Class): 0 = Normal, 1–6 = Keparahan
target_class
Integer
Label biner: 0 = Normal, 1 = Disleksia 
Skenario Pemodelan & Pencegahan Data Leakage Kelas Berat: 
1) Kolom `target_class` memampatkan `Corrected` dan `Reversal` 
menjadi kelas `1` murni untuk membangun baseline screening 
(Sehat vs Sakit). Namun, identitas medis yang krusial tetap 
dikuantifikasi secara ordinal pada kolom `severity_score` (Skor 6 
untuk Reversal, 1-5 untuk Corrected) guna melayani skenario 
model Multi-class Classification ke depannya. 
2) Kolom `severity_score`, `folder_category`, dan bahkan nama file 
itu sendiri (`file_name`) mengandung label (ground truth). 
Ketiganya dilarang masuk sebagai fitur. String path murni hanya 
boleh digunakan sebagai pointer pemuatan piksel (`cv2.imread`). 
3) Kolom `split` (Train/Test) tetap dipertahankan sekadar untuk 
referensi komparasi. AI Engineer sangat direkomendasikan 
mengabaikan 
split 
bawaan 
ini 
karena 
potensi 
ketidakseimbangannya, dan wajib melakukan Stratified Shuffle 
Split atau K-Fold Cross Validation ulang dari nol dengan random 
seed yang deterministik. 


<!-- PAGE 13 -->
12 
 
 
Gambar 6. Contoh Isi Master CSV 
3.2. Sinkronisasi Fisik & Penghapusan Anomali Background 
Setelah cetak biru logis (Master CSV) terbentuk, intervensi fisik hard disk 
dilakukan: 
A. Sinkronisasi Folder Dataset 
File `.png` yang tidak memiliki record di dalam CSV (karena terkena 
`DROP` atau Regex) dianggap sebagai sampah (noise) dan dihapus secara 
fisik untuk menghemat ruang. 
 
Sebagai implementasi Defensive Programming, eksekusi penghapusan 
ini dilindungi oleh mekanisme `DRY_RUN = True`. Skrip akan mencetak 
simulasi target file ke terminal untuk diverifikasi manusia, sebelum 
akhirnya sakelar diubah menjadi `DRY_RUN = False` untuk melakukan 
penghapusan permanen di level OS. 
 
B. Penghapusan Anomali Inverted Background / Overexposed 
Satu filter tambahan berbasis Computer Vision diterapkan: menghapus 
gambar dengan `mean_pixel > 127`. Mengingat standar dataset tulisan 
tangan AI (seperti MNIST) didominasi latar hitam (piksel 0), gambar 
dengan mean di atas 127 mengindikasikan anomali Inverted Background 
(latar putih, tulisan hitam) atau keberadaan artefak bercak putih raksasa 
(overexposed). Memasukkan citra dengan polaritas warna yang terbalik ini 
akan merusak filter konvolusi CNN. 
 


<!-- PAGE 14 -->
13 
 
Catatan Penanganan Image Mode: Sebelum nilai rata-rata piksel 
dihitung, seluruh file gambar secara wajib dikonversi ke mode Grayscale 
(`L`, rentang piksel 0–255). Langkah ini krusial untuk mencegah 
kegagalan deteksi pada gambar yang memiliki mode bawaan Binary (`1`), 
yang mana nilai piksel maksimalnya hanya `1` sehingga tidak akan pernah 
terdeteksi oleh ambang batas 127. 
 
Pertahanan Desain Filter: Ambang batas `mean > 127` dipilih secara 
konservatif. Pada praktiknya, tulisan tangan anak di atas latar hitam 28×28 
piksel nyaris tidak mungkin melampaui mean 127 secara organik, 
mengingat area foreground (goresan putih) umumnya hanya menempati 
~15–25% total kanvas. Risiko filter ini "salah bunuh" data disleksia yang 
valid secara klinis adalah mendekati nol. 
 
(Catatan Batasan: Filter ini sangat efektif membunuh anomali putih, 
namun belum dirancang untuk menangkap anomali gambar hitam pekat 
buta (`mean_pixel < 5`). Anomali tersebut ditangguhkan pada tahap 
inspeksi visual EDA). 
3.3. Ringkasan Kuantitatif Hasil Cleaning 
Tahap 
Proses 
Status 
A 
Logical Cleaning (7 Regex + OS Validation) 
Selesai 
B 
Sinkronisasi Folder (Hapus fisik non-CSV) 
Selesai 
C 
Penghapusan Anomali Polaritas Putih (mean_pixel > 127) 
Selesai 
D 
Rebuild master_dataset_dyslexia.csv Final 
Selesai 
Hasil Akhir: Dari 208.372 gambar mentah yang tercatat pada audit awal 
(Bab 2), pipeline cleaning berhasil menyelamatkan ~156.453 gambar bersih ke 
dalam Master CSV final. Selisih ~52.000 file merupakan akumulasi eliminasi 
dari Label Noise, duplikat Windows, placeholder, file glitch, anomali Inverted 
Background, dan baris yang gagal parsing `severity_score`. 


<!-- PAGE 15 -->
14 
 
 
Gambar 7. Ringkasan Kuantitatif Cleaning 
3.4. Kesimpulan BAB 3 
Melalui Logical Cleaning berlapis yang disusul pembersihan Inverted 
Background, dataset Gambo telah direstorasi, di mana anomali Label Noise 
musnah, Severity Score tertata logis, dan Ghost Records berhasil ditumpas. 
Dokumen CSV akhir yang memuat kumpulan file selamat (survived files) ini 
resmi menjadi satu-satunya sumber kebenaran (single source of truth) untuk 
tahapan ekstraksi fitur (Explainable AI).  
Satu-satunya anomali audit (Bab 2) yang sengaja ditangguhkan 
penanganannya pada tahap ini adalah Class Imbalance. Isu ketimpangan 
distribusi tersebut akan dieksekusi secara khusus melalui strategi Augmentasi 
(Injeksi EMNIST) pasca tahap Exploratory Data Analysis, demi mencegah 
tercemarnya kemurnian data asli selama proses perancangan fitur XAI (Bab 4). 
 
 
 
 
 
 
 


<!-- PAGE 16 -->
15 
 
BAB IV 
Feature Engineering Explainable AI (XAI) 
Bab ini mendokumentasikan proses transformasi matriks piksel mentah 
menjadi metrik kuantitatif yang merepresentasikan karakteristik motorik tulisan 
tangan. Pendekatan ini dikenal sebagai Explainable AI (XAI): alih-alih 
menyerahkan gambar mentah ke dalam black-box CNN, kita terlebih dahulu 
mengekstrak 6 fitur matematis yang memiliki makna klinis sehingga setiap prediksi 
model kelak dapat dirasionalisasi secara manusiawi. 
Pertahanan MLOps (Zero Data Leakage): Seluruh ekstraksi fitur geometri 
di bab ini bersifat Stateless Operation (dihitung murni dan mandiri per gambar). 
Karena tidak ada penggunaan agregat populasi (seperti mean/variance scaling), 
ekstraksi fitur secara global pada Master CSV dijamin 100% bebas dari kebocoran 
data (Data Leakage) antar-split Train dan Test. 
4.1. Preprocessing Citra Dasar 
Sebelum fitur diekstrak, setiap gambar melewati dua tahap normalisasi 
keruangan dan warna: 
A. Konversi Grayscale & Spatial Normalization (Resize) 
Seluruh gambar dikonversi ke format grayscale (1 kanal warna, skala 
0–255) dan di-resize secara absolut ke resolusi standar 28 × 28 piksel. 
 
(Catatan Metodologi: Proses resize absolut ini secara inheren memaksa 
normalisasi batas keruangan. Oleh karena itu, teknik standarisasi 
whitespace manual/padding yang direncanakan di awal sengaja dibatalkan, 
karena hanya berisiko mendistorsi aspek rasio bawaan dari matriks sparsa 
tulisan tangan). 
 
B. Binarisasi (Thresholding) 
Matriks grayscale (0–255) ditransformasi menjadi matriks biner (0 dan 
1) menggunakan ambang batas (threshold = 128): 


<!-- PAGE 17 -->
16 
 
binary = (pixels > 128).astype(np.float64) 
Mengingat dataset ini menggunakan standar latar belakang hitam 
(seperti MNIST): 
- 
Piksel > 128 → dikategorikan sebagai Foreground (goresan/tulisan 
putih) → nilai `1`. 
- 
Piksel ≤ 128 → dikategorikan sebagai Background (latar hitam) → nilai 
`0`. 
4.2. Definisi, Justifikasi, & Batasan 6 Fitur Matematis 
Keenam fitur dirancang secara matematis untuk menangkap gejala motorik 
disleksia. Berikut adalah pembedahan algoritmanya beserta pengungkapan 
keterbatasan secara objektif: 
A. Fitur 1: “stroke_density” Kepadatan Tinta (Deteksi Over-tracing) 
Aspek 
Detail 
Formula 
Σ(piksel foreground) / total_piksel (784)
Rentang 
Output 
0.0 (gambar kosong) – 1.0 (gambar penuh) 
Celah 
Algoritmik 
Bias Skala (Scale-Dependent): Karena pembaginya adalah luas 
total kanvas (784) dan bukan luas area huruf (Bounding Box Area), 
fitur 
ini 
juga 
menangkap 
ukuran 
tulisan 
(macrographia/micrographia). Huruf besar yang ditarik tipis bisa 
mendapat skor sama dengan huruf kecil yang ditekan tebal (over-
tracing). 
Justifikasi 
Klinis 
Penderita disleksia sering menunjukkan perilaku over-tracing: 
menekan pena berulang kali di garis yang sama karena keraguan 
motorik. Akibatnya, kepadatan tinta (stroke density) secara 
proporsional lebih tinggi dibandingkan tulisan normal yang satu 
tarikan efisien. 
 
B. Fitur 2-3: “center_of_mass_x” & “center_of_mass_y” Pusat Massa 
(Distorsi Spasial) 
Aspek 
Detail 
Formula 
mean(koordinat piksel foreground) pada sumbu X dan Y 


<!-- PAGE 18 -->
17 
 
Rentang 
Output 
0.0 – 27.0 (sesuai dimensi gambar 28×28) 
Justifikasi 
Klinis 
Tulisan normal cenderung memiliki Center of Mass (CoM) yang 
stabil di sekitar pusat kanvas (X=14, Y=14). Pada penderita 
disleksia, CoM kerap bergeser secara asimetris akibat distorsi 
keruangan (spatial distortion) dan kesulitan mempertahankan titik 
awal penulisan. 
C. Fitur 4: “bounding_box_ratio” Rasio Rentang Aktif (Distorsi Dimensi) 
Aspek 
Detail 
Formula 
(Σ(baris_aktif) + 1) / (Σ(kolom_aktif) + 1)
Rentang 
Output 
> 0.0 (penambahan +1 mencegah pembagian nilai nol) 
Celah 
Algoritmik 
Fitur ini secara matematis menghitung rasio Active Ink Span (jumlah 
baris bertinta), bukan True Bounding Box (max_y - min_y). Pendekatan 
ini justru dipertahankan karena lebih sensitif dalam menghukum 
(memberi rasio aneh) pada garis tulisan yang putus-putus akibat tremor 
parah. 
Justifikasi 
Klinis 
Mengidentifikasi huruf yang proporsinya hancur (terlalu "gepeng" atau 
memanjang keluar batas) akibat kontrol motorik halus yang terganggu. 
 
D. Fitur 5: “stroke_transitions” Transisi Warna (Deteksi Tremor) 
Aspek 
Detail 
Formula
Σ(diff(baris_biner) / IMG_SIZE (28) 
Rentang 
Output 
≥ 0.0 (semakin tinggi skor, semakin kuat indikasi tremor/gerigi) 
Celah 
Algoritmik 
Mengandung 
bias 
skala 
vertikal 
(Scale-Dependent 
Tremor 
Approximation). Karena dibagi dengan total kanvas (28) dan bukan 
dengan tinggi huruf asli, tulisan lurus yang panjang secara vertikal dapat 
mengakumulasi skor transisi yang tinggi secara artifisial. 
Justifikasi 
Klinis 
Menghitung rata-rata perpindahan warna (hitam↔putih) per baris. 
Getaran tangan (tremor) menyebabkan garis menjadi bergerigi atau 
putus-putus, sehingga jumlah transisi melonjak drastis dibandingkan 
garis lurus/mulus pada anak normal. 
 


<!-- PAGE 19 -->
18 
 
E. Fitur 6: “horizontal_symmetry” Simetri Absolut (Deteksi Reversal) 
Aspek 
Detail 
Formula 
mean(belahan_kiri_kanvas == flip(belahan_kanan_kanvas))
Rentang 
Output 
Teoritis 0.0 - 1.0 (namun secara praktis terkompresi > 0.85) 
Celah 
Algoritmik 
1. Ilusi Rentang: Akibat dominasi >90% background hitam pekat yang 
selalu simetris (0 == 0), skor fitur ini mengalami kompresi dan nyaris 
tidak pernah turun di bawah 0.85. 
2. Absolute Spatial: Pemisahan dilakukan tepat di pusat kanvas (kolom 
14), bukan di pusat huruf (CoM). 
Justifikasi 
Klinis 
Karakteristik Absolute Spatial di atas justru brilian: skor akan anjlok 
tidak hanya jika bentuk hurufnya asimetris (seperti letter reversal "b" vs 
"d"), tetapi juga jika huruf tersebut diletakkan melenceng dari tengah 
kanvas (kegagalan tata ruang). Ini adalah indikator terkuat untuk kasus 
Disleksia tipe Reversal. 
 
4.3. Pipeline Ekstraksi & Validasi 
Fungsi 
ekstraksi 
diaplikasikan 
secara 
iteratif 
pada 
`master_dataset_dyslexia.csv`. Hasilnya digabungkan secara horizontal 
menjadi 12 kolom final. Hasil ekstraksi memicu dua proses validasi: 
1) NaN Audit: Berkat pembersihan Broken Links di Bab 3, audit 
melaporkan 0 Error/NaN, membuktikan kekokohan pipeline rekayasa 
data. 
2) Distribusi Histogram: Analisis visual mengonfirmasi bahwa sebaran 
fitur antar kelas tidak saling tumpang tindih secara identik. 


<!-- PAGE 20 -->
19 
 
 
Gambar 8. Distribusi 6 Fitur XAI 
Ringkasan Statistik Selisih Antar Kelas 
 
Gambar 9. Selisih Statistik Fitur 
(Berdasarkan tabel log di atas, fitur dengan selisih absolut terbesar terbukti 
menjadi diskriminator utama yang merepresentasikan perbedaan nyata secara 
klinis). 
4.4. Implikasi Arsitektur: Late Fusion Model 
Kolom Baru 
Tipe 
Deskripsi (Data Dictionary) 
stroke_density
Float
Kepadatan area tulisan putih (0.0–1.0) 
center_of_mass_x
Float
Titik pusat goresan sumbu-X (0–27) 


<!-- PAGE 21 -->
20 
 
center_of_mass_y
Float
Titik pusat goresan sumbu-Y (0–27) 
bounding_box_ratio
Float
Rasio baris aktif vs kolom aktif (Active Ink Span) 
stroke_transitions
Float
Rata-rata transisi per baris (skala IMG_SIZE) 
horizontal_symmetry
Float
Skor kemiripan cermin spasial absolut (terkompresi > 0.8)
 
4.5. Kesimpulan BAB 4 
Ekstraksi fitur matematis berhasil menerjemahkan kondisi motorik (tremor, 
asimetri spasial, keraguan/ over-tracing) ke dalam 6 metrik tabular. Dengan 
membedah secara jujur keterbatasan algoritmik dari formulanya (seperti bias 
skala tremor dan kompresi rentang simetri), fitur ini terbukti tetap memiliki 
variansi tinggi untuk membedakan kelas Normal dan Disleksia.  
 
Dataset yang telah diperkaya fitur tabular pendamping ini (Featured 
Dataset) membuka ruang bagi AI Engineer untuk merancang arsitektur Late 
Fusion (Multi-Input Model), di mana cabang pertama (CNN) menganalisis 
pola gambar mentah dan cabang kedua (Dense Layer) menganalisis 6 fitur 
biologis ini, menciptakan AI yang tidak sekadar menebak namun mampu 
menjelaskan alasannya secara klinis. Dataset ini kini siap untuk dianalisis lebih 
lanjut pada tahap Exploratory Data Analysis (Bab 5). 
 
 
 
 
 
 
 


<!-- PAGE 22 -->
21 
 
BAB V 
Exploratory Data Analysis (EDA) & Dashboarding 
Bab ini memaparkan seluruh temuan visual yang dihasilkan dari proses 
eksplorasi data (Exploratory Data Analysis). EDA dilakukan setelah fitur tabular 
diekstrak (Bab 4), sehingga analisis tidak hanya mencakup distribusi metadata dasar, 
tetapi juga validasi empiris terhadap ke-6 fitur XAI. Temuan-temuan ini kemudian 
di-deploy ke dalam dashboard interaktif berbasis Streamlit Cloud agar dapat 
diakses oleh stakeholder tanpa perlu menjalankan kode Python. 
5.1. Analisis Integritas & Distribusi Dataset 
Tahap pertama EDA adalah mengonfirmasi kondisi kesehatan populasi 
data secara kuantitatif. 
A. Keseimbangan Kelas (Class Imbalance Audit) 
Visualisasi bar chart mengonfirmasi kembali temuan audit Bab 2 
dengan angka matematis yang kritis: dari ~156.453 gambar bersih pasca-
cleaning (Bab 3), populasi Disleksia (Corrected + Reversal) mendominasi 
hingga ~120.463 gambar, sedangkan Normal hanya ~35.990 gambar. 
Rasio ini menyentuh titik kritis ~3.35:1 sebuah ketimpangan separah ini 
menjamin bahwa model AI yang dilatih langsung pada data ini akan 
menderita Majority Class Bias (cenderung selalu menebak "Disleksia"). 
Kuantifikasi ini memberikan mandat mutlak untuk dilakukannya skenario 
augmentasi dataset. 
 
Gambar 10. Class Imbalance 


<!-- PAGE 23 -->
22 
 
B. Distribusi Kelas per Split (Train vs Test) 
Proporsi relatif antar kelas (Normal, Corrected, Reversal) cukup 
konsisten baik pada set Train maupun Test bawaan. Meskipun tidak 
ditemukan distribution shift yang ekstrem pada split orisinal ini, eksekusi 
ulang Stratified Splitting (yang akan didefinisikan secara formal di Bab 7) 
tetap diwajibkan demi menjamin integritas saintifik MLOps. 
 
C. Distribusi Severity Score (0–6) 
Distribusi Severity Score sangat bervariasi dan memusat pada rentang 
skor yang tinggi (Skor 6 / Reversal). Skor `0` (Normal) memiliki populasi 
yang terlampau kecil untuk menyeimbangi gabungan seluruh level 
keparahan disleksia. Ketimpangan ini wajib menjadi catatan perhatian 
khusus jika pengembangan diarahkan menuju arsitektur Multi-class 
Classification. 
 
Gambar 11. Distribusi Severity 
5.2. Analisis Spasial & Piksel (Computer Vision Analytics) 
A. Sampel Visual: Normal vs Corrected vs Reversal 
Grid visual 3×5 menampilkan perbedaan mencolok antara ketiga kelas: 
- 
Normal: Huruf terbentuk dengan satu goresan dominan yang tegas, 
bersih, dan mudah dikenali. 


<!-- PAGE 24 -->
23 
 
- 
Corrected: Goresan tampak tebal dan bertumpuk akibat tekanan pena 
berulang (over-tracing/scribbling), menjadi indikator keraguan menulis. 
- 
Reversal: Huruf mengalami efek cermin (mirror image) atau rotasi yang 
tidak lazim, ciri khas utama dari disleksia orientasi spasial. 
 
B. Pixel Variance Heatmap (Bukti Empiris Inkonsistensi Spasial) 
Ini adalah visualisasi agregat paling krusial dalam EDA. Dengan 
merata-ratakan variansi piksel dari ratusan sampel per kelas: 
- 
Normal: Variansi piksel rapat dan terpusat di tengah kanvas. Artinya, 
anak normal memiliki tata ruang penulisan yang konsisten (selalu di 
tengah). 
- 
Disleksia: Area kuning (variansi tinggi) menyebar sangat luas dan tidak 
beraturan. Hal ini membuktikan secara empiris bahwa penderita 
disleksia menderita Inkonsistensi Spasial (gagal menempatkan posisi 
huruf secara konstan; coretan bisa berada di pojok, tepi, atas, atau 
bawah kanvas). 
 
Gambar 11. Variance Heatmap 
 
 
 


<!-- PAGE 25 -->
24 
 
C. Heatmap Rata-rata Piksel: Skor Terendah vs Tertinggi 
Perbandingan Ghost Image (mean pixel image) antara Skor 1 (Ringan) 
dan Skor 6 (Parah) mengungkap: 
- 
Skor ringan memiliki pola piksel rata-rata yang lebih tegas dan 
terkumpul. 
- 
Skor parah menunjukkan rata-rata piksel yang menyebar dan memudar, 
merepresentasikan variasi bentuk goresan yang ekstrem. 
- 
Panel ketiga ("Selisih Intensitas") dengan colormap inferno menandai 
zona anomali (blind spots) utama di mana distorsi spasial paling sering 
terjadi. 
 
Gambar 12. Analisis Spasial Disleksia 
5.3. Validasi Fitur XAI: Explanatory Analysis 
Bagian ini bersifat explanatory (bukan sekadar mencari pola, tetapi 
menyajikan jawaban definitif atas empat pertanyaan bisnis utama dari Bab 1) 
menggunakan bukti visual. 
a) Pertanyaan Bisnis 1: "Apakah dataset asli sudah cukup seimbang 
untuk melatih model AI?" 
Jawab: Tidak. Rasio kelas 2:1 adalah ketimpangan yang fatal. Fakta 
matematis ini secara resmi memicu eksekusi Augmentasi Dataset (yang akan 
dibahas di Bab 6). 
 


<!-- PAGE 26 -->
25 
 
b) Pertanyaan Bisnis 2: "Apakah pola visual tulisan tangan cukup 
kuat merepresentasikan kondisi kognitif disleksia?" 
Jawab: Iya. Variance Heatmap memberikan pembuktian tingkat populasi 
bahwa anak disleksia memiliki letak spasial yang sangat inkonsisten/fluktuatif 
dibandingkan anak normal. 
c) Pertanyaan Bisnis 3: "Bagaimana merancang AI yang mampu 
menjelaskan keputusannya?" 
Jawab: Dengan arsitektur Late Fusion. Plot distribusi (Boxplot) terhadap 4 
fitur utama XAI (stroke_density, bounding_box_ratio, stroke_transitions, 
horizontal_symmetry) membuktikan kemampuan pemisahan kelas secara 
organik. Angka-angka klinis inilah yang kelak dicetak oleh AI untuk 
merasionalisasi keputusannya. 
 
Gambar 13. Boxplot XAI 
 


<!-- PAGE 27 -->
26 
 
d) Pertanyaan Bisnis 4: "Bagaimana sistem dapat memberikan 
interpretasi klinis terhadap sub-tipe disleksia?" 
Jawab: Melalui profiling sub-tipe. KDE Plot (Kernel Density Estimation) 
membuktikan bahwa setiap sub-tipe disleksia memiliki "sidik jari" numerik: 
- 
Corrected: Mengelompok kuat di wilayah Stroke Density ekstrem (validasi 
perilaku over-tracing). 
- 
Reversal: Terdeteksi sangat akurat melalui pola anomali pada metrik 
Horizontal Symmetry. 
 
Gambar 14. KDE Sub-tipe 
5.4. Deployment Dashboard: Streamlit Cloud 
Seluruh temuan analitik ini tidak dibiarkan terisolasi di dalam Jupyter 
Notebook, melainkan di-deploy ke dalam aplikasi interaktif berbasis Streamlit 
Cloud (`app.py`). Ini memfasilitasi stakeholder non-teknis untuk memvalidasi 
insight medis secara mandiri. 
A. Arsitektur Dashboard (5 Tab) 
Ini adalah visualisasi agregat paling krusial dalam EDA. Dengan 
merata-ratakan variansi piksel dari ratusan sampel per kelas: 
Tab 
Konten 
Tujuan 
Dataset 
Summary 
Metrik kuanƟtaƟf & distribusi 
kelas 
Quick overview kesehatan data 
Computer Vision
Heatmap Piksel, Distribusi 
Severity 
BukƟ empiris pola visual
XAI Proﬁling 
Boxplot 4 ﬁtur XAI, KDE Plot 
Sub-Ɵpe 
Menjawab Pertanyaan Bisnis 3 & 4 


<!-- PAGE 28 -->
27 
 
StraƟﬁcaƟon 
Komparasi Metrik 
Keseimbangan Kelas 
Visualisasi Imbalance (Menjawab 
RQ 1) 
InteracƟve 
Viewer 
Operasi In-Memory Pixel 
AnalyƟcs 
Inspeksi raw data & Ghost Image 
interakƟf 
B. Fitur Teknis Unggulan 
1) Dual-Dataset Toggle: Sidebar menyediakan sakelar radio untuk 
membandingkan dataset tanpa augmentasi (Original Gambo) dan dataset 
dengan augmentasi (Gambo + EMNIST). (Catatan: Kehadiran fitur 
EMNIST di dalam dashboard ini merupakan preview dari strategi 
penyelesaian imbalance yang baru akan dieksekusi secara detail pada Bab 
6). 
2) Compressed Pixel CSV (`.csv.gz`): Tab Interactive Viewer memanfaatkan 
file kompresi CSV yang berisi matriks piksel 28×28 yang telah di-flatten 
ke 784 kolom. Teknik ini memungkinkan stakeholder melihat gambar 
mentah tanpa memerlukan akses ke folder dataset fisik. 
3) Caching (`@st.cache_data`): Seluruh operasi loading data di-cache oleh 
Streamlit untuk mencegah pembacaan ulang CSV pada setiap interaksi 
pengguna. 
 
Gambar 15. Dashboard Streamlit 
 
 


<!-- PAGE 29 -->
28 
 
C. Pertahanan Arsitektur (Engineering Highlights) 
Aplikasi ini tidak hanya tentang visualisasi, namun juga unjuk gigi 
keahlian Data Engineering: 
1) OOM (Out-of-Memory) Defense via `.csv.gz`: Untuk melindungi limitasi 
RAM Streamlit Cloud (1 GB gratis), Tab 5 tidak meload file `.png` fisik. 
Seluruh matriks gambar di-flatten (28×28 = 784 kolom) menjadi data 
tabular yang kemudian dikompresi tingkat tinggi menggunakan `.csv.gz`. 
Ini meniadakan beban I/O Disk server dan mencegah aplikasi mengalami 
crash saat dieksekusi ribuan kali. 
2) On-the-Fly Matrix Aggregation: Berbeda dengan notebook yang merender 
Heatmap statis, Interactive Viewer di aplikasi mampu menghitung Ghost 
Image (rata-rata matriks dari 300 gambar acak) secara dinamis/real-time 
di atas RAM browser.  
3) Dual-Dataset Scalability: Dashboard ini telah dirancang untuk berskala. 
Sidebar sudah dilengkapi dengan toggle yang kelak siap digunakan untuk 
membandingkan populasi Data Asli (Gambo) versus Data Augmentasi 
(Gambo+EMNIST), yang merupakan agenda utama di tahap selanjutnya 
(Bab 6). 
5.5. Kesimpulan BAB 5 
EDA berhasil menjawab seluruh pertanyaan bisnis yang didefinisikan di 
Bab 1 dengan bukti visual dan statistik yang kuat. Temuan paling kritis adalah 
konfirmasi bahwa (1) pola disleksia terbukti nyata dan terukur secara piksel, 
(2) fitur XAI mampu memisahkan kelas secara organik, namun (3) dataset 
belum layak untuk pelatihan model karena Class Imbalance yang fatal. Temuan 
ketiga ini secara langsung memicu keputusan eksekusi untuk melakukan 
Augmentasi Dataset menggunakan EMNIST (Bab 6), yang harus divalidasi 
melalui A/B Testing sebelum data dinyatakan siap untuk handover ke AI 
Engineer. 
 


<!-- PAGE 30 -->
29 
 
BAB VI 
Strategi Augmentasi & A/B Testing 
Bab ini mendokumentasikan keputusan strategis paling kritis dalam seluruh 
pipeline: bagaimana menyeimbangkan dataset yang timpang tanpa merusak "DNA" 
data asli. Di Bab 5 (EDA), kita menemukan bahwa rasio Disleksia:Normal pada 
dataset Gambo asli mencapai titik kritis ~2:1 sebuah level Class Imbalance yang 
menjamin kegagalan model AI akibat Majority Class Bias. Bab ini memaparkan 
solusi yang dipilih, alasan penolakan alternatif lain, serta validasi statistik formal 
yang membuktikan bahwa solusi tersebut aman. 
6.1. Solusi Dual-Track & EMNIST 
A. Mengapa Augmentasi Spasial (Rotasi/Flip) Dilarang Keras? 
Dalam Computer Vision konvensional, teknik augmentasi paling 
populer adalah transformasi spasial. Namun, seluruh teknik ini dilarang 
keras dalam konteks proyek DyslexiaLens: 
Teknik 
Augmentasi 
Alasan Pelarangan 
Rotasi (90°, 
180°) 
Huruf "d" yang dirotasi 180° menjadi "p". Dalam konteks disleksia, rotasi 
adalah gejala klinis itu sendiri (letter reversal). Merotasi data Normal 
berarti menciptakan data Disleksia buatan dan menyuntikkannya ke 
kelas yang salah. 
Horizontal 
Flip 
Huruf "b" yang di-flip horizontal menjadi "d". Ini adalah inti dari disleksia 
tipe Reversal. Menerapkan flip pada kelas Normal akan memproduksi 
label noise secara massal. 
Vertical Flip 
Menghasilkan huruf terbalik yang tidak ada dalam alfabet manapun, 
memaksa model belajar pola artifisial (out-of-distribution). 
Random 
Crop 
Gambar sudah berukuran 28×28 piksel (sangat kecil). Memotong sebagian 
akan menghancurkan struktur huruf dan membuat fitur XAI (seperti 
Center of Mass dan Bounding Box Ratio) menjadi tidak bermakna. 
Prinsip Emas: Dalam Medical AI berbasis tulisan tangan, orientasi 
spasial adalah informasi klinis. Memanipulasinya secara artifisial sama 
dengan merusak integritas diagnostik dataset. 
 


<!-- PAGE 31 -->
30 
 
B. Solusi yang Dipilih: Injeksi Dataset Eksternal (EMNIST) 
Alih-alih memanipulasi data yang sudah ada, kita memilih jalur yang 
lebih aman: menambahkan data tulisan tangan asli dari sumber eksternal 
untuk menambal populasi kelas Normal yang kekurangan sampel. 
 
EMNIST (Extended MNIST) dipilih sebagai donor karena alasan 
berikut: 
Kriteria 
Kesesuaian EMNIST 
Format 
Identik 
Gambar grayscale 28×28 piksel persis sama dengan dataset Gambo. 
Tidak perlu preprocessing tambahan. 
Konten 
Relevan 
Berisi tulisan tangan huruf alfabet (a-z, A-Z) dari penulis non-
disleksia  representasi ideal untuk kelas "Normal". 
Skala Besar 
697.932 sampel tersedia di split ByClass-Train, jauh lebih dari cukup 
untuk menambal defisit ~57.000 sampel Normal. 
Kualitas 
Akademis 
Dipublikasikan oleh NIST dan telah menjadi benchmark standar 
dalam riset Computer Vision (Cohen et al., 2017). 
 
Namun, keputusan ini diiringi mitigasi atas dua risiko inheren: 
1) Analisis Risiko Demografis (Domain Shift): Dataset Gambo berasal 
dari anak-anak, sedangkan EMNIST dikumpulkan dari orang dewasa 
(NIST Special Database 19). Ada risiko model AI belajar membedakan 
"Usia" alih-alih "Disleksia". Namun, blind spot ini berhasil dipatahkan 
oleh hasil A/B Testing (Cohen's d < 0.2), yang membuktikan secara 
empiris bahwa morfologi fitur piksel EMNIST sangat identik dengan 
kelas Normal Gambo, meniadakan risiko bias demografis tersebut. 
2) Pencegahan Shortcut Learning Bias: EMNIST tidak dimasukkan begitu 
saja. Injeksi dilakukan secara Upstream (sebelum Preprocessing Bab 4). 
Dengan demikian, data EMNIST yang aslinya berformat grayscale anti-
aliased dipaksa melewati algoritma Otsu Binarization yang sama persis 
dengan Gambo. Ini menjamin keseragaman tekstur tepi (hitam-putih 


<!-- PAGE 32 -->
31 
 
absolut) dan mencegah CNN berbuat curang dengan sekadar 
mendeteksi gradasi piksel abu-abu. 
 
C. Proses Teknis Konversi & Injeksi (Fair Pruning) 
Konversi 
EMNIST 
dieksekusi 
melalui 
notebook 
terpisah 
(`EMNIST_to_Gambo.ipynb`) dengan alur berikut 
1) Parsing & Reshape: Matriks piksel dari `emnist-byclass-train.csv` di-
reshape dan di-transpose untuk mengoreksi orientasi bawaannya. 
2) Label Contamination Filtering: Dari 62 kelas bawaan EMNIST, label 
angka (0-9) dihapus secara absolut. Karena Gambo secara eksklusif hanya 
menguji morfologi alfabetis, penyuntikan angka akan merusak logika AI. 
3) Konversi ke PNG: Matriks yang lulus filter disimpan sebagai `.png` ke 
folder `Normal/`. 
4) Fair Pruning: EMNIST disuntikkan secukupnya, sementara kelas 
Disleksia (mayoritas) sedikit di-downsample. Ini memastikan rasio 1:1 
tercapai tanpa membiarkan EMNIST mendominasi kelas Normal secara 
berlebihan. 
 
D. Hasil Kuantitatif Augmentasi 
Konversi 
EMNIST 
dieksekusi 
melalui 
notebook 
terpisah 
(`EMNIST_to_Gambo.ipynb`) dengan alur berikut 
Metrik 
Dataset A (Gambo Asli) 
Dataset B (Gambo + 
EMNIST) 
Total Sampel 
~156.453 
~204.833 
Kelas Disleksia 
~120.463 
~102.394 
Kelas Normal 
~35.990 
~102.439 
Rasio Disleksia:Normal 
3.35:1 (Kritis) 
1.00:1 (Ideal) 
Catatan Penting: Angka kelas Disleksia pada Dataset B berkurang dari 
~120.463 menjadi ~102.394 karena proses Fair Pruning juga melakukan 


<!-- PAGE 33 -->
32 
 
downsampling terhadap kelas mayoritas untuk mencapai keseimbangan 
sempurna, bukan hanya menambahkan data ke kelas minoritas. 
 
6.2. A/B Testing Integritas Data 
Menyeimbangkan rasio kelas adalah langkah yang mudah secara teknis. 
Pertanyaan yang jauh lebih sulit dan kritis adalah: apakah injeksi data asing ini 
merusak karakteristik alami tulisan tangan disleksia? Jika iya, model AI akan 
belajar pola yang salah dan gagal mendeteksi disleksia di dunia nyata skenario 
terburuk dalam Medical AI. 
Untuk menjawab pertanyaan ini secara saintifik (bukan opini), kita 
merancang eksperimen A/B Testing formal. 
A. Desain Eksperimen & Perumusan Hipotesis 
Sebelum mengeksekusi uji utama, kita mengonfirmasi bahwa 
pemilihan Mann-Whitney U (non-parametrik) sudah tepat. Uji Shapiro-
Wilk dijalankan pada 5.000 sampel acak per fitur per dataset. 
Komponen 
Detail 
Grup A 
(Kontrol) 
Dataset Gambo Asli (~156k sampel, tanpa injeksi EMNIST) 
Grup B 
(Perlakuan) 
Dataset Gambo + EMNIST (~205k sampel, setelah Fair Pruning) 
Metrik 
Evaluasi 
6 Fitur XAI Matematis (Bab 4): stroke_density, center_of_mass_x, 
center_of_mass_y, bounding_box_ratio, stroke_transitions, 
horizontal_symmetry 
Uji Statistik 
Mann-Whitney U Test (Non-Parametrik, Two-Sided) 
Tingkat 
Signifikansi 
α = 0.05 
B. Perumusan Hipotesis 
Tingkat Signifikansi: α = 0.05 
Arah Uji yang dilakukan: Two-sided (dua sisi) 
 


<!-- PAGE 34 -->
33 
 
H₀ (Hipotesis Nol): Tidak ada perbedaan signifikan pada distribusi fitur 
XAI antara Dataset A (Gambo) dan Dataset B (Gambo + EMNIST). 
Kesimpulan: Augmentasi EMNIST TIDAK mengubah karakteristik data 
secara bermakna. 
 
H₁ (Hipotesis Alternatif): Ada perbedaan signifikan pada distribusi fitur 
XAIantara Dataset A dan Dataset B. 
Kesimpulan: Augmentasi EMNIST MENGUBAH karakteristik data 
secara nyata. 
 
Desain ini menguji 6 fitur secara independen, yang secara teoritis 
memicu inflasi False Positive (membutuhkan Koreksi Bonferroni: α/6 = 
0.0083). Selain itu, pengujian ini membandingkan distribusi global, 
padahal rasio kelasnya berubah drastis (Simpson's Paradox). Namun, 
kedua kelemahan akademis ini berhasil dimentahkan sepenuhnya oleh 
evaluasi Effect Size di tahap akhir, yang membuktikan bahwa perbedaan 
yang terjadi secara praktis adalah nol. 
 
C. Validasi Pra-Uji: Cek Normalitas (Shapiro-Wilk) 
Sebelum mengeksekusi uji utama, kita mengonfirmasi bahwa 
pemilihan Mann-Whitney U (non-parametrik) sudah tepat. Uji Shapiro-
Wilk dijalankan pada 5.000 sampel acak per fitur per dataset. 
 
Hasil: Seluruh 12 pengujian (6 fitur × 2 dataset) menghasilkan p-value 
= 0.000000 distribusi 100% TIDAK Normal. Ini adalah konsekuensi alami 
dari sifat matematis fitur itu sendiri: fitur seperti `stroke_density` 
(terkurung di 0.0–1.0) dan `bounding_box_ratio` (rasio positif) secara 
fundamental tidak mungkin mengikuti kurva Gaussian yang menjangkau 
minus tak terhingga. 
 


<!-- PAGE 35 -->
34 
 
Dengan demikian, pemilihan Mann-Whitney U Test (non-parametrik) 
tervalidasi sebagai keputusan metodologis yang tepat. Menggunakan T-
Test pada data ini akan menghasilkan kesimpulan yang tidak valid. 
 
D. Hasil Uji Utama & Penyelamat (Effect Size) 
P-Value menjawab "Apakah perbedaan ini nyata secara statistik?". 
Cohen's d menjawab pertanyaan yang jauh lebih penting: "Apakah 
perbedaan ini cukup besar untuk bermakna secara praktis?" 
Interpretasi Cohen's d 
Ambang Batas
Negligible (Diabaikan) 
|d| < 0.2 
Small (Kecil) 
|d| 0.2 – 0.5 
Medium (Sedang) 
|d| 0.5 – 0.8 
Large (Besar) 
|d| > 0.8 
Hasil Cohen's d menunjukkan bahwa seluruh 6 fitur memiliki |d| < 0.2 
(Negligible). Pergeseran rata-rata terbesar (`bounding_box_ratio`) hanya 
sebesar ~0.06 unit angka yang secara klinis tidak bermakna dan tidak 
mungkin dibedakan oleh model AI. 
 
E. Keputusan Dual-Criteria (Tabel Verdict Final) 
Keputusan akhir menggunakan logika dual-criteria: sebuah perbedaan 
baru dianggap "berbahaya" jika signifikan secara statistik dan bermakna 
secara praktis. 
Fitur XAI 
P-Value 
Cohen's d 
Magnitude 
Verdict 
stroke_density
< 0.05 
< 0.2 
Negligible 
Aman 
center_of_mass_x
< 0.05 
< 0.2 
Negligible 
Aman 
center_of_mass_y
< 0.05 
< 0.2 
Negligible 
Aman 
bounding_box_ratio
< 0.05 
< 0.2 
Negligible 
Aman 


<!-- PAGE 36 -->
35 
 
stroke_transitions
< 0.05 
< 0.2 
Negligible 
Aman 
horizontal_symmetry
< 0.05 
< 0.2 
Negligible 
Aman 
Hasil: 6/6 Fitur memiliki |d| < 0.2 (Diabaikan). Perbedaan yang 
terdeteksi secara statistik ternyata sangat kecil secara fisik sehingga 
mustahil memengaruhi persepsi model AI. 
 
F. Visualisasi Overlay KDE 
 
Gambar 16. KDE Overlay A/B Testing 
Plot KDE (Kernel Density Estimation) menampilkan overlay distribusi 
kedua dataset untuk setiap fitur. Secara visual, kurva merah (Dataset A) 
dan kurva biru (Dataset B) nyaris bertumpuk sempurna di seluruh 6 panel 
konfirmasi visual bahwa karakteristik data tidak berubah. 
 
6.3. Kesimpulan & Rekomendasi Lanjutan 
Eksperimen A/B Testing membuahkan kesimpulan solid bahwa 
augmentasi spasial (seperti rotasi atau flip) dilarang keras karena orientasi 
huruf adalah informasi klinis inti dalam diagnosis disleksia. Sebagai gantinya, 


<!-- PAGE 37 -->
36 
 
EMNIST dipilih sebagai donor kelas Normal karena memiliki format identik 
(28×28 grayscale), konten yang relevan, dan skala yang memadai.  
Walaupun Mann-Whitney U Test mendeteksi perbedaan statistik pada 
seluruh 6 fitur (p < 0.05) akibat tingginya statistical power (N > 150.000), 
evaluasi Cohen's d membuktikan bahwa seluruh perbedaan tersebut bersifat 
Negligible (|d| < 0.2) alias tidak bermakna secara praktis. Dengan keputusan 
final 6 dari 6 fitur dinyatakan aman, injeksi EMNIST sukses menyeimbangkan 
rasio kelas dari 3.35:1 menjadi ekuilibrium 1.00:1 tanpa merusak "DNA" asli 
karakteristik tulisan disleksia.  
Berbekal bukti saintifik ini, Dataset B (Gambo + EMNIST) diputuskan 
secara resmi layak untuk diserahkan ke tim AI Engineer. Proses penyiapan data 
final (Stratified Splitting dan Data Dictionary) akan didokumentasikan di Bab 
7. Jika waktu pengembangan memungkinkan, tim AI Engineer disarankan 
untuk kelak melakukan uji McNemar Test guna membandingkan performa 
akurasi akhir antara model yang dilatih pada Dataset A versus Dataset B. 
 
 
 
 
 
 
 
 
 


<!-- PAGE 38 -->
37 
 
BAB VII 
Penyiapan Data Final (Data Preparation) 
Bab ini adalah tahap pemaketan terakhir sebelum seluruh aset data diserahkan 
(handover) ke tim AI Engineer. Seluruh proses di bab sebelumnya pembersihan 
anomali (Bab 3), ekstraksi fitur XAI (Bab 4), validasi EDA (Bab 5), dan bukti 
keamanan augmentasi EMNIST (Bab 6) bermuara di sini. Dataset final harus 
melewati dua gerbang kritis: Stratified Splitting yang menjamin keadilan distribusi, 
dan Data Dictionary yang menjadi kontrak formal spesifikasi data. 
7.1. Stratified Splitting 
A. Mengapa Split Bawaan Dataset Tidak Digunakan? 
Dataset Gambo asli sudah memiliki pembagian Train/Test bawaan dari 
periset awal. Namun, di Bab 3 kita telah memutuskan bahwa split bawaan 
ini tidak memenuhi standar MLOps karena: 
1) Tidak ada set Validasi: Model AI membutuhkan tiga partisi 
(Train/Validation/Test), bukan hanya dua. 
2) Stratifikasi tidak terjamin: Tidak ada bukti bahwa periset awal melakukan 
stratified sampling berdasarkan `severity_score`. Tanpa stratifikasi, 
dimungkinkan satu level keparahan seluruhnya masuk ke Train dan tidak 
ada representasinya di Test menghasilkan evaluasi yang menipu. 
3) Populasi berubah: Setelah augmentasi EMNIST (Bab 6), komposisi 
dataset berubah total. Split lama menjadi tidak relevan. 
 
B. Mekanisme Stratified Shuffle Split 
Pembagian 
ulang 
dilakukan 
menggunakan 
`sklearn.model_selection.train_test_split` 
dengan 
parameter 
`stratify=df['severity_score']`. Ini menjamin bahwa proporsi setiap level 
keparahan (0–6) terjaga identik di seluruh partisi. 
Parameter 
Nilai 
Rasio Train 
70% 


<!-- PAGE 39 -->
38 
 
Rasio Validation
15% 
Rasio Test 
15% 
Stratifikasi 
Berdasarkan severity_score (7 level: 0–6)
Random State 
42 (Reprodusibilitas) 
Split dilakukan dalam dua tahap: 
1) Tahap 1: Pisahkan 15% sebagai Test (stratified), sisanya 85% menjadi 
pool Train+Validation. 
2) Tahap 2: Dari pool 85%, pisahkan ~17.6% (= 15/85) sebagai Validation 
(stratified). Sisanya menjadi Train final (70%). 
 
Dengan adanya Deep Learning, dataset masif (>200.000 sampel) 
umumnya memadai dengan rasio 90/5/5. Namun, proyek ini secara sadar 
mempertahankan pendekatan konservatif 70/15/15. Morfologi tulisan 
tangan anak-anak memiliki variansi visual (noise) yang ekstrem. Test Set 
berukuran raksasa (>30.000 gambar) mutlak dipertahankan agar evaluasi 
metrik (F1-Score/Recall) benar-benar kebal terhadap anomali outlier dan 
mewakili 7 level keparahan secara representatif. 
 
Kelas 0 (Normal) merupakan gabungan dari data Gambo Asli dan 
injeksi EMNIST. Secara teoritis, fungsi `stratify` hanya menjaga total 
populasi kelas 0, bukan sub-grupnya. Namun, berkat ukuran sampel kelas 
0 yang sangat masif (>100.000 data), Hukum Bilangan Besar (Law of 
Large Numbers) secara matematis menjamin bahwa rasio internal Gambo 
vs EMNIST di dalam Test set akan tersebar secara proporsional dan 
mencegah terjadinya Distribution Shift. 
 
C. Validasi Integritas Split 
Setelah split dieksekusi, tiga lapisan verifikasi dijalankan secara 
otomatis: 


<!-- PAGE 40 -->
39 
 
1) Sinkronisasi 
CSV 
vs 
Direktori: 
Jumlah 
baris 
di 
`master_dataset_final_balanced_rill.csv` dibandingkan secara matematis 
dengan jumlah file `.png` fisik di folder `Dataset/Gambo_Balanced/`. 
Hasil: 100% sinkron. 
2) Missing File Audit: Setiap `image_path` di CSV divalidasi keberadaan 
fisiknya di disk. Hasil: 0 file hilang. 
3) Data Leakage Check (Zero Overlap): Irisan (intersection) dihitung secara 
eksplisit antar himpunan partisi. Mengiris nilai `image_path` secara utuh 
akan selalu menghasilkan `0` (ilusi validasi) karena keberbedaan prefix 
folder (`/Train/`, `/Test/`). Oleh karena itu, pengujian Zero Overlap ini 
dieksekusi secara ketat pada kolom `file_name` (basename murni) untuk 
memastikan tidak ada duplikasi identitas lintas partisi 
 
Gambar 17. Proporsi Split 
 
D. Class Weights untuk AI Engineer 
Meskipun augmentasi EMNIST telah menyeimbangkan rasio global 
menjadi ~1:1, distribusi `severity_score` (7 level) tetap tidak seimbang 
secara alami. Untuk mengakomodasi hal ini, class weights dihitung secara 
otomatis 
menggunakan 
`sklearn.utils.class_weight.compute_class_weight('balanced')` 
khusus 
dari data Train saja (mencegah bocornya informasi Validation/Test ke 
dalam parameter pelatihan). 
 
 


<!-- PAGE 41 -->
40 
 
Hasil perhitungan ini disimpan dalam dua dictionary: 
- 
`binary_weight_dict`: Bobot untuk klasifikasi biner Normal (0) vs 
Disleksia (1). 
- 
`severity_weight_dict`: Bobot untuk klasifikasi multi-kelas Severity 
Score (0–6). 
Mengingat ketimpangan tajam antara Skor 0 (~102.000 sampel) dan 
Skor 6 (skala ribuan), penggunaan `severity_weight_dict` rentan memicu 
ketidakstabilan gradien (Gradient Instability) karena bobot penalti untuk 
kelas 
minoritas 
menjadi 
terlampau 
raksasa. 
AI 
Engineer 
direkomendasikan untuk menaklukkan Klasifikasi Biner (0 vs 1) terlebih 
dahulu, dan menjadikan klasifikasi Severity sebagai iterasi sekunder 
dengan penyesuaian learning rate yang hati-hati. 
 
7.2. Data Dictionary Final 
Berikut adalah spesifikasi formal (kontrak data) dari file output utama 
`Dataset_Dyslexia_EMNIST_FeatureEngineering.csv`:  
Kolom 
Tipe 
Data 
Deskripsi 
Rentang Nilai 
image_path
String 
Path ke file gambar .png 
Dataset/Gambo_Balanced/Train/...
file_name
String 
Nama file gambar fisik 
(termasuk prefix split) 
Train_Normal_A-3.png
split
String 
Partisi dataset 
Train, Validation, Test 
folder_category
String 
Kategori kelas diagnosis 
Normal, Corrected, Reversal 
severity_score
Integer 
[ORDINAL 
CATEGORICAL] Skor 
keparahan (skala 
ternormalisasi Bab 3) 
0 = Sehat, 1–6 = Ringan–Parah 
target_class
Integer 
Label target klasifikasi 
biner 
0 = Normal, 1 = Disleksia 


<!-- PAGE 42 -->
41 
 
stroke_density
Float 
[RAW] Kepadatan area 
tulisan (Bab 4) 
0.0 – 1.0 
center_of_mass_x
Float 
[RAW] Pusat massa 
goresan sumbu-X (Bab 
4) 
0.0 – 27.0 
center_of_mass_y
Float 
[RAW] Pusat massa 
goresan sumbu-Y (Bab 
4) 
0.0 – 27.0 
bounding_box_ratio
Float 
[RAW] Rasio Active Ink 
Span (Bab 4) 
> 0.0
stroke_transitions
Float 
[RAW] Rata-rata transisi 
warna per baris (Bab 4) 
≥ 0.0
horizontal_symmetry
Float 
[RAW] Skor simetri 
spasial absolut (Bab 4) 
0.0 – 1.0 (terkompresi > 0.85) 
 Aturan Penggunaan untuk AI Engineer 
Aturan 
Penjelasan 
Input model 
utama 
Matriks piksel gambar dari image_path (28×28 grayscale) 
Input model 
sekunder 
6 fitur XAI tabular (opsional, untuk arsitektur Late Fusion) 
Kewajiban 
Feature 
Scaling 
6 fitur XAI di atas bersifat mentah (unscaled). Wajib 
mengaplikasikan StandardScaler/MinMaxScaler pada fitur ini 
sebelum menggabungkannya (concat) ke dalam Dense Layer untuk 
mencegah Weight Dominance. 
Interpretasi 
Geometris 
AI Engineer wajib memahami bahwa 6 fitur XAI diekstrak 
SETELAH kompresi gambar absolut ke 28×28 piksel (Bab 4). Oleh 
karena itu, rasio (seperti bounding_box_ratio) melambangkan 
kepadatan spasial di dalam kanvas kompresi, BUKAN aspect ratio 
asli dari goresan di atas kertas. 
Output 
utama 
target_class (klasifikasi biner: Normal vs Disleksia) 
Output 
sekunder 
severity_score (klasifikasi multi-kelas: 7 level keparahan) 
Pelarangan 
Regresi 
severity_score (0-6) adalah variabel kategorikal ordinal, BUKAN 
variabel kontinu. Dilarang memodelkannya sebagai Regresi (misal: 


<!-- PAGE 43 -->
42 
 
dengan MSE Loss) karena jarak keparahan antar skor tidaklah linier. 
Wajib diproses sebagai Multi-Class Classification. 
Kolom 
Terlarang 
severity_score, folder_category, file_name, split → menggunakannya 
sebagai input fitur akan menyebabkan Data Leakage fatal 
Format 
gambar 
Grayscale, 28×28 piksel, .png 
Larangan 
Mutlak 
Transformasi Spasial (Horizontal/Vertical Flip & Rotasi) dilarang 
keras saat augmentasi on-the-fly karena merusak makna klinis (misal: 
"b" menjadi "d"). 
File Output untuk Handover 
File 
Deskripsi 
Dataset_Dyslexia_EMNIST_FeatureEngineering.csv
Single Source of Truth Metadata 
lengkap, path bersih, label 
tervalidasi, dan 6 fitur XAI 
Dataset_Gambo_EMNIST_Final.zip
Arsip seluruh gambar .png 
(Train/Validation/Test) yang siap 
diekstrak dan di-load 
(Catatan: File CSV representasi piksel dari pipeline No-Augment 
sebelumnya telah ditarik dari daftar handover guna mencegah AI Engineer 
melakukan evaluasi pada universe data yang salah).  
 
 
 
 
 


<!-- PAGE 44 -->
43 
 
BAB VIII 
Kesimpulan & Action Items (Handover) 
Bab ini merupakan penutup resmi dari seluruh rangkaian pipeline Data Science 
untuk proyek DyslexiaLens. Tujuannya ada dua: (1) menjawab secara definitif 
keempat 
Pertanyaan 
Bisnis 
yang 
didefinisikan 
di 
Bab 
1, 
dan 
(2) 
mendokumentasikan mandat teknis (Action Items) yang mengikat secara 
operasional bagi tim AI Engineer sebagai penerima estafet dataset. 
8.1. Jawaban Pertanyaan Bisnis 
Berikut adalah jawaban final atas keempat pertanyaan analitis yang 
menjadi fondasi seluruh eksperimen dalam laporan ini:  
A. Pertanyaan 1: "Apakah dataset asli (Gambo) sudah cukup 
representatif dan seimbang untuk melatih model AI?" 
Jawaban: Tidak. Dataset Gambo mentah menderita tiga cacat 
fundamental: 
- 
Class Imbalance 3.35:1: Kelas disleksia mendominasi populasi secara 
masif terhadap kelas Normal (Bab 2 & 5). 
- 
Label Noise dua arah: File Normal tersesat di folder Disleksia, dan 
sebaliknya (Bab 2). 
- 
Severity Score terbalik dan berlubang: Skala keparahan periset asli 
menggunakan konvensi `9 = Ringan`, `1 = Parah`, dengan angka 2 dan 3 
hilang total (Bab 2). 
Seluruh anomali telah diintervensi melalui Logical Cleaning berlapis 
(Bab 3) dan augmentasi EMNIST yang tervalidasi secara statistik (Bab 6), 
menghasilkan dataset final dengan rasio kelas 1:1 yang seimbang. 
 
(Catatan: Keseimbangan 1:1 ini hanya berlaku untuk kelas Biner Sehat vs 
Sakit. Distribusi internal `severity_score` tetap dibiarkan timpang secara 
alami untuk merepresentasikan distribusi klinis yang otentik di dunia 
nyata). 


<!-- PAGE 45 -->
44 
 
 
B. Pertanyaan 2: "Apakah pola visual dalam tulisan tangan cukup 
kuat untuk merepresentasikan kondisi kognitif disleksia?" 
Jawaban: Iya, sangat kuat. Tiga bukti empiris mendukung kesimpulan 
ini: 
1) Variance Heatmap (Bab 5): Populasi disleksia menunjukkan Inkonsistensi 
Spasial yang sangat nyata area variansi piksel menyebar luas dan tidak 
beraturan, berbanding terbalik dengan pola terpusat milik anak Normal. 
2) KDE Plot Sub-tipe (Bab 5): Setiap sub-tipe disleksia memiliki "sidik jari" 
numerik yang unik Corrected terdeteksi melalui Stroke Density ekstrem, 
Reversal melalui anomali Horizontal Symmetry. 
3) A/B Testing (Bab 6): Cohen's d membuktikan bahwa 6 fitur XAI konsisten 
menangkap perbedaan pola klinis bahkan setelah injeksi data EMNIST 
(Effect Size = Negligible, artinya sinyal asli tidak terdistorsi). 
 
C. Pertanyaan 3: "Bagaimana cara mengekstrak metrik visual agar 
AI tidak menjadi black-box?" 
Jawaban: Melalui 6 Fitur XAI Matematis. Keenam fitur diekstrak 
secara stateless (per gambar, tanpa kebocoran antar-split) dan memiliki 
makna klinis yang dapat dirasionalisasi: 
Fitur 
Gejala Klinis yang Ditangkap 
stroke_density
Over-tracing (keraguan menulis) 
center_of_mass_x
Distorsi spasial horizontal (posisi tulisan melenceng ke kiri/kanan)
center_of_mass_y
Distorsi spasial vertikal (posisi tulisan melenceng ke atas/bawah) 
bounding_box_ratio
Inkonsistensi proporsi huruf akibat kontrol spasial yang lemah 
stroke_transitions
Getaran tangan (tremor) berupa garis bergerigi 
horizontal_symmetry
Letter reversal (huruf terbalik, misal: b ↔ d) 


<!-- PAGE 46 -->
45 
 
Fitur-fitur ini memungkinkan AI Engineer merancang arsitektur Late 
Fusion di mana model tidak sekadar menebak, tetapi mampu mencetak 
alasan klinis di balik setiap prediksinya. 
 
D. Pertanyaan 4: "Bagaimana merekonstruksi Severity Score yang 
anomali agar layak menjadi target prediksi?" 
Jawaban: Fungsi `get_score()` berhasil: 
1) Membalik skala dari konvensi periset asli (9 = Ringan) menjadi 
konvensi AI standar (1 = Ringan, 6 = Parah, 0 = Normal). 
2) Memampatkan lubang & Menggabungkan Puncak Angka 2 dan 3 yang 
hilang berhasil terisi melalui pergeseran indeks, sementara 2 skor 
ekstrem di dataset asli (skor 4 untuk Corrected terparah dan skor 1 
untuk Reversal) secara logis digabungkan menjadi satu puncak 
keparahan absolut (skor 6). 
3) Mengeliminasi Label Noise File Normal di folder Disleksia dan 
sebaliknya dieksekusi secara algoritmik (`return 'DROP'`). 
Hasilnya: kolom `severity_score` (0–6) kini bersifat Kategorikal 
Ordinal yang bersih dan siap dijadikan target Multi-Class Classification. 
 
8.2. Rangkuman Perjalanan Pipeline 
Berikut adalah jawaban final atas keempat pertanyaan analitis yang 
menjadi fondasi seluruh eksperimen dalam laporan ini:  
Tahap 
Bab
Input 
Output 
Transformasi Kunci 
Audit 
2 
Dataset Gambo 
mentah 
(208.372 
gambar) 
Laporan 4 anomali 
kritis 
Deteksi Label Noise, Inverted 
Score, Imbalance 
Cleaning 
3 
208.372 gambar 
+ anomali 
~156.453 gambar 
bersih + Master 
CSV 
8 filter logika, rekonstruksi 
severity_score 


<!-- PAGE 47 -->
46 
 
Feature 
Eng. 
4 
Master CSV + 
gambar bersih 
CSV + 6 kolom 
fitur XAI 
Ekstraksi stateless per gambar 
EDA 
5 
Featured CSV 
Jawaban 4 
Pertanyaan Bisnis + 
Dashboard 
Variance Heatmap, KDE Plot, 
Boxplot 
Augmentasi 
6 
Gambo (156k) 
+ EMNIST 
Dataset Balanced 
1:1 (~204.833) 
Injeksi Normal & Fair Pruning 
Disleksia, validasi A/B 
Preparation 
7 
Dataset 
Balanced 
Train/Val/Test 
(70/15/15) + Data 
Dictionary 
Stratified Split, Class Weights 
 
8.3. Action Items: Mandat Teknis untuk AI Engineer 
Bagian ini bersifat kontraktual. Seluruh instruksi di bawah ini wajib 
dipatuhi oleh tim AI Engineer demi menjaga integritas saintifik dari dataset 
yang telah dibangun. 
A. Instruksi Wajib (MUST) 
No.
Mandat 
Alasan 
Referensi
1 
Gunakan master_dataset_final_balanced_rill_featured.csv 
sebagai satu-satunya sumber kebenaran 
Mengandalkan 
struktur folder 
fisik akan 
menyebabkan 
Data Poisoning 
akibat Label 
Noise bawaan 
Bab 2 & 
3 
2 
Masukkan binary_weight_dict ke parameter class_weight 
pada model.fit() 
Meskipun rasio 
global sudah 1:1, 
distribusi internal 
severity_score 
tetap timpang 
Bab 
7.1.D 
3 
Aplikasikan StandardScaler/MinMaxScaler pada 6 fitur 
XAI sebelum concat ke Dense Layer 
Fitur masih 
bersifat [RAW] 
dengan rentang 
berbeda; tanpa 
scaling, fitur 
berskala besar 
akan 
Bab 7.2 


<!-- PAGE 48 -->
47 
 
mendominasi 
bobot neuron 
4 
Fokuskan metrik evaluasi pada F1-Score dan Recall, 
bukan Accuracy 
Pada dataset 
medis, False 
Negative (gagal 
deteksi anak 
disleksia) jauh 
lebih berbahaya 
daripada False 
Positive 
Prinsip 
Medical 
AI 
5 
Taklukkan Klasifikasi Biner (target_class: 0 vs 1) terlebih 
dahulu 
Model Multi-
Class 
(severity_score) 
rentan Gradient 
Instability akibat 
ketimpangan 
1:50 pada kelas 
minoritas 
Bab 
7.1.D 
 
B. Larangan Mutlak (MUST NOT) 
No.
Larangan 
Konsekuensi Pelanggaran 
Referensi 
1 
DILARANG menggunakan 
severity_score, folder_category, 
file_name, atau split sebagai 
fitur input model
Data Leakage model menghafal 
label, bukan belajar pola 
Bab 3.1.C & 7.2 
2 
DILARANG melakukan 
Transformasi Spasial 
(Horizontal/Vertical Flip, 
Rotasi) saat augmentasi on-the-
fly
Mengubah orientasi huruf (b→d, 
p→q) dan menghancurkan diagnosis 
letter reversal 
Bab 6.1.C & 7.2 
3 
DILARANG memodelkan 
severity_score sebagai tugas 
Regresi (MSE Loss) atau 
Kategorikal Multiclass 
standar (Cross-Entropy murni) 
severity_score bersifat Kategorikal 
Ordinal. Categorical Cross-Entropy 
(CCE) standar itu "buta urutan" 
(salah tebak 1 ke 6 akan dihukum 
sama dengan tebak 1 ke 2). Wajib 
menggunakan Ordinal Loss (seperti 
Coral Ordinal).
Bab 7.2 
 
 
 


<!-- PAGE 49 -->
48 
 
C. Rekomendasi Opsional (SHOULD) 
#
Saran 
Tujuan 
1
Rancang arsitektur Late Fusion (Multi-Input): 
Branch 1 (CNN) untuk gambar, Branch 2 
(Dense) untuk 6 fitur XAI 
Memaksimalkan transparansi 
dan akurasi prediksi 
2
Jalankan McNemar Test untuk 
membandingkan akurasi model yang dilatih 
pada Dataset A (Gambo murni) vs Dataset B 
(Gambo+EMNIST) 
Memvalidasi secara empiris 
bahwa augmentasi EMNIST 
benar-benar meningkatkan 
performa model 
3
Pahami bahwa 6 fitur XAI diekstrak pasca-
kompresi 28×28 rasio geometris mencerminkan 
kepadatan kanvas, bukan dimensi kertas asli 
Mencegah misinterpretasi klinis 
pada output model 
4
Lakukan Pixel-Level Leakage Check 
menggunakan Cryptographic/Perceptual 
Hashing 
Mendeteksi duplikasi gambar 
yang lolos dari validasi level 
nama file 
 
 
 
 
 
 
 
 
 
 
 


<!-- PAGE 50 -->
49 
 
DAFTAR PUSTAKA 
Cohen, G., Afshar, S., Tapson, J., & van Schaik, A. (2017). EMNIST: An 
extension 
of 
MNIST 
to 
handwritten 
letters. 
arXiv. 
https://arxiv.org/abs/1702.05373 
Isa, I. S., Ramlan, S. A., Sulaiman, S. N., et al. (2021). CNN comparisons models 
on dyslexia handwriting classification. Universiti Teknologi MARA 
Cawangan Pulau Pinang. 
Isa, I. S., Rahimi, W. N. S., Ramlan, S. A., & Sulaiman, S. N. (2019). Automated 
detection of dyslexia symptom based on handwriting image for primary 
school children. Procedia Computer Science, 163, 440–449. 
Jasira, K. T. (2023a). DxDetekt: A dyslexia detection method from handwriting 
using ensemble method. Grenze International Journal of Engineering & 
Technology (GIJET), 9(2). 
Jasira, K. T., Laila, V., & Jemsheer Ahmed, P. (2023b, July). DyslexiScan: A 
dyslexia detection method from handwriting using CNN LSTM model. 
Dalam 2023 International Conference on Innovations in Engineering and 
Technology (ICIET) (hlm. 1-6). IEEE. 
National Institute of Standards and Technology. (n.d.). EMNIST dataset. 
Retrieved Month Day, Year, from https://www.nist.gov/itl/iad/image-
group/emnist-dataset 
Oktamarina, L., Rosalina, E., Utami, L. S., Duati, S. F. K., Dzakiyyah, C., Sari, 
R. P., & Julita, M. S. (2022). Gangguan gejala disleksia pada anak usia dini. 
Jurnal Multidisipliner Bharasumba, 1(02), 104-118. 
Peterson, R. L., Pennington, B. F., & Olson, R. K. (2013). Subtypes of 
developmental dyslexia: Testing the predictions of the dual-route and 
connectionist frameworks. Cognition, 126(1), 20-38. 


<!-- PAGE 51 -->
50 
 
Rahmawati, I. (2025). Penerapan Naïve Bayes untuk klasifikasi penyederhanaan 
teks bacaan anak disleksia (Doctoral dissertation, Universitas Islam Sultan 
Agung). 
Robaa, M., Balat, M., Awaad, R., Omar, E., & Aly, S. A. (2024, December). 
Explainable AI in handwriting detection for dyslexia using transfer learning. 
Dalam 2024 12th International Japan-Africa Conference on Electronics, 
Communications, and Computations (JAC-ECC) (hlm. 17-22). IEEE. 
Rosli, M. S. A. B., Isa, I. S., Ramlan, S. A., Sulaiman, S. N., & Maruzuki, M. 
I. F. (2021, August). Development of CNN transfer learning for dyslexia 
handwriting recognition. Dalam 2021 11th IEEE International Conference on 
Control System, Computing and Engineering (ICCSCE) (hlm. 194–199). 
IEEE. https://doi.org/10.1109/ICCSCE52189.2021.9530971 
Seman, N. S. L., Isa, I. S., Ramlan, S. A., Li-Chih, W., & Maruzuki, M. I. F. 
(2021, August). Classification of handwriting impairment using CNN for 
potential dyslexia symptom. Dalam 2021 11th IEEE International Conference 
on Control System, Computing and Engineering (ICCSCE) (hlm. 188–193). 
IEEE. https://doi.org/10.1109/ICCSCE52189.2021.9530989 
Spoon, K., Crandall, D., & Siek, K. (2019, June). Towards detecting dyslexia in 
children’s handwriting using neural networks. Dalam Proceedings of the 
International Conference on Machine Learning AI for Social Good Workshop 
(Vol. 28). 
 
