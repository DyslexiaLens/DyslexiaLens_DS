# Keputusan Arsitektur Translasi dan Skrining (DyslexiaLens)

Berdasarkan perdebatan teknis mengenai bagaimana aplikasi *DyslexiaLens* harus mengenali dan "menerjemahkan" tulisan tangan penderita disleksia yang secara visual sangat tidak beraturan (dan **tidak boleh** dilabeli menggunakan sistem OCR langsung untuk mencegah *Data Poisoning*), berikut adalah dua pilihan arsitektur akhir yang bisa diambil oleh tim.

---

## PILIHAN A: "Golden MVP" (Jalur Paling Aman & Cepat)
*Lebih difokuskan pada Skrining Medis/Assesment ketimbang alat Translasi Bebas.*

**Cara Kerja:**
1. Di layar aplikasi, Orang tua/Guru/Sistem **memasukkan kata instruksi terlebih dahulu**, misal: **"A P E L"**.
2. Aplikasi men-generate sebuah *Template* (bisa berupa kertas PDF atau UI kotak di tablet) yang berisi persis 4 buah kotak kosong secara beruntun.
3. Anak menulis huruf demi huruf di dalam setiap kotak sesuai urutan.
4. Ketika foto dikirim ke *Backend*, program akan memotong 4 kotak tersebut.
5. **Bagaimana ia menerjemahkan?** Aplikasi tidak perlu menerka bentuknya. Karena posisinya absolut berjumlah 4 kotak, ia tahu pasti Kotak 1 adalah huruf 'A', Kotak 2 adalah huruf 'P', dan seterusnya.
6. **Peran DyslexiaLens:** Keempat kotak berisi gambar tulisan anak tersebut dievaluasi oleh CNN buatan kita. Sistem mendeteksi polanya, contoh: *"Kotak 3 (huruf E) masuk dalam kategori Reversal / Tersajikan Terbalik".*

**Kelebihan:**
- Penyelamat *Capstone* jika waktu mepet. 
- Tidak memerlukan integrasi dengan AI OCR atau NLP eksternal.
- Seratus persen aman dari *bug* tebakan huruf yang salah.

---

## PILIHAN B: "Free-Writing Tandem" (Jalur Hardcore, Berisiko, Tapi Sangat Keren)
*Diambil MURNI jika tim **bersikeras** ingin mempertahankan fitur "Memotret tulisan bebas anak, lalu aplikasi ajaib menebak apa yang si anak maksud dari tulisannya".*

Jalur ini membutuhkan perakitan "Pipeline 3 Mesin" secara *Tandem*:

1. **Input:** Anak bebas menulis kata apapun (misal dia mencoba merangkai kata **"M A K A N"**) di dalam suatu *Grid* kosong. Karena kesulitan belajar, abjad *N* yang ia tulis di akhir menyajikan goresan terbalik (Reversal).
2. **Mesin 1 (Penerjemah Kasar - OCR):** Gambar utuh/potongan tadi dilempar ke API OCR Pihak Ketiga (seperti *Google Vision API*). Mengandalkan basis data normal, OCR membaca huruf yang hancur itu dan menebak salah.
   - *Output Mesin 1:* Kembalian String mentah `"M A K A H"`.
3. **Mesin 2 (Sang Korektor - NLP Spellchecker):** String rusak tersebut masuk ke algoritma pengecek ejaan Bahasa Indonesia (NLP/Kamus *Auto-Correct*). Algoritma dengan cerdas menyadari bahwa kata "MAKAH" itu absurd dan mengkoreksinya secara konteks menjadi "MAKAN".
   - *Output Mesin 2 (Hasil Translasi Final):* String **`"MAKAN"`** (Berjalan lancar! Teks aneh dari anak disleksia sukses ditranslate).
4. **Mesin 3 (Sang Dokter - DyslexiaLens):** Di belakang layar, kelima kotak gambar anak tadi tetap dimasukkan satu persatu ke model CNN *DyslexiaLens*. Model yang dilatih dari kumpulan ribuan data *Gambo* ini melihat gambar Kotak ke-5, lalu melapor: *"Pola Goresan Tipe Reversal (Severity 4)!"*.
5. **Output Layar Akhir:** Tampilan UI akan menggabungkan hasil pekerjaan Mesin 2 dan Mesin 3. 
   > **Teks Translasi Bersih:** "MAKAN"
   > **Visual Indikator Cacat:** Huruf 'N' ditebalkan dengan balok merah dan keterangan ("Tanda Reversal / Terbalik").

**Kelebihan:**
- Fitur revolusioner sesungguhnya dari impian deteksi disleksia yang fungsional.
- Mendapatkan nilai bonus maksimum (Side Quest) di mata Reviewer MVP karena melakukan Integrasi API NLP pihak ke-3 untuk fitur sekunder.
- Menguji ketahanan ilmu *Fullstack Data Engineering* dari tim.

---

## 🎯 Kesimpulan Penting Untuk Divisi Data Science
Terlepas dari Pilihan A atau Pilihan B yang akan divoting dan dieksekusi oleh rekan AI dan Backend besok, **Satu hal pasti**: 
> **Kewajiban Data Scientist cukup sampai mensuplai `master_dataset_final.csv` (Dataset `Gambo` 180k) yang murni.**

Kamu sekali-sekali tidak perlu bersusah payah menambahkan *Metadata* "A-Z" ke dalam dataset penderita disleksia hanya demi bisa membaca abjadnya, karena tugas penebakan abjad sudah di- *takeover* dengan pendekatan struktural (Solusi A) atau pendekatan API NLP/Kamus (Solusi B). Fokus datamu 100% hanyalah mencerdaskan "Mesin 3"!
