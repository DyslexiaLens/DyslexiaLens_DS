# Checkpoint 4 — Finalisasi Arsitektur Translasi, OCR Paradox, dan Revisi Dataset
**Tanggal:** 21 April 2026  
**Peran:** Data Scientist  

---

## 🎯 Ringkasan Eksekutif Sesi
Sesi ini sangat krusial bagi keberlangsungan *System / Product Architecture* dari Capstone proyek kita (DyslexiaLens). Kita telah membedah secara mendalam masalah fundamental mengenai *"Bagaimana cara AI ini mengenali tulisan penderita disleksia?"*

Diskusi ini berujung pada penemuan kelemahan sistem yang fatal jika kita menggunakan OCR biasa (Paradoks OCR). Sebagai jalan keluarnya, kita memformulasikan 2 Opsi Arsitektur untuk dieksekusi oleh tim Backend/AI, serta mensinkronkan ulang seluruh dokumentasi terkait transisi dari "Augmentasi Fisik" ke strategi `class_weight`.

Teman-teman *(AI Engineer & Full-stack)* diharapkan membaca dokumen referensi yang tertaut di setiap poin bawah ini.

---

## 1. Penemuan Kritis: "Paradoks OCR" pada Tulisan Disleksia
**Konteks:** Awalnya muncul gagasan agar Data Scientist melabeli dataset disleksia menggunakan API OCR biasa sehingga mesin otomatis mengenali abjad tulisannya. Namun, ini memicu jebakan logika (*OCR Paradox*).

**Masalah Fundamental:** 
- Jika OCR biasa disuruh menebak huruf yang bentuknya Reversal (Anak niat menulis huruf 'b', tapi gambar yang keluar mirip 'd'). OCR akan melabeli gambar tersebut secara ngotot sebagai abjad 'd'. Jika ini diajarkan pada AI kita, model CNN *DyslexiaLens* akan belajar secara salah!
- Begitu juga tulisan dengan keparahan *Severity 6* (coretan abstrak), tentu akan merusak pembacaan OCR menjadi simbol aneh seperti `@` atau `#`.

**Kesimpulan untuk Tim:** Model AI *DyslexiaLens* yang dilatih menggunakan dataset *Gambo* **TIDAK BERTUGAS UNTUK MENG-OCR/MENERJEMAHKAN ABJAD**. Output model tersebut murni hanya sebagai **Diagnostic Tools (Dokter Penilai Tingkat Kepelikan Pola Goresan via Severity 0-6).**
📖 **Baca Rincian Dokumen Lengkap di sini:** [👉 Diskusi_Paradoks_OCR_dan_Translasi.md](../Pembahasan%20Pembagian%20Dataset/Diskusi_Paradoks_OCR_dan_Translasi.md)

---

## 2. Pemilihan Dua Sistem Translasi Arsitektur (Bahan Diskusi Meeting Lanjutan)
Meskipun Model DyslexiaLens kita tidak mengenali Abjad teks, **Aplikasi Website/Android kita Tetap Bisa Memiliki Fitur Terjemahan Abjad.** Untuk merajutnya, teman-teman di ranah *Software Engineering / AI* harus memilih salah satu dari dua pendekatan sistem di bawah ini:

### Opsi A: "Golden MVP" (Smart Grid / Kertas Template Terstruktur)
* **Konsep:** Pendekatan paling masuk akal jika waktu kita sempit. Orang tua memasukkan kata di Web -> Cetak Kertas Grid PDF -> Anak menebalkan tulisan sesuai grid yang diinstruksikan.
* **Proses Translasi:** OpenCV di *Backend* melakukan pemotongan koordinat absolut pada grid tersebut. Aplikasi tidak butuh AI OCR untuk menebak, karena aplikasi sudah tahu pasti abjad apa yang seharusnya berada di kotak nomor 1. Model DyslexiaLens hanya bertugas mengevaluasi tiap kotak tersebut. *(Cepat, Aman)*.

### Opsi B: "Tandem Pipeline" (OCR API + NLP Spellchecker Auto-Correct)
* **Konsep:** Berisi perakitan model lapis ganda jika kita nekat mau membuat *Fitur Scan Kertas Kosong*.
* **Proses Translasi:** Anak bebas menulis kalimat, difoto -> masuk ke Mesin API OCR Pihak Ketiga (seperti Google Vision) -> teks mentah rusak yang dihasilkan OCR dilempar ke algoritma AutoCorrect Ejaan Bahasa Indonesia (Modul NLP) agar membenarkan konteks katanya -> di latar belakang Sistem DyslexiaLens memberi label merah pada huruf yang keparahannya tinggi. *(Sangat rumit untuk Backend, namun bernilai Plus Ekstra dari Penilai Dicoding)*.

📖 **Pahami Perbedaan 2 Pipeline Ini di sini:** [👉 Pilihan.md](../Pembahasan%20Pembagian%20Dataset/Pilihan.md)

---

## 3. Sweeping Dokumentasi Strategi Dataset (Anti-Augmentasi Fisik)
Menyelaraskan kesepakatan sesi *Checkpoint* sebelumnya, manipulasi gambar fisik seperti digandakan dan diputar (*Offline Augmentation*) **resmi dibatalkan seluruhnya**. Hal ini semata-mata untuk mencegah *Ledakan Storage Harddisk* pada PC AI Engineer dan menghindari *Overfitting*.

**Tindak Lanjut & Ketetapan Hukum Model Training:**
- Ketidakseimbangan data yang ekstrem antara Normal vs Disleksia (1:2) kini **WAJIB** diatasi murni hanya dengan parameter `class_weight` (rasio matematika Scikit-Learn) yang ditaruh oleh AI Engineer di fungsi `model.fit()`. Tidak ada manipulasi gambar satupun.
- Dataset final siap pakai diserahkan utuh *(Zero Data Loss)* dengan jumlah original: **180.726 gambar** *(Train, Val, Test split)*.
- Seluruh file dokumen *Markdown (.md)* yang tersebar di *repository* di bawah ini telah diselaraskan bahasanya untuk mendukung pendekatan Final *Class Weight* tersebut:
  1. [README.md](../../README.md) *(Di halaman Root Repo)*
  2. [Temuan_EDA.md](../Temuan_EDA.md) *(Khusus AI Engineer: Cek rumus weight/bobot penalti AI-mu di Bab 7 file ini)*
  3. [Pipeline_Preprocessing_Data.md](../Pipeline_Preprocessing_Data.md)
  4. [Data Scientist Checklist.md](../Data%20Scientist%20Checklist.md) *(Progres DS sudah Checklist [x] Selesai 100%)*
  5. [Analisis Dataset.md](../Analisis%20Dataset.md) 

---

## 🚀 Rencana / Rekomendasi Aksi Lanjut (Next Action)
1. **Meeting Integrasi:** Tim Backend, Frontend, dan AI wajib mengadakan *Meeting* untuk melakukan voting eksekusi (*Opsi A* atau *Opsi B*) dari *Pilihan.md*. Ini sangat bernilai dalam efisiensi koding aplikasi beberapa siklus waktu ke depan.
2. Tugas Data Scientist murni dalam pengantaran CSV/Dataset telah usai (*Main Quest Selesai*). Kini SDM kami siap turun gunung untuk mendampingi AI Engineer masuk ke area penulisan Arsitektur TensorFlow Kustom, atau melanjutkan eksplorasi *Dashboard EDA Streamlit*.
