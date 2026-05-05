# Feature Engineering (Side Quest)

Dokumen ini menjelaskan metrik-metrik yang diekstrak melalui proses **Feature Engineering** pada dataset gambar tulisan tangan (28x28 piksel grayscale). 

Tujuan utama dari tahapan ini adalah untuk menerjemahkan karakteristik fisik dari "bentuk goresan" gambar mentah menjadi "angka ukur" (variabel numerik). Dengan adanya fitur tabular ini, model AI (*Machine Learning* / *Deep Learning*) dapat lebih mudah dan akurat dalam mendeteksi pola yang membedakan antara tulisan tangan biasa (Normal) dan tulisan yang memiliki indikasi kesulitan menulis (Disleksia/Disgrafia), misalnya dengan menggunakan *Multi-Input Model*.

Berikut adalah lima fitur utama yang diekstrak beserta penjelasan teknis dan signifikansinya dalam deteksi disleksia:

---

## 1. `ink_density` (Kepadatan Tinta)
*   **Cara Hitung:** 
    Mengukur persentase jumlah piksel hitam (tinta/goresan) dibandingkan dengan keseluruhan area gambar (total 784 piksel). Nilainya berupa pecahan desimal antara 0.0 (kanvas kosong) hingga 1.0 (gambar hitam sepenuhnya).
*   **Kegunaan dalam Deteksi Disleksia:** 
    Anak dengan disleksia atau diskrafia sering kali melakukan koreksi tebal, mencoret-coret ulang (menebalkan) huruf yang salah, atau menekan alat tulis lebih kuat karena ragu-ragu. Hal ini menyebabkan karakter huruf tersebut memiliki goresan yang lebih tebal dan menumpuk. Fitur ini sangat berguna untuk mendeteksi anomali penebalan huruf; nilai `ink_density` yang tidak wajar / lebih tinggi bisa menjadi indikator kuat adanya coretan berlebih (*reversal/corrected*).

## 2. `center_of_mass_x` (Titik Berat Goresan Sumbu Horizontal / X)
*   **Cara Hitung:** 
    Mencari titik keseimbangan rata-rata (*centroid*) dari seluruh piksel tinta pada sumbu X (kiri ke kanan), dengan rentang nilai dari 0 hingga 27.
*   **Kegunaan dalam Deteksi Disleksia:** 
    Fitur ini mengevaluasi keseimbangan proporsi huruf dari kiri ke kanan. Orang yang mengalami kesulitan menulis sering kali menghasilkan bentuk huruf yang "berat sebelah", asimetris, melenceng, atau memiliki proporsi lengkungan yang tidak wajar (misalnya, perut huruf 'b', 'd', atau 'p' yang terlalu menjorok ke satu sisi dibandingkan bentuk idealnya). Titik centroid sumbu X yang melenceng drastis dari pusat dapat mendeteksi huruf yang digambar secara asimetris.

## 3. `center_of_mass_y` (Titik Berat Goresan Sumbu Vertikal / Y)
*   **Cara Hitung:** 
    Mencari titik keseimbangan rata-rata (*centroid*) dari seluruh piksel tinta pada sumbu Y (atas ke bawah), dengan rentang nilai dari 0 hingga 27.
*   **Kegunaan dalam Deteksi Disleksia:** 
    Melihat proporsi huruf secara vertikal. Penderita disleksia sering mengalami kendala spasial dalam menjaga posisi huruf pada "garis imajiner" dasar buku tulis. Akibatnya, tiang huruf (seperti 't', 'd', 'l') terkadang terlalu panjang, atau terlalu pendek, bahkan hurufnya bisa terlihat melayang/tenggelam dari *baseline*. Fitur ini membantu menangkap anomali proporsi atas-bawah dan penempatan vertikal dari struktur tulisan.

## 4. `bounding_box_ratio` (Rasio Proporsi Bounding Box)
*   **Cara Hitung:** 
    Merupakan rasio hasil pembagian antara **Tinggi area goresan** dengan **Lebar area goresan** (setelah ruang kosong / *whitespace* di sekeliling goresan huruf dipangkas). 
    *   Jika rasionya **< 1**, tulisan memiliki kecenderungan melebar secara horizontal.
    *   Jika rasionya **> 1**, tulisan memiliki kecenderungan memanjang secara vertikal.
*   **Kegunaan dalam Deteksi Disleksia:** 
    Sangat efektif untuk mendeteksi "distorsi bentuk huruf". Anak dengan gangguan disgrafia sering memproduksi huruf yang ditarik terlalu lebar menyamping (akibat keraguan atau pengulangan penarikan garis) atau justru terlalu memanjang secara tidak beraturan. Apabila rasio ini sangat jauh berbeda (outlier) dibandingkan rata-rata bentuk standar untuk huruf yang sama, AI akan mengidentifikasinya sebagai suatu anomali morfologis.

## 5. `stroke_transitions` (Tingkat Transisi Goresan)
*   **Cara Hitung:** 
    Menghitung rata-rata jumlah pergantian warna (transisi) dari warna latar/background (putih) menjadi goresan tinta/foreground (hitam) dan sebaliknya, pada setiap baris piksel mendatar.
*   **Kegunaan dalam Deteksi Disleksia:** 
    Ini merupakan metrik ampuh untuk mengevaluasi **tingkat kekacauan, kontinuitas, dan kerumitan goresan**. Huruf yang ditulis secara wajar, lancar, dan rapi umumnya akan memiliki jumlah transisi pergantian warna yang stabil dan minim. Namun, tulisan yang digambar dengan gemetar (*tremor*), diulang-ulang (*retracing*), penuh coretan berantakan, atau goresannya terputus-putus akan memicu lonjakan jumlah transisi warna secara signifikan. Fitur ini secara kuantitatif mempresentasikan seberapa "kotor" dan berantakan bentuk dari karakter yang ditulis.

---

**Kesimpulan:**
Alih-alih memaksa model AI murni hanya mengandalkan ekstraksi *feature maps* dari matriks piksel mentah (CNN konvensional), kelima fitur ini berfungsi layaknya memberikan data "ringkasan" tabular kepada model (bahwa *"Gambar ini tintanya sangat padat, ukurannya melebar, dan tarikan garisnya sangat berantakan"*). Hal ini diharapkan dapat menjadi komplementer yang mempercepat pembelajaran dan secara signifikan menaikkan akurasi dalam membedakan pola gambar Normal dan Disleksia.
