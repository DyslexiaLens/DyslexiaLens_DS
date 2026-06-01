# 🤖 Dokumen Konteks — AI Engineer: Arsitektur Model & Pipeline Inferensi
**Dibuat:** 1 Juni 2026  
**Terakhir Diperbarui:** 1 Juni 2026  
**Tujuan:** Mendokumentasikan keputusan teknis, arsitektur model, dan alur sistem inferensi yang ditetapkan oleh tim AI Engineer pada proyek DyslexiaLens.  
**Status:** 🟡 Dalam Progres — Model sedang aktif dilatih

---

## 👥 Pembagian Peran

| Peran | Tanggung Jawab |
|---|---|
| **Data Scientist (Rainy)** | Dataset preparation, Feature Engineering, A/B Testing, Dashboard ✅ SELESAI |
| **Data Engineer (w0pal)** | EMNIST integration, pipeline automation ✅ SELESAI |
| **AI Engineer 1** | Model Deteksi Disleksia (Klasifikasi Biner + Regresi Severity) 🟡 AKTIF |
| **AI Engineer 2** | Model OCR (Character Recognition dari grid scan) 🟡 AKTIF |
| **Full-Stack Engineer** | Website, PDF grid generator, scan interface, integrasi FastAPI |

---

## 🧠 Arsitektur Model (Keputusan Final Tim AI)

Tim AI Engineer mengerjakan **dua model yang berbeda secara paralel**, masing-masing dikerjakan oleh satu orang yang berbeda.

---

### 🔬 Model A — Deteksi Disleksia (oleh AI Engineer 1)

Model A sebenarnya adalah **satu kesatuan sistem** yang terdiri dari dua sub-model yang bekerja bersamaan:

#### Sub-Model A1: Klasifikasi Biner
- **Tujuan:** Menentukan apakah tulisan pada satu sel grid mengandung indikasi disleksia atau tidak.
- **Output:** `0 (Normal)` atau `1 (Disleksia)`
- **Fungsi:** Gate pertama — menyaring tulisan mana yang perlu dievaluasi lebih lanjut.

#### Sub-Model A2: Regresi Severity Score
- **Tujuan:** Memprediksi tingkat keparahan goresan tulisan secara numerik.
- **Output:** Skor keparahan (skala masih perlu dikonfirmasi — DS menggunakan 0–6, AI Engineer menyebut 0–10)
- **Fungsi:** Memberikan granularitas penilaian seberapa berat indikasi disleksianya.

> ⚠️ **Catatan penting:** Dataset dari Data Scientist menggunakan skala Severity `0–6`. Jika AI Engineer menggunakan skala `0–10`, perlu ada konfirmasi dan dokumentasi tentang remapping yang digunakan agar tidak terjadi mismatch saat evaluasi.

**Penggunaan Fitur XAI dari Data Scientist:**  
Fitur Engineering yang telah dikerjakan oleh Data Scientist (5 fitur geometri matematis: `ink_density`, `center_of_mass_x/y`, `bounding_box_ratio`, `horizontal_symmetry`, `stroke_transitions`) **digunakan sebagai input tambahan** pada model ini untuk meningkatkan akurasi dan interpretabilitas prediksi.

**Monitoring Training:**
- Menggunakan **TensorBoard** dengan TensorBoard Callback untuk menyimpan log training secara otomatis.
- Log training divisualisasikan menjadi dashboard untuk memantau perkembangan pelatihan model secara real-time (loss, accuracy, F1, dll.).

---

### 🔤 Model B — OCR (Character Recognition) (oleh AI Engineer 2)

#### Arsitektur & Cara Kerja
- **Tujuan:** Mengenali karakter/abjad apa yang ditulis pada tiap sel grid (fitur translasi tulisan tangan → teks).
- **Pendekatan:** Setelah kertas grid di-scan, gambar dipecah menjadi per-karakter (per sel). Setiap sel kemudian dimasukkan ke model OCR untuk mendapatkan prediksi karakter apa yang terdapat di dalamnya.
- **Alur singkat:**
  ```
  Gambar scan → Pecah per sel (Traditional CV) → Tiap sel → Model OCR → Prediksi karakter
  ```
- **Sumber model:** Menggunakan model dari **HuggingFace** yang telah diintegrasikan ke dalam backend.

#### Spesifikasi Teknis
- **Input ke model:** Data gambar dalam format **Base64** (bukan foto mentah/file binary langsung).
- **API Framework:** **FastAPI** — model diekspos sebagai REST API endpoint.
- **Integrasi:** HuggingFace model → FastAPI → Backend aplikasi web.

> 📌 **Referensi Silang CP 4:** Ini adalah implementasi dari **Opsi A (Golden MVP / Smart Grid)** yang telah dirumuskan pada Checkpoint 4. Sistem tidak butuh AI OCR untuk menebak posisi abjad karena koordinat tiap sel di grid sudah diketahui — model hanya bertugas mengenali karakter yang tertulis di dalamnya.

---

## 🖨️ Desain Sistem Grid & Alur Inferensi

### Keputusan Arsitektur Grid
- Satu format kertas grid PDF yang **sama** digunakan untuk **Fitur 1** (Deteksi Disleksia) dan **Fitur 2** (OCR / Translasi Tulisan).
- User mendownload PDF → Print → Tulis di atas kertas → Scan/Foto → Upload ke aplikasi.
- Pemrosesan gambar scan menggunakan **Traditional Computer Vision** (kemungkinan OpenCV): deteksi garis grid → segmentasi koordinat → crop per sel.

### Alur Lengkap User Journey

```
[1] User buka aplikasi web DyslexiaLens
        │
        ▼
[2] User download PDF Grid Template (via link di aplikasi)
        │
        ▼
[3] User PRINT kertas grid
        │
        ▼
[4] User TULIS tulisan tangan di atas sel-sel grid
        │
        ▼
[5] User SCAN / FOTO kertas → Upload ke aplikasi
        │
        ▼
[6] Backend (Traditional CV / OpenCV):
    → Deteksi grid
    → Crop tiap sel
    → Encode ke Base64
        │
        ├──────────────────────────────────────────┐
        ▼                                          ▼
[7A] Tiap sel → FastAPI (Model A)          [7B] Tiap sel → FastAPI (Model B / HuggingFace)
    → Klasifikasi Biner (Disleksia/Normal)      → OCR: Prediksi karakter apa
    → Regresi Severity Score                        yang tertulis di sel
        │                                          │
        └──────────────┬───────────────────────────┘
                       ▼
              [8] Hasil ditampilkan di aplikasi:
                  → Grid dengan highlight sel bermasalah
                  → Skor Severity per karakter
                  → Teks hasil translasi OCR per sel
                  → Ringkasan keseluruhan
```

---

## 🔗 Catatan Integrasi Antar Tim

### Untuk Full-Stack Engineer:
- Siapkan halaman **Download PDF Grid** di early onboarding flow.
- Endpoint upload menerima gambar scan (JPG/PNG).
- Backend melakukan preprocessing (CV → crop → Base64) sebelum dikirim ke FastAPI.
- Tampilkan hasil: highlight merah/hijau per sel + teks OCR + skor severity (user-friendly, bukan angka mentah).

### Untuk AI Engineer 1 (Model Deteksi):
- Konfirmasi skala Severity yang digunakan (`0–6` dari DS atau `0–10`). Dokumentasikan remapping jika berbeda.
- Tentukan threshold confidence untuk Klasifikasi Biner.
- Gunakan `Weighted F1-Score` sebagai metrik utama (bukan Accuracy).
- **JANGAN** gunakan augmentasi rotasi/flip — akan merusak sinyal Reversal Error. (Lihat SLA Constraints di `Konteks_Handover_AI_Agent.md`)

### Untuk AI Engineer 2 (Model OCR):
- Pastikan model HuggingFace yang dipilih mendukung karakter Latin A–Z dan a–z.
- Input Base64 harus sudah di-normalize ukurannya (28×28 grayscale) sebelum dikirim ke model, agar konsisten dengan distribusi training data EMNIST.
- Dokumentasikan nama/versi model HuggingFace yang digunakan sebagai referensi reproducibility.

---

## 📌 Status & Hal yang Masih Perlu Dikonfirmasi

| Hal | Status |
|---|---|
| Model A: Klasifikasi Biner + Regresi Severity (satu kesatuan) | ✅ Dikonfirmasi |
| Model B: OCR via HuggingFace + FastAPI | ✅ Dikonfirmasi |
| Input model: Base64 (bukan foto mentah) | ✅ Dikonfirmasi |
| TensorBoard Callback untuk monitoring training | ✅ Dikonfirmasi |
| Pilihan arsitektur Grid (Opsi A dari CP 4) | ✅ Dikonfirmasi |
| Skala Severity yang digunakan di model (0–6 atau 0–10) | ⚠️ Perlu konfirmasi |
| Nama/versi model HuggingFace yang dipakai (Model B) | ⚠️ Perlu dicatat |
| Format grid PDF sudah didesain | ⚠️ Perlu konfirmasi |
| Threshold confidence Klasifikasi Biner | ⚠️ Belum ditentukan |
| Detail teknis Traditional CV untuk crop grid | ⚠️ Masih dalam pengerjaan |
