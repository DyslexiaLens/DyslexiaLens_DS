# 📊 Analisis Anomali: Mengapa Skor 1 Kosong pada Distribusi 'Corrected'?

## 🎯 Isu yang Dibahas
Pada grafik "Pola Severity Score per Kategori", khususnya pada sub-grafik **Distribusi Severity Score — Corrected**, terlihat bahwa nilai pada **Severity Score 1** kosong (0 gambar), sedangkan skor 2 hingga 6 memiliki jumlah data yang banyak. Hal ini memunculkan pertanyaan: *Mengapa tidak ada gambar kelas Corrected dengan Skor Keparahan 1 (Paling Ringan)?*

## 🔍 Penjelasan Ilmiah & Historis Dataset
Ketiadaan Skor 1 pada kelas `Corrected` **bukanlah sebuah error atau data yang hilang (missing data)**, melainkan murni merupakan **desain pelabelan dari peneliti asli (periset Dataset Gambo)**.

Untuk memahaminya, kita harus melihat kembali pemetaan (*mapping*) folder asli dari pembuat dataset sebelum kita melakukan standarisasi menjadi skala AI (0-6):

### 1. Struktur Folder Asli dari Peneliti Gambo
Peneliti asli membagi tingkat keparahan gejala disleksia menggunakan angka acak secara terbalik:
* **Kelas `Corrected`** hanya dibagi menjadi 5 folder keparahan: **`4, 5, 6, 7, 8`**.
* **Kelas `Reversal`** memiliki folder keparahan ekstrem: **`1`** (sangat hancur) dan **`9`** (sangat ringan).

### 2. Proses Normalisasi (Mapping ke Skala AI 1-6)
Pada Tahap 2 di notebook `Dyslexia.ipynb`, kita melakukan standarisasi agar model AI dapat belajar secara berurutan (Skor tinggi = Makin Parah). Pemetaannya adalah:

| Skor Asli (Gambo) | Kategori Asal | Skor AI (Kita) | Deskripsi |
|:---:|:---:|:---:|:---|
| **9** | **Hanya Reversal** | **1** | Paling Ringan |
| 8 | Corrected | 2 | |
| 7 | Corrected | 3 | |
| 6 | Corrected | 4 | |
| 5 | Corrected | 5 | |
| 4 | Corrected | 6 | Corrected Parah |
| 1 | Reversal | 6 | Reversal Parah (Disatukan dengan skor 4) |

### 3. Mengapa Skor 1 Corrected Kosong?
Dari tabel pemetaan di atas, **Skor AI 1 berasal dari Skor Asli 9**. Karena peneliti asli **TIDAK PERNAH membuat folder `9` untuk kelas `Corrected`**, maka mustahil bagi kita untuk memiliki data `Corrected` dengan Skor AI 1.

Peneliti asli menganggap bahwa cacat *Corrected* (tulisan yang ditimpa berulang kali) paling ringan pun masih tergolong cukup parah secara visual dibandingkan dengan *Reversal* (terbalik) yang kadang sangat halus perbedaannya dari huruf asli. Oleh karena itu, mereka mengawali pelabelan *Corrected* dari angka 8 (yang kita petakan menjadi AI Skor 2).

## ✅ Kesimpulan & Rekomendasi
* **Status Data:** Valid dan Normal.
* **Tindakan:** Tidak perlu ada perbaikan. Ini adalah cerminan murni dari metodologi pengumpulan data asli (Gambo).
* **Dampak pada Model AI:** CNN yang akan dibangun nanti tidak akan terganggu oleh hal ini. Model AI akan otomatis memahami bahwa setiap ciri-ciri "Corrected" secara minimal sudah memiliki "bobot keparahan" setara dengan Skor 2.
