List Tech Stack Capstone Project (Checklist Tugas Wajib dan Opsional)

Dalam pengerjaan capstone project, terdapat 2 jenis checklist (Tech Stack) yang harus dipenuhi oleh tim capstone, diantaranya adalah Main Quest (Wajib) dan Side Quest (Opsional, nilai tambah). Adapun fungsi tech stack adalah sebagai berikut:

Memandu tim melalui checklist checklist tugas wajib dan optional untuk mencapai Minimum Viable Product (MVP).

Membantu tim capstone untuk menyusun pembagian tugas antar anggota tim.

Pengerjaan capstone project menjadi lebih terarah.

Silakan perhatikan Checklist Tech Stack berikut untuk mengetahui lebih lanjut checklist apa saja yang perlu diselesaikan oleh Tim Capstone:

Tech Stack Tim dengan 3 Learning Path
A. Main Quest (Checklist yang Wajib Terpenuhi)
Definisi: Merupakan checklist wajib yang harus dipenuhi oleh Tim Capstone untuk mencapai Minimum Viable Product.

Tugas: Buatlah sebuah aplikasi yang mengintegrasikan dua teknologi utama: Front-End dan Back-End, untuk memberikan solusi terhadap suatu permasalahan yang sesuai dengan tema yang telah ditentukan.

1. List Tugas: Front End and Back End

[ ] Menggunakan networking calls untuk berinteraksi dengan API pada proyek.

[ ] Menggunakan module bundler (seperti webpack, Vite, dan sejenisnya) untuk membangun proyek aplikasi web.

[ ] Membangun RESTful API untuk mendukung aplikasi Front-End.

[ ] RESTful API dapat menyimpan data dengan atau tanpa menggunakan database.

[ ] Membuat RESTful API dengan URL yang mengikuti standar konvensi RESTful.

[ ] Mengintegrasikan kemampuan AI/ML sebagai fitur utama aplikasi, baik melalui back-end aplikasi maupun langsung pada perangkat pengguna (browser).

[ ] Memastikan implementasi fitur utama yang dikembangkan dalam proyek berjalan dengan baik tanpa menyebabkan aplikasi crash.

Tindakan yang Dilarang:
Menggunakan web generator untuk membuat aplikasi front-end maupun back-end.

2. List Tugas: Artificial Intelligence

[ ] Membangun model Deep Learning menggunakan TensorFlow Functional API atau Model Subclassing, yang disesuaikan dengan dataset dan permasalahan bisnis yang telah ditentukan oleh tim Data Science (jika ada).

[ ] Mengimplementasikan setidaknya satu komponen kustom lanjutan dalam proses pengembangan model, seperti:

Custom Layer

Custom Loss Function

Custom Callback

[ ] Menyimpan dan mengekspor model yang telah dilatih secara penuh dalam format TensorFlow siap produksi (.keras atau SavedModel).

[ ] Membuat kode sederhana untuk proses inference model.

Tindakan yang Dilarang:

Menggunakan model yang sudah tersedia dari TensorFlow Hub atau sumber serupa.

Menggunakan model langsung dari layanan API seperti ChatGPT API, Gemini API, dan sejenisnya.

Menggunakan AutoML untuk membuat model AI diskriminatif (Vertex AI hanya diperbolehkan untuk use case Generative AI).

3. List Tugas: Data Science

[ ] Mengumpulkan dan menganalisis berbagai permasalahan, kemudian menentukan satu solusi utama yang akan dikembangkan dalam proyek.

[ ] Mendefinisikan pertanyaan bisnis yang dapat diukur.

[ ] Melakukan proses Data Wrangling secara end-to-end, yang mencakup:

Gathering Data: Mengumpulkan data atau mencari dataset yang relevan, baik dari sumber publik maupun melalui proses scraping.

Assessing Data: Mengevaluasi kualitas dan struktur data.

Cleaning Data: Membersihkan dan mempersiapkan data sebelum masuk ke tahap analisis.

[ ] Melakukan Exploratory Data Analysis (EDA) untuk mendapatkan insight dari data.

[ ] Membuat visualisasi data dan melakukan explanatory analysis untuk menjawab pertanyaan bisnis.

[ ] Mengembangkan dashboard interaktif menggunakan Streamlit untuk menampilkan insight dan kesimpulan.

[ ] Memastikan data sudah siap diproses oleh model, serta disarankan untuk membuat Data Dictionary.

Tindakan yang Dilarang:

Menggunakan dataset yang sudah siap pakai tanpa melakukan proses pembersihan data secara manual.

Melakukan analisis data tanpa memberikan penjelasan dalam bentuk markdown atau teks.

Menarik kesimpulan tanpa didukung oleh visualisasi data.

Menghasilkan format dataset akhir yang belum siap digunakan pada tahap pemodelan.

Menyertakan informasi target ke dalam fitur training (data leakage).

B. Side Quest (Checklist Optional, Nilai Tambah)
Tingkatkan kualitas proyek dan dapatkan nilai tambah dengan mengimplementasikan rekomendasi berikut:

1. Front-End dan Back-End

Membuat mockup aplikasi sebagai representasi visual dari desain dan antarmuka pengguna (UI).

Membangun layout aplikasi web yang responsif agar dapat berjalan dengan baik pada berbagai ukuran layar perangkat.

RESTful API dapat menyimpan data ke dalam database.

RESTful API dibangun menggunakan framework Express.

Rekomendasi tools untuk meningkatkan proses pengembangan aplikasi web: Bootstrap / Tailwind CSS, Axios.

Melakukan deployment aplikasi web ke server.

Rekomendasi layanan hosting: GitHub Pages, Netlify, atau Vercel.

2. Artificial Intelligence

Mengembangkan REST API mandiri menggunakan FastAPI atau Flask untuk melayani model machine learning.

Mengimplementasikan training dan evaluation loop kustom secara penuh dari awal menggunakan tf.GradientTape.

Menggunakan API Generative AI untuk fitur tambahan atau fitur sekunder pada aplikasi.

Mengintegrasikan TensorBoard untuk memantau dan memvisualisasikan metrik pelatihan secara menyeluruh, serta menyertakan log yang dihasilkan dalam repository akhir.

Memastikan model memiliki performa yang baik, dengan ketentuan minimum:

Akurasi minimal: 85%

MAE maksimal: 0,02

3. Data Science

Melakukan feature engineering untuk menghasilkan fitur yang lebih informatif bagi model.

Melakukan deployment dashboard ke Streamlit Cloud agar dapat diakses secara publik.

Mengimplementasikan A/B Testing menggunakan Python.

Membuat laporan teknis komprehensif mulai dari tahap Problem Discovery hingga hasil akhir proyek dalam format PDF.