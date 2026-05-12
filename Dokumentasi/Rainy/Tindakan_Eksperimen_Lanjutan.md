# Laporan Eksekusi Rencana Tindakan & Gerakan Lanjutan

Dokumen ini melacak eksekusi dari rencana yang disusun sebelumnya pada dokumen `Peran_dan_Tindakan_Data_Scientist.md`.

---

### ❌ 1. Augmentasi Rotasi Skala Kecil (±10 Derajat)
**Status:** Dibatalkan
**Alasan:** Setelah dievaluasi, penambahan data melalui augmentasi rotasi skala kecil dirasa tidak memberikan variasi yang cukup bagus dan signifikan. Daripada melakukan rotasi, diputuskan bahwa mengambil data eksternal dari EMNIST atau **tidak menambahkan data augmentasi sama sekali** akan menghasilkan kualitas model yang lebih baik dan menjaga kealamian data.

### ❌ 2. Eksperimen Pelabelan Abjad dari Skor Keparahan
**Status:** Dibatalkan
**Alasan:** Sangat tidak memungkinkan untuk dilakukan. Keterbatasan teknologi saat ini menyulitkan otomatisasi proses pelabelan abjad pada tulisan anak penderita disleksia. Eksperimen pelabelan manual pun sudah dicoba, namun dibatalkan karena bentuk tulisan dan abjad pada keparahan tinggi sudah sangat tidak beraturan sehingga membingungkan untuk diidentifikasi secara manual sekalipun manusia.

---

### ✅ 3. Eksperimen Feature Engineering
**Status:** Selesai
**Tindakan:** Eksperimen ini berhasil dieksekusi dengan sangat baik. Skrip telah berhasil mengekstrak 5 fitur turunan matematis dari matriks piksel gambar. Berikut adalah penjelasan untuk masing-masing fitur yang diekstrak:

| Fitur | Deskripsi |
|---|---|
| `ink_density` | Persentase piksel hitam (tinta) terhadap total area gambar (784 piksel). Fitur ini berguna mendeteksi penebalan tulisan akibat coretan berulang (*over-tracing*) yang sering terjadi pada penderita disleksia. Tulisan yang banyak dicoreng akan memiliki kepadatan tinta lebih tinggi. |
| `center_of_mass_x` | Posisi titik tengah goresan pada sumbu horizontal (0-27). Membantu mendeteksi distorsi orientasi; huruf yang miring, asimetris, atau menyimpang jauh ke kiri/kanan akan memiliki *centroid* yang melenceng. |
| `center_of_mass_y` | Posisi titik tengah goresan pada sumbu vertikal (0-27). Berguna untuk mendeteksi masalah spasi dan letak vertikal, seperti tulisan yang "melayang" terlalu tinggi atau "anjlok" secara tidak wajar melewati garis bayangan. |
| `bounding_box_ratio` | Rasio tinggi/lebar area goresan setelah *whitespace* luar dipangkas. Sangat efektif untuk mengidentifikasi distorsi proporsi huruf (misal: huruf 'o' menjadi sangat pipih). Huruf yang direvisi berulang kali cenderung melebar (rasio < 1). |
| `stroke_transitions` | Rata-rata frekuensi perubahan warna (putih ↔ hitam) per baris horizontal. Angka transisi yang tinggi mengindikasikan goresan yang terputus-putus, berantakan, atau bergetar (tremor) akibat kesulitan motorik halus penderita. |

---

### 🔄 4. Pelaksanaan A/B/C Testing Dataset
**Status:** Masih dalam proses (In Progress)

### 🔄 5. Deployment Dashboard ke Cloud
**Status:** Masih dalam proses (In Progress)
