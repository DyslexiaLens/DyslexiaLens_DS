# Penjelasan Kelas dan Kejanggalan Visual Dataset Gambo

Dokumen ini mencatat temuan mengenai anomali visual yang ditemukan selama proses *Data Auditing* pada dataset `Gambo`, beserta revisi pemahaman kami setelah dilakukan inspeksi visual mendalam.

---

## 1. Definisi Kelas (Label)
Pembuat dataset `Gambo` menggunakan tiga label utama untuk mengkategorikan tulisan tangan:

* **Normal**: Tulisan tangan wajar/benar tanpa ada ciri-ciri disleksia atau disgrafia.
* **Reversal (Terbalik)**: Tulisan tangan di mana penulisnya mengalami bingung arah (*mirror writing* / terbalik). Misalnya, menulis huruf `d` tapi bentuknya jadi seperti `b`, atau menulis `j` tapi melengkung ke arah sebaliknya. Ini adalah gejala klasik disleksia.
* **Corrected (Dikoreksi)**: Tulisan tangan di mana penulisnya menyadari mereka salah tulis di tengah-tengah goresan, lalu mereka **mencoret/menimpa** tulisan tersebut untuk "mengoreksinya" tanpa menghapus menggunakan penghapus. Ini menghasilkan bentuk tulisan yang sangat berantakan dan saling tumpang tindih.

## 2. Arti Nama Folder Angka (1, 4, 5, 6, 7, 8, 9) — DIREVISI

> [!IMPORTANT]
> **Asumsi awal keliru.** Folder-folder numerik ini **bukan** merepresentasikan karakter angka yang sedang ditulis. Setelah inspeksi manual, terbukti bahwa setiap folder mengandung hampir seluruh abjad huruf yang bervariasi.

Folder numerik tersebut merepresentasikan **Tingkat Keparahan Coretan (Severity Score)** dari goresan tulisan penderita disleksia. Skala aslinya bersifat terbalik dalam konteks *Machine Learning*:
* **Folder 9** = Coretan paling ringan (masih mudah dibaca).
* **Folder 1** = Coretan paling parah (hampir tidak terbaca sama sekali).

Setelah normalisasi melalui *Dictionary Mapping* di `Dyslexia.ipynb`, skala dikonversi menjadi:
* **Skor 1** = Paling Ringan
* **Skor 6** = Paling Parah

## 3. Anomali Visual: Kenapa Karakter Terlihat Seperti Huruf Lain (P, R, Q, M)?
Ketika folder kelas **Corrected** dibuka, goresannya seringkali sama sekali tidak menyerupai karakter asli yang dimaksudkan, melainkan `P`, `R`, atau `M`. Ini bukan kerusakan data — melainkan efek dari kelas itu sendiri:

1. **Efek Kelas Corrected (Koreksi)**: Tulisan yang dihasilkan oleh orang dengan disgrafia/disleksia parah. Ketika mereka mencoba menulis suatu karakter, mereka membuat tarikan garis yang salah (misalnya garis lengkung tak terduga).
2. **Penumpukan Garis (*Scribbling*)**: Alih-alih menghapus dan memulai ulang, penulis menimpa garis tersebut dengan coretan baru.
   * Coretan vertikal digabung coretan diagonal melengkung akan merubah bentuk keseluruhannya menjadi huruf seperti **P** atau **R**.
   * Garis yang salah tarik lalu ditimpa garis lurus bisa menyerupai abjad **Q** atau **S** yang cacat.
   * Tumpang tindih coretan ekstrem menciptakan banyak titik sudut, merubah garis sederhana menjadi bentuk dengan banyak kaki layaknya huruf **M**.

Ini adalah **bukti visual yang sah** dari gejala disgrafia dan menjadi nilai belajar (informasi) yang sangat berharga bagi model AI kita.

## 4. Revisi: Tidak Ada Data Leakage
Asumsi awal bahwa dataset ini mengalami *Data Leakage* fatal (model hanya belajar mengenali karakter) telah **gugur** berkat temuan ini.

Karena hampir semua abjad tersebar merata di seluruh folder keparahan (1–9), model tidak bisa "menghafal karakter untuk menebak kelas". Model terpaksa belajar **pola goresan / texture** dari coretan tersebut — persis seperti yang kita inginkan untuk sistem deteksi disleksia!

## 5. Kontaminasi Label (*Label Noise*) — Temuan Baru
Selain pola Severity Score, ditemukan juga file-file bernama `NormalXXXX.png` yang terselip di dalam folder `Corrected` dan `Reversal`. Ironisnya, konten visual gambar tersebut justru berisi goresan-goresan yang sangat cacat dan berantakan.

Lebih jauh, kelas `Normal` murni dari dataset aslinya pun terbukti mengandung beberapa gambar yang menampilkan coretan tidak wajar. Ini adalah bukti **Label Noise** dari pihak periset asli.

**Tindakan yang diambil:**
* Seluruh file `NormalXXXX.png` yang berada di luar folder `Normal` dibuang (*drop*) melalui proses *Logical Cleaning* di `Dyslexia.ipynb`.
* File tersebut **tidak dihapus secara fisik** dari disk; hanya tidak dimasukkan ke dalam daftar `master_dataset_dyslexia.csv` yang dibaca oleh model AI.
* Keputusan ini menjamin "kebersihan" data latih tanpa mengambil risiko menghapus data asli yang tidak dapat dipulihkan.
