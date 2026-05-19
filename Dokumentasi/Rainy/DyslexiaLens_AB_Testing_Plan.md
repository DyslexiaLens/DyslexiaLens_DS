# 🧪 Rencana A/B Testing — Proyek DyslexiaLens

Dokumen ini memaparkan dua jalur (opsi) metodologi A/B Testing untuk mengevaluasi strategi *Dual-Track Dataset* pada proyek DyslexiaLens. Eksekusi bergantung pada ketersediaan model dari tim AI Engineer.

---

## 🚦 Dua Skenario A/B Testing

Kita memiliki dua varian dataset:
- **Dataset A (Kontrol):** `master_dataset_final_balanced_rill_featured.csv` (Hanya Gambo asli, ~180k gambar)
- **Dataset B (Perlakuan):** `master_dataset_emnist_balanced_final_featured.csv` (Gambo + EMNIST, ~273k gambar)

Karena bekerja dalam tim, terdapat dua pendekatan yang bisa diambil untuk membuktikan keberhasilan eksperimen secara statistik:

---

## 🟢 OPSI A: Pendekatan Mandiri Data Scientist (Tanpa AI Engineer)

**Fokus Utama:** Integritas Data dan Pelestarian Karakteristik Alami Tulisan Disleksia.
**Kondisi Penggunaan:** Digunakan apabila model *Deep Learning* dari tim AI Engineer belum selesai dilatih, namun Data Scientist dituntut untuk segera menyelesaikan validasi akhir (*submission*) atas pekerjaannya meracik dataset.

### 1. Konteks Bisnis & Mengapa Ini Valid Sebagai A/B Testing?
Dalam siklus pengembangan *Machine Learning*, kualitas data menentukan kualitas model (*Garbage In, Garbage Out*). Eksperimen kita bertujuan untuk menyeimbangkan jumlah kelas (agar rasio Disleksia : Normal menjadi 1:1) dengan menyuntikkan data pihak ketiga (EMNIST). 

**Masalah Bisnis:** Apakah data pihak ketiga ini "merusak" keaslian karakteristik tulisan tangan penderita disleksia? Jika rusak, model AI nantinya akan belajar pola yang salah dan justru gagal mendeteksi disleksia di dunia nyata.

Sesuai kaidah pengujian di kelas Dicoding, eksperimen *A/B Testing* harus memiliki kerangka kerja yang solid:
- **Control Group (Dataset A):** Dataset murni tanpa injeksi eksternal. Ini adalah *baseline* keaslian data.
- **Treatment Group (Dataset B):** Dataset yang telah diberikan "perlakuan" berupa injeksi algoritma *Fair Pruning* menggunakan EMNIST.
- **Evaluation Metric:** 6 fitur *Explainable AI* (XAI) matematis (seperti `ink_density`, `stroke_transitions`, dll). Fitur ini bertindak sebagai representasi kuantitatif dari "pola alami" sebuah tulisan tangan.

Maka, A/B Testing ini bertujuan murni untuk menjawab: **Apakah perlakuan injeksi EMNIST mengubah karakteristik fundamental (distribusi fitur XAI) dari dataset secara statistik?**

### 2. Perumusan Hipotesis & Pengambilan Keputusan
```
H₀ (Hipotesis Nol):
  Tidak ada perbedaan signifikan pada distribusi fitur antara Dataset A dan Dataset B.
  → Augmentasi EMNIST tidak mengubah karakteristik data secara bermakna.

H₁ (Hipotesis Alternatif):
  Ada perbedaan signifikan pada distribusi fitur antara Dataset A dan Dataset B.
  → Augmentasi EMNIST mengubah karakteristik data secara nyata.

Alpha (α) = 0.05
Uji: Two-sided (dua sisi)
```

### Metrik yang Dibandingkan
Enam fitur XAI yang sudah diekstrak menjadi metrik utama A/B Testing:

| Fitur | Deskripsi |
|---|---|
| `ink_density` | Kepadatan tinta (proporsi piksel hitam) |
| `center_of_mass_x` | Posisi horizontal pusat massa |
| `center_of_mass_y` | Posisi vertikal pusat massa |
| `bounding_box_ratio` | Rasio tinggi/lebar kotak bounding box |
| `stroke_transitions` | Jumlah transisi hitam-putih (kompleksitas goresan) |
| `horizontal_symmetry` | Skor simetri horizontal tulisan |

Untuk setiap fitur ini, bandingkan distribusinya antara Dataset A vs Dataset B.

### Uji Statistik: Mann-Whitney U Test (Non-Parametrik)
Dipilih karena:
- Distribusi fitur kemungkinan **tidak normal** (data gambar handwriting).
- Tidak memerlukan asumsi distribusi tertentu.
- Cocok untuk membandingkan dua grup independen.

### Kode Implementasi (Opsi A)
```python
import pandas as pd
from scipy.stats import mannwhitneyu

# 1. Load Datasets
# Pastikan nama file disesuaikan dengan path directory kamu
df_A = pd.read_csv('master_dataset_final_balanced_rill_featured.csv')
df_B = pd.read_csv('master_dataset_emnist_balanced_final_featured.csv')

# 2. Definisikan 6 Fitur XAI yang akan diuji
features = [
    'ink_density', 'center_of_mass_x', 'center_of_mass_y', 
    'bounding_box_ratio', 'stroke_transitions', 'horizontal_symmetry'
]

# 3. Eksekusi Mann-Whitney U Test untuk setiap fitur
results = []
alpha = 0.05

for feature in features:
    val_A = df_A[feature].dropna()
    val_B = df_B[feature].dropna()
    
    # Lakukan uji statistik dua sisi
    stat, p_value = mannwhitneyu(val_A, val_B, alternative='two-sided')
    
    # Tentukan keputusan statistik
    if p_value > alpha:
        conclusion = "Gagal Tolak H0 (Distribusi Sama - AMAN)"
    else:
        conclusion = "Tolak H0 (Distribusi Berbeda - BERUBAH)"
        
    results.append({
        'Fitur XAI': feature,
        'P-Value': p_value,
        'Keputusan Statistik': conclusion
    })

# 4. Tampilkan Hasil Analisis
df_results = pd.DataFrame(results)
display(df_results)

# -------------------------------------------------------------
# KESIMPULAN BISNIS / INTERPRETASI:
# -------------------------------------------------------------
# Jika mayoritas fitur "Gagal Tolak H0", maka secara keseluruhan 
# penambahan dataset EMNIST *sangat direkomendasikan* karena berhasil 
# menyeimbangkan kelas (1:1) tanpa mendistorsi karakteristik asli disleksia.
```

---

## 🔵 OPSI B: Pendekatan Kolaboratif (*End-to-End* dengan AI Engineer)

**Fokus Utama:** Evaluasi Performa Model dan Kecerdasan Buatan Akhir.
**Kondisi Penggunaan:** Digunakan apabila tim AI Engineer sudah sepenuhnya menyelesaikan proses *training* dan *inference* terhadap Model A (menggunakan Dataset A) dan Model B (menggunakan Dataset B).

### 1. Konteks Bisnis & Metodologi Uji
Pada skenario ini, kita menggeser metrik evaluasi dari ranah "Integritas Data" (tugas DS) ke ranah "Akurasi Prediksi" (tugas AI). Objektif akhirnya adalah membuktikan secara empiris apakah jerih payah Data Scientist dalam menyuntikkan dataset EMNIST benar-benar menghasilkan model AI yang lebih cerdas dan akurat dalam mendeteksi disleksia.

Karena kedua model dievaluasi pada **lembar ujian (Test Set) yang sama persis**, kita diwajibkan menggunakan kaidah statistik untuk **Data Berpasangan (*Paired Data*)**. 
Oleh karena itu, kita **TIDAK BOLEH** menggunakan *A/B Testing* standar seperti Two-Sample Z-Test atau T-Test independen, melainkan wajib menggunakan **McNemar Test**. McNemar Test adalah standar emas (SOP) di ranah *Machine Learning* untuk membandingkan dua *classifier* karena ia secara spesifik hanya membandingkan **ketidaksepakatan (*disagreement*)** antara tebakan Model A dan Model B.

### 2. Kebutuhan Eksternal (Dari AI Engineer)
Untuk mengeksekusi A/B Testing ini, Data Scientist tidak perlu repot menyentuh arsitektur kode *training* model sama sekali. Cukup meminta satu buah file `hasil_prediksi.csv` dari tim AI yang wajib berisi 4 kolom:
1. `image_path` (identifier file gambar).
2. `true_label` (kunci jawaban kelas aslinya).
3. `pred_model_A` (tebakan dari Model yang dilatih dengan Dataset murni).
4. `pred_model_B` (tebakan dari Model yang dilatih dengan Dataset + EMNIST).

### 3. Perumusan Hipotesis & Pengambilan Keputusan
```
H₀ (Hipotesis Nol):
  Akurasi Model A = Akurasi Model B 
  → Dataset EMNIST tidak memberi efek nyata pada performa akhir.

H₁ (Hipotesis Alternatif):
  Akurasi Model A ≠ Akurasi Model B 
  → Terdapat perbedaan performa yang nyata berkat penambahan EMNIST.

Alpha (α) = 0.05
Uji: Two-sided (dua sisi)
```

### Kode Implementasi (Opsi B)
```python
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar

# 1. Load data hasil tebakan AI Engineer
df = pd.read_csv('hasil_prediksi.csv')

# 2. Evaluasi kebenaran prediksi masing-masing model (1=Benar, 0=Salah)
df['A_correct'] = (df['pred_model_A'] == df['true_label'])
df['B_correct'] = (df['pred_model_B'] == df['true_label'])

# 3. Hitung metrik akurasi dasar untuk konteks (Opsional)
acc_A = df['A_correct'].mean() * 100
acc_B = df['B_correct'].mean() * 100
print(f"Akurasi Model A (Tanpa EMNIST): {acc_A:.2f}%")
print(f"Akurasi Model B (Dengan EMNIST): {acc_B:.2f}%\n")

# 4. Buat Tabel Kontingensi (Disagreement Table)
# a = Keduanya Benar             | b = Model A Benar, Model B Salah
# c = Model A Salah, Model B Benar | d = Keduanya Salah
a = len(df[(df['A_correct'] == True) & (df['B_correct'] == True)])
b = len(df[(df['A_correct'] == True) & (df['B_correct'] == False)])
c = len(df[(df['A_correct'] == False) & (df['B_correct'] == True)])
d = len(df[(df['A_correct'] == False) & (df['B_correct'] == False)])

table = [[a, b], 
         [c, d]]

# 5. Eksekusi McNemar Test
alpha = 0.05
result = mcnemar(table, exact=False, correction=True)
p_value = result.pvalue

print(f"P-Value McNemar Test: {p_value}\n")

# 6. Pengambilan Keputusan Bisnis
print("=== KESIMPULAN BISNIS ===")
if p_value <= alpha:
    print("Keputusan Statistik: Tolak H0 (Terdapat perbedaan performa yang signifikan).")
    print("Tindakan: Pilih model (dan dataset) dengan akurasi tertinggi untuk fase Production.")
else:
    print("Keputusan Statistik: Gagal Tolak H0 (Perbedaan akurasi tidak signifikan secara statistik).")
    print("Tindakan: Gunakan Dataset A (NoAugmentation) karena secara operasional lebih ringan namun performanya setara.")
```

---

## 📋 SOP Rekomendasi Eksekusi
Berdasarkan kondisi proyek saat ini, disarankan untuk:
1. **Lakukan Opsi A terlebih dahulu** hari ini, untuk mengamankan kewajiban kelengkapan *submission Data Science* (mengingat semua data CSV fitur XAI sudah kamu miliki).
2. **Siapkan *script* Opsi B**, dan segera eksekusi uji *McNemar* ini di tahap akhir proyek apabila AI Engineer berhasil mengirimkan file prediksi sebelum *deadline*.
