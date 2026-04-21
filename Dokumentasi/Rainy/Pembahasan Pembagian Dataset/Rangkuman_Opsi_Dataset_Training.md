# Rangkuman Diskusi Strategi Dataset & Training (DyslexiaLens)

Dokumen ini memuat rangkuman opsi strategis terkait bagaimana kita akan menyuapkan data (180.726 gambar) ke *Machine Learning Model*, mengingat adanya masalah *Class Imbalance* antara Normal vs Disleksia, dan ketidakseimbangan internal di dalam *Severity Score* 1-6.

---

## 🏆 Rencana A: Pendekatan "Zero Data Loss" (SANGAT DIREKOMENDASIKAN)
*(Opsi ini sudah diimplementasikan dan siap pakai pada notebook `Dyslexia.ipynb` saat ini)*

**Konsep:** 
- Tetap menggunakan seluruh target label (Severity 1-6 dan Normal).
- **TIDAK ADA augmentasi fisik** sama sekali.
- **TIDAK ADA undersampling** (penghapusan data). 
- Melakukan Train/Validation/Test split murni secara *stratified*.
- Mengimplementasikan `class_weight` pada saat training model.

**Kelebihan:**
1. **Harta Karun Selamat:** Semua 180.000 data orisinil yang kita kumpulkan akan digunakan 100%. Tidak ada data terbuang sia-sia.
2. **Tanpa Risiko Overfitting Manipulasi Fisik:** Gambar tetap alami. AI tidak ditipu dengan gambar Normal yang sengaja dimiringkan (yang berisiko membuatnya disangka '*Reversal*' / Disleksia).
3. **Pekerjaan AI Engineer Terarah:** Parameter `class_weight` (bobot urgensi) sudah dihitungkan oleh Data Scientist. Saat training, AI akan otomatis memberikan porsi fokus lebih besar (bobot penalti tinggi) tiap memproses data yang minoritas untuk menyeimbangkannya secara *matematis*.

---

## 🥈 Rencana B: Pendekatan "Murni Binary & Undersampling" (ALTERNATIF AMAN)
*(Disarankan hanya jika AI Engineer merasa model kesulitan menemukan pola di Rencana A)*

**Konsep:**
- Menghapus sama sekali target `severity_score` (1-6). Hanya menyisakan target label *Binary* (Normal vs Disleksia).
- Mengurangi label Disleksia secara acak (*Undersampling*) agar jumlahnya seimbang secara absolut untuk *Binary Classification* (misal: 58k Normal vs 58k Disleksia).
- Atau, Model hanya belajar Normal vs Disleksia, namun tetap menggunakan `class_weight` (tanpa undersampling) untuk mengimbangi 58k Normal vs 121k Disleksia.

**Kelebihan:**
- Model sangat cepat belajar dan beban RAM rendah. Fokus utamanya tidak terpecah ke 6 *severity* skor yang njelimet.

**Kelemahan (Risiko):**
- Kita kehilangan informasi label (1-6) kepelikan gambar yang bernilai riset tinggi. 
- *Undersampling* berarti membuang puluhan ribu data Disleksia secara sia-sia.

*Catatan: Jika menempuh cara ini, ukuran keparahan (Level Disleksia) didapat dari mengkonversikan tingkat probabilitas (`Confidence Score`) dari AI Backend saat memproses gambar, bukan murni dari hasil prediksi `Target_Class`.*

---

## 🗑️ Rencana C: Pendekatan Augmentasi Fisik (TIDAK MASUK AKAL / OPSI TOLOL)
*(Ini adalah pendekatan eksperimen lama yang sudah dicadangkan di notebook `Dyslexia_OfflineAugmentation.ipynb`)*

**Konsep:**
- Tetap menggunakan severity 1-6.
- Melakukan augmentasi fisik (Rotasi/Zoom) secara offline ke harddisk khusus pada kelas disleksia berporsi rendah (severity 2-5) agar jumlahnya sama dengan severity 1 dan 6.

**Alasan Mengapa ini "Tolol" (Sangat Buruk):**
1. **Overfitting yang Parah:** Kita memaksakan sebuah gambar unik disalin dan sedikit diputar beribu-ribu kali. AI akan menghafal bentuk-bentuk yang diulang ini (*overfitting*) dan akan bodoh saat mengenali data dunia nyata.
2. **Kiamat Hardware:** Menambah file gambar augmented ke disk lokal akan membengkakkan dataset menjadi 300.000+ keping. Perangkat Google Colab gratis dan penyimpanan akan hancur dan waktu *training* sangat tidak masuk akal lambatnya.
3. Menghasilkan *total Disleksia* yang jauh menembus angkasa dan sama sekali tidak imbang dengan kuantitas non-disleksia (Normal).

---
**🎯 Kesimpulan Utama untuk Proyek (Action for AI Engineer):**
Gunakan file `master_dataset_final.csv` dari hasil **Rencana A**. Data Scientist sudah selesai merangkum Data Wrangling ini. Beban penyeimbangan kelas secara utuh sekarang berada di `class_weight` parameter ketika `model.fit()` dijalankan.
