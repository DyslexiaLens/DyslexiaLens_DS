# Checkpoint 7 — Full Dataset Re-Engineering & Integrity Hardening
**Tanggal:** 11 Mei 2026  
**Role:** Data Scientist  
**Status Notebook:** `Dyslexia.ipynb` (Finalisasi Dataset Steril)

---

## 🎯 Ringkasan Eksekutif Sesi
Sesi ini menjadi titik perubahan besar bagi proyek DyslexiaLens: berevolusi dari sekadar **preprocessing dataset sederhana** menjadi **rekayasa sistem data saintifik penuh (*full scientific dataset engineering*)**. Fokus utama kita kini bukan lagi sekadar *"bagaimana melatih model"*, melainkan *"bagaimana memastikan model belajar sinyal yang benar"*. 

Evaluasi kritis menunjukkan bahwa pipeline lama masih belum cukup steril. Ditemukan berbagai pola tersembunyi yang berpotensi membuat model CNN melakukan *shortcut learning* (menghafal artefak visual alih-alih belajar pola disleksia autentik). Sesi ini didedikasikan untuk **Dataset Integrity Hardening**, dengan pencapaian puncak berupa **keputusan final untuk menghapus data berpolaritas anomali demi menjaga kualitas sinyal**.

---

## 🚨 Pencapaian & Resolusi Sesi Ini

### 1. Finalisasi Standardisasi Polarity (Keputusan Akhir)
**Konteks:** Ditemukan ketidakkonsistenan pada polaritas dataset (sebagian gambar tulisan putih di latar hitam, lainnya hitam di latar putih). Ini sangat berbahaya karena CNN berpotensi belajar *background* atau *contrast pattern*, bukan pola tulisan disleksia.
**Tindakan Resolusi:** 
- Melakukan eksperimen *auto inversion* dan *polarity normalization*.
- **Masalah Ditemukan:** Hasil augmentasi polaritas ternyata tidak stabil (gambar menjadi *noisy*, detail *stroke* rusak, karakter berubah, dan distribusi tidak natural).
- **Keputusan Final:** Gambar dengan polaritas berbeda diputuskan untuk **DIHAPUS**, bukan diaugmentasi secara paksa. Pendekatan ini jauh lebih aman secara saintifik demi menghindari bias visual tambahan dan *distribution shift* baru. Kualitas visual asli lebih penting dibanding jumlah data.

### 2. Penanganan Residual Data Leakage
**Konteks:** Masih terdapat *duplicate lineage*, *visual duplication*, dan kontaminasi kelas tersembunyi (seperti file *placeholder* dan penamaan *regex* yang rusak).
**Tindakan Resolusi:** 
- Melakukan operasi *Dataset Integrity Hardening* yang mencakup *full dataset re-audit* dan *strict filename validation*.
- Menjalankan *duplicate removal* dan *leakage sterilization*.
- **Hasil:** Risiko model menghafal pola visual spesifik atau meraih *validation score* tinggi palsu berhasil dieliminasi.

### 3. Revisi Feature Engineering Ketebalan (Bias Removal)
**Konteks:** Fitur ketebalan *stroke* (*ink density*) masih terpengaruh oleh warna *background*, *inversion*, dan *noise grayscale*, berisiko menghasilkan metrik ketebalan yang bias.
**Tindakan Resolusi:** 
- Ketebalan kini dikalibrasi ulang dengan mengandalkan *foreground isolation*, *stroke density*, dan *threshold-aware extraction*.
- **Hasil:** Fitur ketebalan kini benar-benar merepresentasikan kepadatan tulisan nyata, tekanan visual, dan pola coretan autentik.

### 4. Standardisasi Dataset Total
**Tindakan Resolusi:** Menerapkan *grayscale consistency*, *polarity consistency*, *foreground normalization*, dan *structural validation*.
**Dampak:** CNN kini dipaksa mutlak untuk belajar pola *stroke*, *severity*, dan *reversal behavior*, **BUKAN** warna *background*, polaritas, atau artefak visual dataset.

---

## 🧠 Evolusi Filosofi Proyek
Perjalanan proyek ini telah membongkar berbagai tantangan kritis: *severity architecture*, *OCR paradox*, *hidden leakage*, *polarity bias*, *label contamination*, dan ancaman *shortcut learning* pada CNN. 

Hal ini memaksa evolusi besar dalam filosofi AI System Design kami:
- **Filosofi Awal:** *"Dataset cukup bersih untuk training."*
- **Filosofi Sekarang:** *"Dataset harus steril secara statistik dan visual."*

Kualitas sinyal visual kini adalah prioritas absolut di atas jumlah data maupun augmentasi berlebihan.

---

## 🚀 Dampak Strategis & Kesimpulan Perjalanan
Pipeline baru (*Dataset Integrity Hardening*) diperkirakan akan:
- Secara drastis mengurangi *shortcut learning*.
- Meningkatkan generalisasi performa dunia nyata.
- Memperkuat validitas ilmiah proyek secara keseluruhan.
- Meningkatkan *robustness* model CNN.

**Kesimpulan Akhir:**
Perjalanan ini telah berkembang dari preprocessing sederhana menjadi rekayasa sistem data saintifik penuh. Saat ini, proyek telah mencapai tahap akhir *Dataset Integrity Hardening*. Fokus utama bukan lagi sekadar melatih model, melainkan memastikan bahwa model CNN nantinya benar-benar belajar pola disleksia yang autentik, stabil, dan dapat dipertanggungjawabkan secara ilmiah. Dataset steril ini siap digunakan untuk tahap selanjutnya!