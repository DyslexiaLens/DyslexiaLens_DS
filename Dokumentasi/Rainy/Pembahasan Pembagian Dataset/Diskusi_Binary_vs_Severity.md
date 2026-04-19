# Diskusi Fitur: Strategi Menangani Imbalance (Binary vs Multi-Class)

Dokumen ini disusun untuk membahas masalah klasik *Machine Learning* yang sedang kita hadapi terkait perbandingan jumlah data (*imbalance*) dan target arsitektur AI untuk Capstone Project **DyslexiaLens**.

## ⚠️ Akar Permasalahan: Konflik Keseimbangan Kelas
Saat ini dataset kita memiliki rincian kurang lebih sebagai berikut:
- **Normal (Label 0):** ~58.000 gambar
- **Disleksia Total:** ~121.000 gambar, dengan rincian Severity:
  - Severity 1: ~32.000
  - Severity 2-5: Masing-masing hanya ~1.600
  - Severity 6: ~46.000

Pertanyaan yang muncul dalam tim:
> "Apakah tiap bagian label (1-6) itu harus seimbang persis jumlahnya dengan kelas non-disleksia (label 0)? Atau memang tidak perlu seimbang karena disleksia itu merupakan satu kesatuan?"

Jawabannya sangat bergantung pada **jenis dan tujuan model Machine Learning** yang akan dirancang AI Engineer.

---

## 🔍 Analisis Berdasarkan Pendekatan Model

### Skenario A: Pendekatan "Multi-Class" (Memprediksi output pasti: 0, 1, 2, 3, 4, 5, 6)
Jika AI Engineermu memilih jalan ini, maka aturannya: **YA, Setiap kelas harus seimbang**.
*(Jumlah 0 = Jumlah 1 = Jumlah 2 = Jumlah 3 = Jumlah 4 = Jumlah 5 = Jumlah 6)*

**❌ Dampak Fatal:**
Karena Skor 2 hanya memiliki ~1.600 gambar, jika kita menyeimbangkan semuanya tanpa melakukan augmentasi gila-gilaan, maka seluruh kelas (termasuk kelas Normal yang isinya 58.000 gambar) **harus dipotong brutal menjadi 1.600 gambar**. 
Kita berisiko membuang puluhan ribu data berharga, akurasi akan turun tajam, dan ini mendiskreditkan fungsi Big Data. Alternatifnya (yakni dengan memaksakan augmentasi), akan mencetak **300.000+ gambar**, yang berujung *Overfitting* dan komputer kehabisan RAM.

### Skenario B: Pendekatan "Binary" (Memprediksi output: Normal vs Disleksia)
Jika AI Engineermu memilih jalan ini, maka aturannya: **TIDAK, sub-label (1-6) tidak perlu seimbang**.
Yang perlu seimbang hanyalah **KESATUANNYA**.
*(Jumlah Normal [0] = Total Keseluruhan Jumlah Disleksia [1+2+3+4+5+6])*

---

## 🏆 Rekomendasi Data Scientist: Pendekatan "Binary Validation"

Keputusan yang paling rasional, sehat secara performa model, dan paling minim risiko untuk *Capstone Project* ini adalah dengan membuang target label Severity (1-6) dan **fokus 100% pada Binary Classification**. 

### Mengapa ini adalah Ide Sangat Cemerlang?
1. **Penyelamatan Dataset dari Pembengkakan (Efisiensi RAM)**
   Karena kita menyatukan semua Disleksia (121.000 gambar), kita tinggal memotong secara acak (*Undersampling*) menjadi 58.000 saja.
   Hasil akhirnya sangat rapi: **58.000 Normal vs 58.000 Disleksia (Rasiao Rasio 1:1)**. Total 116k gambar sangat ringan dan cepat di-training.
2. **Terhindar dari Augmentasi Fisik Berbahaya**
   Tidak ada lagi rotasi/translasi fisik di Folder Normal yang justru berbahaya, karena Normal yang sengaja dimiringkan bisa dinilai terbalik / disleksia oleh AI.

### 🤔 Pertanyaan Tim: "Tapi kalau dihapus, kita kehilangan ukuran Keparahan / Level Disleksianya dong?"
**JAWABANNYA:** Tidak Hilang. Kita bisa menebak Level Keparahan dari **Confidence Score (Probabilitas AI)**!

Model *Binary* selalu mengeluarkan output skala keyakinan.
Jika diimplementasikan pada Backend FastAPI/Flask:
- Jika CNN Probability / `predict()` output = **90% - 100% Dyslexia** ➔ Ini menandakan pola ekstrem. Sistem Frontend menerjemahkannya sebagai **Dyslexia Tingkat Parah**.
- Jika CNN Probability / `predict()` output = **70% - 89% Dyslexia** ➔ Tampilkan sebagai **Dyslexia Sekala Sedang**.
- Jika CNN Probability / `predict()` output = **51% - 69% Dyslexia** ➔ Tampilkan sebagai **Dyslexia Tingkat Ringan** (hampir mirip Normal tapi sedikit janggal).

### 📝 Action Items Berdasarkan Rekomendasi Ini
Jika keputusan disetujui tim:
- **Data Scientist:** Merevisi Notebook di Tahap Data Preparation dengan menghapus logic *Augmentasi (Tahap 5)*, dan menggantinya murni dengan **Random Undersampling** pada target Disleksia (*target_class=1*).
- **AI Engineer:** Fokus membuat Arsitektur *CNN Binary Classification* saja dan melakukan `model.predict_proba()` untuk Confidence Score-nya.
- **Frontend / UI-UX:** Mempersiapkan palet warna atau UI gauge meter berdasarkan variabel *Confidence Score Backend* untuk merepresentasikan tingkat keparahan.
