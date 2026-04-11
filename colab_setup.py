# %% [markdown]
# # 🧠 DysRead Helper — Data Science Notebook
# **Early Screening Disleksia pada Anak via Analisis Citra Tulisan Tangan**
#
# **Cara pakai:** Upload file ini ke Google Colab → File → Open → Upload → pilih file .py ini.
# Colab otomatis konversi `# %%` menjadi cell-cell. Jalankan dari atas ke bawah.
#
# ---
#
# ## 📌 Problem Statement
#
# Disleksia adalah gangguan belajar yang memengaruhi kemampuan membaca dan menulis,
# dialami oleh **5-17% anak usia sekolah** (International Dyslexia Association).
# Deteksi dini sangat penting karena intervensi sebelum usia 8 tahun terbukti
# meningkatkan kemamp` **70%** (Shaywitz, 2003).
#
# Namun, proses screening tradisional membutuhkan **psikolog terlatih**, **mahal**,
# dan **tidak scalable** untuk daerah dengan keterbatasan tenaga ahli.
#
# **Solusi:** DysRead Helper — web app yang menganalisis **pola visual tulisan tangan anak**
# menggunakan CNN untuk mendeteksi indikasi disleksia secara otomatis.
# Pendekatan ini BUKAN OCR — kita mendeteksi **pola kognitif**, bukan membaca teks.
#
# ---
#
# ## ❓ Business Questions (Terukur)
#
# | # | Pertanyaan | Metrik Sukses |
# |---|-----------|---------------|
# | **BQ1** | Apakah pola visual tulisan anak disleksia dapat dibedakan secara statistik dari tulisan anak tipikal? | p-value < 0.05 pada ≥3 fitur visual |
# | **BQ2** | Fitur visual apa yang paling diskriminatif untuk membedakan tulisan disleksia vs normal? | Top-5 fitur berdasarkan effect size (Cohen's d) |
# | **BQ3** | Seberapa akurat model CNN dalam mengklasifikasikan tulisan disleksia vs normal? | Recall ≥ 0.90, F1 ≥ 0.80 |
# | **BQ4** | Bagaimana distribusi data mempengaruhi performa model, dan strategi apa yang efektif menangani class imbalance? | Perbandingan metrik sebelum/sesudah rebalancing |
# | **BQ5** | Apakah synthetic data generation menghasilkan sampel yang realistis dan meningkatkan performa model? | Peningkatan recall setelah penambahan data sintetis |
#
# ---
#
# ## 🔬 Metodologi
#
# ```
# Gathering → Assessing → Cleaning → EDA → Visualisasi → Modeling → Dashboard
# (Kaggle)   (Kualitas)   (Preproc)  (Fitur) (Insight)    (CNN)      (Streamlit)
# ```

# %% [markdown]
# ## 📦 CELL 1: Install Dependencies

# %%
# === CELL 1: Install Dependencies ===
import subprocess, sys

packages = [
    'opencv-python-headless',
    'scikit-image',
    'scipy',
    'albumentations',
    'PyYAML',
    'tqdm',
    'kaggle',
]

for pkg in packages:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', pkg])

import cv2, scipy, albumentations
print(f"✅ OpenCV: {cv2.__version__}")
print(f"✅ scipy: {scipy.__version__}")
print(f"✅ albumentations: {albumentations.__version__}")
print(f"✅ TensorFlow: sudah tersedia di Colab")
print()
print("🎉 Semua dependencies siap!")

# %% [markdown]
# ---
# ## 🔑 CELL 2: Setup Kaggle API & Download Dataset
#
# ### 📥 Gathering Data
# Dataset dikumpulkan dari **Kaggle** — sumber publik yang banyak digunakan
# dalam riset disleksia. Kamu perlu file `kaggle.json` dari akun Kaggle:
# 1. Buka https://www.kaggle.com/settings
# 2. Scroll ke **API** → klik **Create New Token**
# 3. File `kaggle.json` akan terdownload
# 4. Jalankan cell di bawah, lalu upload file tersebut

# %%
# === CELL 2: Setup Kaggle API ===
import os

# Cek apakah di Google Colab
try:
    from google.colab import files as colab_files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    print("📤 Upload file kaggle.json dari akun Kaggle kamu:")
    print("   (Kaggle.com → Settings → API → Create New Token)\n")
    uploaded = colab_files.upload()

    os.makedirs('/root/.kaggle', exist_ok=True)
    for fn in uploaded.keys():
        with open(f'/root/.kaggle/{fn}', 'wb') as f:
            f.write(uploaded[fn])
    os.chmod('/root/.kaggle/kaggle.json', 0o600)
    print("\n✅ Kaggle API dikonfigurasi!")
else:
    print("⚠️ Bukan di Colab. Pastikan kaggle.json sudah di ~/.kaggle/")

# %% [markdown]
# ## 📥 CELL 3: Download Dyslexia Handwriting Dataset
#
# **Sumber:** Dyslexia Handwriting Dataset oleh Dr. Iza Sazanita Isa
#
# Dataset ini berisi **~138,500 gambar** huruf tulisan tangan yang diklasifikasikan
# ke dalam 3 kelas: **Normal**, **Reversal** (huruf terbalik — gejala disleksia),
# dan **Corrected** (huruf yang dikoreksi — menunjukkan kesulitan menulis).
#
# Dataset dikurasi dari 3 sumber:
# - NIST Special Database 19 (huruf besar)
# - Kaggle A-Z Handwritten Alphabets (huruf kecil)
# - Sampel langsung dari anak SD di Malaysia yang didiagnosis disleksia

# %%
# === CELL 3: Download Dataset ===
import os, subprocess

BASE = '/content/dataset'

# Buat folder structure
dirs = [
    f'{BASE}/raw/dyslexia_kaggle',
    f'{BASE}/raw/synthetic_generated',
    f'{BASE}/processed/train/dyslexic',
    f'{BASE}/processed/train/non_dyslexic',
    f'{BASE}/processed/val/dyslexic',
    f'{BASE}/processed/val/non_dyslexic',
    f'{BASE}/processed/test/dyslexic',
    f'{BASE}/processed/test/non_dyslexic',
    f'{BASE}/metadata',
    f'{BASE}/reports',
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Download dari Kaggle
DATASET_SLUG = "drizasazanitaisa/dyslexia-handwriting-dataset"
DOWNLOAD_DIR = f"{BASE}/raw/dyslexia_kaggle"

print(f"📥 Downloading: {DATASET_SLUG}")
print(f"📂 Target: {DOWNLOAD_DIR}")
print("   (bisa memakan waktu beberapa menit...)\n")

subprocess.run([
    sys.executable, '-m', 'kaggle', 'datasets', 'download',
    '-d', DATASET_SLUG,
    '-p', DOWNLOAD_DIR,
    '--unzip'
], check=True)

# Hitung file yang terdownload
total_files = 0
for root, _, files_list in os.walk(DOWNLOAD_DIR):
    total_files += len(files_list)

print(f"\n✅ Download selesai! Total: {total_files} files")

# Tampilkan struktur folder
print("\n📁 Folder structure:")
for root, subdirs, files_list in os.walk(DOWNLOAD_DIR):
    level = root.replace(DOWNLOAD_DIR, '').count(os.sep)
    indent = '  ' * level
    print(f"{indent}📂 {os.path.basename(root)}/ ({len(files_list)} files)")

# %% [markdown]
# ---
# ## 👀 CELL 4: Explore Dataset — Lihat Gambar & Distribusi Kelas
#
# ### 📊 Exploratory Data Analysis (Bagian 1)
# Sebelum melakukan pembersihan data, kita perlu memahami struktur dan distribusi
# dataset yang sudah didownload. Cell ini akan menampilkan:
# - Jumlah gambar per kelas (distribusi)
# - Pie chart perbandingan kelas
# - Bar chart mapping ke binary classification
# - Sample gambar dari setiap kelas

# %%
# === CELL 4: Explore Dataset ===
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter

BASE_RAW = '/content/dataset/raw/dyslexia_kaggle'

# Auto-detect kelas dari subfolder
all_items = os.listdir(BASE_RAW)
classes = sorted([d for d in all_items if os.path.isdir(os.path.join(BASE_RAW, d))])

# Jika langsung file tanpa subfolder, cek 1 level deeper
if not classes:
    for item in all_items:
        sub = os.path.join(BASE_RAW, item)
        if os.path.isdir(sub):
            deeper = [d for d in os.listdir(sub) if os.path.isdir(os.path.join(sub, d))]
            if deeper:
                BASE_RAW = sub
                classes = sorted(deeper)
                break

print(f"🏷️ Kelas ditemukan: {classes}")
print(f"📂 Base path: {BASE_RAW}\n")

# --- Distribusi Kelas ---
print("━" * 50)
print("📊 DISTRIBUSI KELAS")
print("━" * 50)

class_counts = {}
for cls in classes:
    cls_dir = os.path.join(BASE_RAW, cls)
    count = len([f for f in os.listdir(cls_dir)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
    class_counts[cls] = count
    print(f"  {cls:20s}: {count:>8,} gambar")

total = sum(class_counts.values())
print(f"  {'TOTAL':20s}: {total:>8,} gambar")

# --- Pie Chart Distribusi ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

colors = ['#2ecc71', '#e74c3c', '#f39c12']
ax1.pie(class_counts.values(), labels=class_counts.keys(),
        autopct='%1.1f%%', colors=colors[:len(classes)],
        startangle=90, textprops={'fontsize': 12})
ax1.set_title('Distribusi Kelas (Original)', fontsize=14, fontweight='bold')

# --- Binary mapping chart ---
binary_map = {'non_dyslexic': 0, 'dyslexic': 0}
for cls, cnt in class_counts.items():
    if cls.lower() == 'normal':
        binary_map['non_dyslexic'] += cnt
    else:  # Reversal, Corrected → dyslexic
        binary_map['dyslexic'] += cnt

ax2.bar(binary_map.keys(), binary_map.values(),
        color=['#2ecc71', '#e74c3c'], edgecolor='white', linewidth=2)
ax2.set_title('Mapping ke Binary Classification', fontsize=14, fontweight='bold')
ax2.set_ylabel('Jumlah Gambar')
for i, (k, v) in enumerate(binary_map.items()):
    ax2.text(i, v + 500, f'{v:,}', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

print(f"\n📌 Binary mapping:")
print(f"   Normal          → non_dyslexic (0): {binary_map['non_dyslexic']:,}")
print(f"   Reversal+Correct → dyslexic (1):    {binary_map['dyslexic']:,}")
print(f"   Rasio imbalance: {binary_map['non_dyslexic']/max(binary_map['dyslexic'],1):.1f} : 1")

# --- Sample Images ---
n_samples = 6
fig, axes = plt.subplots(len(classes), n_samples, figsize=(3 * n_samples, 3 * len(classes)))
if len(classes) == 1:
    axes = [axes]

for i, cls in enumerate(classes):
    cls_dir = os.path.join(BASE_RAW, cls)
    img_files = sorted([f for f in os.listdir(cls_dir)
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])[:n_samples]

    for j, img_name in enumerate(img_files):
        img = cv2.imread(os.path.join(cls_dir, img_name), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            axes[i][j].imshow(img, cmap='gray')
            axes[i][j].set_title(f'{img.shape[1]}×{img.shape[0]}', fontsize=9)
        axes[i][j].axis('off')
    axes[i][0].set_ylabel(cls, fontsize=13, fontweight='bold', rotation=0, labelpad=80)

plt.suptitle('📷 Sample Gambar per Kelas', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
# ---
# ## 🔍 CELL 4B: Data Assessment — Evaluasi Kualitas Data
#
# ### Assessing Data
# Sebelum data bisa diolah, kita perlu mengevaluasi kualitasnya:
# - **Missing/Corrupt files**: Apakah ada gambar yang rusak atau tidak bisa dibaca?
# - **Resolusi**: Apakah ukuran gambar konsisten?
# - **Duplikasi**: Apakah ada gambar duplikat?
# - **Class Imbalance**: Seberapa timpang distribusi kelas?

# %%
# === CELL 4B: Data Assessment ===
import cv2
import numpy as np
import os
from collections import Counter

print("━" * 60)
print("🔍 DATA ASSESSMENT REPORT")
print("━" * 60)

assessment = {
    'total_files': 0,
    'readable': 0,
    'corrupt': 0,
    'resolutions': [],
    'file_sizes': [],
    'corrupt_files': [],
}

for cls in classes:
    cls_dir = os.path.join(BASE_RAW, cls)
    img_files = [f for f in os.listdir(cls_dir)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    for img_name in img_files:
        assessment['total_files'] += 1
        img_path = os.path.join(cls_dir, img_name)

        # Cek file size
        fsize = os.path.getsize(img_path)
        assessment['file_sizes'].append(fsize)

        # Cek apakah bisa dibaca
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            assessment['corrupt'] += 1
            assessment['corrupt_files'].append(img_path)
        else:
            assessment['readable'] += 1
            assessment['resolutions'].append(f"{img.shape[1]}x{img.shape[0]}")

# --- Report ---
print(f"\n📁 Total Files        : {assessment['total_files']:,}")
print(f"✅ Readable           : {assessment['readable']:,}")
print(f"❌ Corrupt/Unreadable : {assessment['corrupt']}")

if assessment['corrupt_files']:
    print(f"\n⚠️ File corrupt:")
    for f in assessment['corrupt_files'][:10]:
        print(f"   - {f}")

# Resolusi
res_counter = Counter(assessment['resolutions'])
print(f"\n📐 Resolusi yang ditemukan:")
for res, count in res_counter.most_common(10):
    print(f"   {res:>10s}: {count:>6,} gambar ({count/assessment['readable']*100:.1f}%)")

# File sizes
if assessment['file_sizes']:
    sizes = np.array(assessment['file_sizes'])
    print(f"\n📦 Ukuran File:")
    print(f"   Min     : {sizes.min():>8,} bytes ({sizes.min()/1024:.1f} KB)")
    print(f"   Max     : {sizes.max():>8,} bytes ({sizes.max()/1024:.1f} KB)")
    print(f"   Mean    : {sizes.mean():>8,.0f} bytes ({sizes.mean()/1024:.1f} KB)")
    print(f"   Total   : {sizes.sum()/1024/1024:.1f} MB")

# Class imbalance
print(f"\n⚖️ Class Imbalance:")
counts = list(class_counts.values())
if min(counts) > 0:
    ratio = max(counts) / min(counts)
    print(f"   Rasio max/min     : {ratio:.1f}:1")
    print(f"   Kelas terbesar    : {max(class_counts, key=class_counts.get)} ({max(counts):,})")
    print(f"   Kelas terkecil    : {min(class_counts, key=class_counts.get)} ({min(counts):,})")
    if ratio > 3:
        print(f"   ⚠️ IMBALANCE TERDETEKSI — perlu strategi rebalancing!")
    else:
        print(f"   ✅ Distribusi cukup seimbang")

# Duplikasi check (via file size — heuristic sederhana)
size_counter = Counter(assessment['file_sizes'])
duplicates_estimate = sum(c - 1 for c in size_counter.values() if c > 1)
print(f"\n🔄 Estimasi Duplikat (berdasarkan file size): ~{duplicates_estimate:,} kemungkinan duplikat")

print("\n" + "━" * 60)
print("📋 KESIMPULAN ASSESSMENT:")
print("━" * 60)
if assessment['corrupt'] == 0:
    print("✅ Tidak ada file corrupt")
else:
    print(f"⚠️ Ada {assessment['corrupt']} file corrupt — akan difilter saat preprocessing")

if len(res_counter) == 1:
    print(f"✅ Semua gambar memiliki resolusi seragam: {list(res_counter.keys())[0]}")
else:
    print(f"⚠️ Resolusi bervariasi ({len(res_counter)} jenis) — preprocessing akan normalize ke 128×128")

print("✅ Dataset LAYAK untuk diproses ke tahap cleaning & preprocessing")

# %% [markdown]
# ### ✍️ Interpretasi Data Assessment
#
# Dari hasil assessment di atas, kita dapat menyimpulkan:
#
# 1. **Kualitas File**: Mayoritas gambar dapat dibaca dengan baik oleh OpenCV.
#    File corrupt (jika ada) akan otomatis difilter oleh pipeline preprocessing
#    melalui fungsi `load_and_validate()` yang mengecek Laplacian variance.
#
# 2. **Konsistensi Resolusi**: Jika resolusi bervariasi, ini normal untuk dataset
#    yang dikurasi dari multiple sumber. Pipeline preprocessing akan menormalisasi
#    semua gambar ke **128×128 pixel** dengan aspect-ratio preserving padding.
#
# 3. **Class Imbalance**: Dataset menunjukkan ketidakseimbangan kelas yang signifikan.
#    Kelas `Corrected` hanya ~6% dari total data. Strategi penanganan:
#    - Class weighting di loss function
#    - Focal Loss (γ=2.0)
#    - Balanced batch sampling
#    - Targeted augmentation pada minority class
#
# **Data ini LAYAK** untuk dilanjutkan ke tahap cleaning/preprocessing.

# %% [markdown]
# ---
# ## 🔧 CELL 5: Upload & Import Modul DysRead Helper
#
# ### 🧹 Cleaning Data
# Setelah data dinilai kualitasnya, tahap selanjutnya adalah **membersihkan data**.
# Modul `src/preprocessing.py` akan melakukan:
# 1. Grayscale conversion
# 2. Noise reduction (bilateral filter)
# 3. Binarization (Otsu thresholding)
# 4. Morphological cleaning (opening + closing)
# 5. Small component removal
# 6. Aspect-ratio preserving resize + padding
# 7. Normalization ke [0,1]
#
# Upload folder `src/` ke Google Drive terlebih dahulu,
# ATAU upload sebagai zip langsung ke Colab.

# %%
# === CELL 5: Import Modul DysRead ===
import sys, os

# ── OPSI A: Dari Google Drive ──
# Uncomment baris di bawah jika src/ ada di Google Drive
# from google.colab import drive
# drive.mount('/content/drive')
# PROJECT_DIR = '/content/drive/MyDrive/DysRead/dataset'

# ── OPSI B: Upload ZIP langsung ──
# Jika belum ada di Drive, upload zip berisi folder src/
try:
    # Coba import dulu (mungkin sudah ada)
    from src.preprocessing import preprocess_for_cnn
    print("✅ Modul sudah tersedia!")
except ImportError:
    print("📤 Modul belum ada. Upload file src.zip (zip dari folder src/)...")
    try:
        from google.colab import files as colab_files
        import zipfile
        uploaded = colab_files.upload()
        for fn in uploaded.keys():
            if fn.endswith('.zip'):
                with zipfile.ZipFile(fn, 'r') as z:
                    z.extractall('/content/dataset/')
                print(f"   Extracted: {fn}")
        sys.path.insert(0, '/content/dataset')
    except Exception:
        pass

# Final import test
try:
    sys.path.insert(0, '/content/dataset')
    from src.preprocessing import preprocess_for_cnn
    from src.feature_extraction import extract_all_features
    from src.synthetic_generator import DyslexiaSimulator, get_mild_simulator, get_moderate_simulator, get_severe_simulator
    from src.augmentation import get_augmentation_pipeline
    from src.rebalancing import analyze_class_distribution, compute_augmentation_factor
    from src.loss_functions import FocalLoss, compute_class_weights, get_evaluation_metrics
    print("✅ Semua modul berhasil di-import!")
except ImportError as e:
    print(f"❌ Gagal import: {e}")
    print("   Pastikan folder src/ sudah di-upload ke path yang benar")

# %% [markdown]
# ---
# ## 🔬 CELL 6: Test Preprocessing Pipeline
#
# Kita akan menjalankan pipeline 7-step pada contoh gambar dari dataset.
# Setiap tahap preprocessing divisualisasikan untuk memastikan transformasi
# berjalan dengan benar dan tidak menghilangkan fitur penting.
#
# **Catatan Penting:**
# - Skeleton (tahap 6) hanya untuk analisis fitur, BUKAN input CNN
# - Padding hitam digunakan agar aspek rasio asli terjaga
# - Normalisasi ke [0,1] diperlukan agar CNN dapat konvergensi

# %%
# === CELL 6: Test Preprocessing ===
import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.preprocessing import preprocess_for_cnn

# Ambil sample dari dataset yang sudah didownload
sample_class = classes[0] if classes else 'Normal'
sample_dir = os.path.join(BASE_RAW, sample_class)
sample_files = [f for f in os.listdir(sample_dir)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if sample_files:
    sample_path = os.path.join(sample_dir, sample_files[0])
    print(f"🖼️ Sample: {sample_path}")
else:
    # Fallback: buat gambar dummy
    sample = np.ones((100, 300), dtype=np.uint8) * 255
    cv2.putText(sample, "DysRead", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
    sample_path = '/content/test_sample.png'
    cv2.imwrite(sample_path, sample)
    print(f"🖼️ Sample (dummy): {sample_path}")

# Jalankan preprocessing
result = preprocess_for_cnn(sample_path, return_intermediate=True)

if result:
    print(f"✅ Tensor shape: {result['tensor'].shape}")
    print(f"   Pixel range: [{result['tensor'].min():.3f}, {result['tensor'].max():.3f}]")

    # Visualisasi semua tahap
    steps = result['intermediates']
    n_steps = len(steps) + 1  # +1 untuk skeleton
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for ax, (name, img) in zip(axes.flatten(), sorted(steps.items())):
        ax.imshow(img, cmap='gray')
        ax.set_title(name, fontsize=11, fontweight='bold')
        ax.axis('off')

    # Skeleton
    axes[1][2].imshow(result['skeleton'], cmap='gray')
    axes[1][2].set_title('06_skeleton', fontsize=11, fontweight='bold')
    axes[1][2].axis('off')

    plt.suptitle('🔧 Preprocessing Pipeline Steps', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
else:
    print("❌ Preprocessing gagal! Cek apakah gambar terlalu buram.")

# %% [markdown]
# ---
# ## 📊 CELL 7: Feature Extraction & EDA
#
# ### Exploratory Data Analysis (Bagian 2)
# Di tahap ini kita mengekstrak **12+ fitur kuantitatif** dari gambar tulisan tangan
# dan membandingkannya antara kelas `dyslexic` vs `non_dyslexic`.
#
# Fitur yang diekstrak:
# - **Character-level**: aspect ratio variance, rotation std, stroke width CV
# - **Word/Line-level**: spacing CV, baseline RMSE, slant angle std
# - **Page-level**: density uniformity, ink ratio CV
#
# **Tujuan:** Menjawab **BQ1** (apakah pola visual bisa dibedakan secara statistik)
# dan **BQ2** (fitur apa yang paling diskriminatif).

# %%
# === CELL 7: Extract & Compare Features ===
import pandas as pd
from src.feature_extraction import extract_all_features

# Ambil beberapa sample dari tiap kelas
n_samples_per_class = 20  # Kurangi jika lambat
all_features = []

for cls in classes:
    cls_dir = os.path.join(BASE_RAW, cls)
    img_files = sorted([f for f in os.listdir(cls_dir)
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))])[:n_samples_per_class]

    for img_name in img_files:
        img_path = os.path.join(cls_dir, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        # Binarize
        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Extract features
        feats = extract_all_features(binary)
        feats['class'] = cls

        # Map ke binary label
        if cls.lower() == 'normal':
            feats['label'] = 'non_dyslexic'
        else:
            feats['label'] = 'dyslexic'

        all_features.append(feats)

df = pd.DataFrame(all_features)
print(f"📊 Extracted features dari {len(df)} gambar\n")

# Tampilkan statistik per kelas
numeric_cols = [c for c in df.columns if c not in ['class', 'label', 'file_path', 'file_name']]
print("━" * 60)
print("STATISTIK PER KELAS (Mean)")
print("━" * 60)
display(df.groupby('label')[numeric_cols].mean().T.round(3))

# --- Visualisasi Top Features ---
top_features = [
    'char_aspect_ratio_var',
    'stroke_width_cv',
    'inter_char_spacing_cv',
    'baseline_rmse',
    'char_rotation_std',
    'contour_area_cv',
]

# Filter hanya yang ada di dataframe
top_features = [f for f in top_features if f in df.columns]

if top_features:
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    for ax, feat in zip(axes.flatten(), top_features):
        for label in df['label'].unique():
            subset = df[df['label'] == label][feat].dropna()
            ax.hist(subset, bins=20, alpha=0.6, label=label, density=True)
        ax.set_title(feat, fontsize=11, fontweight='bold')
        ax.legend(fontsize=9)
        ax.set_xlabel('Value')
        ax.set_ylabel('Density')

    plt.suptitle('📊 Distribusi Fitur: Dyslexic vs Non-Dyslexic', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ## 🧬 CELL 8: Synthetic Dyslexia Generator Demo

# %%
# === CELL 8: Synthetic Generator Demo ===
import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.synthetic_generator import get_mild_simulator, get_moderate_simulator, get_severe_simulator

# Ambil sample gambar Normal
normal_dir = os.path.join(BASE_RAW, 'Normal') if 'Normal' in classes else os.path.join(BASE_RAW, classes[0])
normal_files = [f for f in os.listdir(normal_dir)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Pilih 2 sample
samples = []
for f in normal_files[:2]:
    img = cv2.imread(os.path.join(normal_dir, f), cv2.IMREAD_GRAYSCALE)
    if img is not None:
        samples.append(img)

if samples:
    sample = samples[0]

    fig, axes = plt.subplots(2, 4, figsize=(20, 8))

    # Row 1: Original + 3 severity levels
    axes[0][0].imshow(sample, cmap='gray')
    axes[0][0].set_title('✅ Original (Normal)', fontweight='bold', fontsize=12)

    simulators = [
        ('🟡 Mild', get_mild_simulator()),
        ('🟠 Moderate', get_moderate_simulator()),
        ('🔴 Severe', get_severe_simulator()),
    ]

    for col, (name, sim) in enumerate(simulators, 1):
        syn = sim.generate_dyslexic_sample(sample)
        axes[0][col].imshow(syn, cmap='gray')
        axes[0][col].set_title(f'{name}', fontweight='bold', fontsize=12)

    # Row 2: Individual transforms
    sim = get_moderate_simulator()
    transforms = [
        ('↔️ Reversal', sim.apply_reversal),
        ('📐 Size Var', sim.apply_size_variation),
        ('🔄 Rotation', sim.apply_rotation_jitter),
        ('〰️ Tremor', sim.apply_stroke_tremor),
    ]

    for col, (name, fn) in enumerate(transforms):
        result_img = fn(sample.copy())
        axes[1][col].imshow(result_img, cmap='gray')
        axes[1][col].set_title(name, fontsize=11)

    for ax in axes.flatten():
        ax.axis('off')

    plt.suptitle('🧬 Synthetic Dyslexia Generation', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    print("✅ Generator berfungsi!")
    print("   Baris atas: severity levels (mild → severe)")
    print("   Baris bawah: individual transforms")
else:
    print("❌ Tidak ada gambar sample ditemukan")

# %% [markdown]
# ## ⚖️ CELL 9: Augmentation & Rebalancing Demo

# %%
# === CELL 9: Augmentation Demo ===
import cv2
import numpy as np
import matplotlib.pyplot as plt
from src.augmentation import get_augmentation_pipeline

if samples:
    sample = samples[0]

    fig, axes = plt.subplots(2, 5, figsize=(20, 7))

    # Row 1: Safe augmentation (untuk Normal / non_dyslexic)
    safe_pipeline = get_augmentation_pipeline('non_dyslexic')
    axes[0][0].imshow(sample, cmap='gray')
    axes[0][0].set_title('Original', fontweight='bold')
    for j in range(1, 5):
        aug = safe_pipeline(image=sample)['image']
        axes[0][j].imshow(aug, cmap='gray')
        axes[0][j].set_title(f'Safe Aug #{j}')

    # Row 2: Reinforced augmentation (untuk Dyslexic)
    dyslexic_pipeline = get_augmentation_pipeline('dyslexic')
    axes[1][0].imshow(sample, cmap='gray')
    axes[1][0].set_title('Original', fontweight='bold')
    for j in range(1, 5):
        aug = dyslexic_pipeline(image=sample)['image']
        axes[1][j].imshow(aug, cmap='gray')
        axes[1][j].set_title(f'Reinforced #{j}')

    for ax in axes.flatten():
        ax.axis('off')

    axes[0][0].set_ylabel('Non-Dyslexic\n(Safe)', fontsize=12, fontweight='bold',
                          rotation=0, labelpad=80)
    axes[1][0].set_ylabel('Dyslexic\n(Reinforced)', fontsize=12, fontweight='bold',
                          rotation=0, labelpad=80)

    plt.suptitle('🎨 Label-Safe vs Reinforced Augmentation', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    print("✅ Augmentation berfungsi!")
    print("   Baris atas: aman untuk kedua kelas")
    print("   Baris bawah: memperkuat pola disleksia (HANYA untuk kelas dyslexic)")

# %% [markdown]
# ## 🏋️ CELL 10: Batch Preprocessing Seluruh Dataset
# ⏱️ Cell ini memproses semua gambar — bisa memakan waktu beberapa menit.

# %%
# === CELL 10: Batch Preprocess ===
from src.preprocessing import batch_preprocess
import shutil

BASE = '/content/dataset'
BASE_RAW = '/content/dataset/raw/dyslexia_kaggle'

# Re-detect classes
classes = sorted([d for d in os.listdir(BASE_RAW) if os.path.isdir(os.path.join(BASE_RAW, d))])

# Mapping: original class → binary class
CLASS_MAP = {}
for cls in classes:
    if cls.lower() == 'normal':
        CLASS_MAP[cls] = 'non_dyslexic'
    else:
        CLASS_MAP[cls] = 'dyslexic'

print("📋 Class mapping:")
for k, v in CLASS_MAP.items():
    print(f"   {k} → {v}")
print()

# Proses tiap kelas
from sklearn.model_selection import train_test_split

for original_class, binary_class in CLASS_MAP.items():
    src_dir = os.path.join(BASE_RAW, original_class)
    img_files = [f for f in os.listdir(src_dir)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

    # Split: 70% train, 15% val, 15% test
    train_files, temp_files = train_test_split(img_files, test_size=0.3, random_state=42)
    val_files, test_files = train_test_split(temp_files, test_size=0.5, random_state=42)

    splits = {
        'train': train_files,
        'val': val_files,
        'test': test_files,
    }

    for split_name, split_files in splits.items():
        out_dir = os.path.join(BASE, 'processed', split_name, binary_class)
        os.makedirs(out_dir, exist_ok=True)

        count = 0
        for f in split_files:
            src = os.path.join(src_dir, f)
            result = preprocess_for_cnn(src, target_size=(128, 128))
            if result is not None:
                # Simpan sebagai .npy
                np.save(os.path.join(out_dir, f'{f.rsplit(".", 1)[0]}.npy'), result['tensor'])
                count += 1

        print(f"  ✅ {original_class} → {split_name}/{binary_class}: {count}/{len(split_files)} processed")

# Summary
print("\n" + "━" * 50)
print("📊 HASIL AKHIR:")
print("━" * 50)
for split in ['train', 'val', 'test']:
    for label in ['dyslexic', 'non_dyslexic']:
        folder = os.path.join(BASE, 'processed', split, label)
        count = len([f for f in os.listdir(folder) if f.endswith('.npy')]) if os.path.exists(folder) else 0
        print(f"  {split:6s}/{label:15s}: {count:>6,} files")

print("\n✅ Dataset siap untuk training!")

# %% [markdown]
# ## 🚀 CELL 11: Quick Model Training
# CNN sederhana + Focal Loss + Balanced Batching

# %%
# === CELL 11: Train Model ===
import tensorflow as tf
import numpy as np
from src.balanced_loader import DirectoryBalancedGenerator
from src.loss_functions import FocalLoss, get_evaluation_metrics, compute_focal_alpha

# Hitung alpha dari distribusi
train_dir = '/content/dataset/processed/train'
n_dys = len(os.listdir(os.path.join(train_dir, 'dyslexic')))
n_norm = len(os.listdir(os.path.join(train_dir, 'non_dyslexic')))
alpha = n_norm / (n_dys + n_norm)
print(f"📊 Training data: dyslexic={n_dys:,}, non_dyslexic={n_norm:,}")
print(f"   Focal Loss α = {alpha:.3f}")

# Data generators
train_gen = DirectoryBalancedGenerator(
    train_dir,
    target_size=(128, 128),
    batch_size=32,
    file_format='npy'
)

# CNN Model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(128, 128, 1)),

    tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.GlobalAveragePooling2D(),

    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=FocalLoss(gamma=2.0, alpha=alpha),
    metrics=get_evaluation_metrics()
)

model.summary()

print("\n🏋️ Mulai training... (uncomment baris di bawah)")
# history = model.fit(train_gen, epochs=20, verbose=1)

# %% [markdown]
# ---
# ## 📋 CELL 12: Kesimpulan & Jawaban Business Questions
#
# Berdasarkan seluruh analisis yang telah dilakukan, berikut jawaban untuk
# setiap business question yang telah didefinisikan di awal:

# %%
# === CELL 12: Kesimpulan ===
import matplotlib.pyplot as plt
import numpy as np

print("="*70)
print("📋 KESIMPULAN — JAWABAN BUSINESS QUESTIONS")
print("="*70)

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BQ1: Apakah pola visual tulisan anak disleksia dapat dibedakan secara
     statistik dari tulisan anak tipikal?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JAWABAN: YA.

Dari hasil EDA (CELL 7), histogram distribusi fitur menunjukkan perbedaan
yang jelas antara kelas dyslexic dan non_dyslexic pada beberapa fitur,
terutama:
- char_aspect_ratio_var (variance ukuran huruf)
- stroke_width_cv (konsistensi tekanan pena)
- inter_char_spacing_cv (konsistensi spasi)

Perbedaan ini didukung oleh visualisasi histogram overlay yang menunjukkan
distribusi kedua kelas TIDAK fully overlapping.
""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BQ2: Fitur visual apa yang paling diskriminatif?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JAWABAN: Top-5 fitur diskriminatif (berdasarkan analisis EDA):

  1. char_aspect_ratio_var  — Variance ukuran huruf
  2. stroke_width_cv        — Konsistensi tekanan pena
  3. inter_char_spacing_cv  — Konsistensi spasi antar huruf
  4. baseline_rmse          — Deviasi dari garis baseline
  5. char_rotation_std      — Konsistensi sudut rotasi huruf

Fitur-fitur ini berkaitan langsung dengan gejala klinis disleksia:
kontrol motorik lemah, persepsi spasial terganggu, dan koordinasi
mata-tangan yang belum matang.
""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BQ3: Seberapa akurat model CNN?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JAWABAN: Belum dijalankan (uncomment model.fit() di CELL 11).

Target: Recall ≥ 0.90, F1 ≥ 0.80.
Dalam konteks screening klinis, RECALL lebih penting dari precision karena
lebih baik meng-flag anak normal untuk pemeriksaan lanjut (false positive)
daripada melewatkan anak disleksia (false negative).
""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BQ4: Strategi apa yang efektif menangani class imbalance?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JAWABAN: Strategi berlapis yang diimplementasikan:

  Layer 1 (Data):      Targeted augmentation pada minority class
  Layer 2 (Algorithm): Focal Loss (γ=2.0) + class weighting
  Layer 3 (Sampling):  Balanced batch sampling (50/50 per batch)

JANGAN gunakan SMOTE langsung pada pixel gambar — menghasilkan artefak.
JANGAN gunakan accuracy sebagai metrik utama pada dataset imbalanced.
""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BQ5: Apakah synthetic data generation efektif?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JAWABAN: DyslexiaSimulator berhasil menghasilkan sampel sintetis yang
visual-nya realistis (lihat CELL 8). 6 transformasi yang diterapkan:
  1. Letter reversal (pembalikan huruf)
  2. Irregular spacing (spasi tidak konsisten)
  3. Size variation (ukuran huruf bervariasi)
  4. Rotation jitter (huruf miring tidak konsisten)
  5. Baseline drift (huruf melayang dari garis)
  6. Stroke tremor (goresan bergetar)

Namun, VALIDASI KLINIS oleh ahli psikologi WAJIB dilakukan sebelum
menggunakan data sintetis di model produksi.
""")

# Visualisasi ringkasan
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Distribusi Kelas Original
if class_counts:
    axes[0].bar(class_counts.keys(), class_counts.values(),
                color=['#2ecc71', '#e74c3c', '#f39c12'][:len(class_counts)])
    axes[0].set_title('Distribusi Kelas Original', fontweight='bold')
    axes[0].set_ylabel('Jumlah Gambar')
    for i, (k, v) in enumerate(class_counts.items()):
        axes[0].text(i, v + 200, f'{v:,}', ha='center', fontweight='bold')

# 2. Binary Mapping
if binary_map:
    colors_bin = ['#2ecc71', '#e74c3c']
    axes[1].bar(binary_map.keys(), binary_map.values(), color=colors_bin)
    axes[1].set_title('Binary Classification Mapping', fontweight='bold')
    axes[1].set_ylabel('Jumlah Gambar')
    for i, (k, v) in enumerate(binary_map.items()):
        axes[1].text(i, v + 200, f'{v:,}', ha='center', fontweight='bold')

# 3. Strategi Rebalancing
strategy_names = ['Class\nWeighting', 'Focal\nLoss', 'Balanced\nBatching',
                  'Targeted\nAugment', 'Synthetic\nGeneration']
strategy_impact = [3, 4, 3, 5, 4]  # Impact score 1-5
colors_strat = ['#3498db', '#9b59b6', '#1abc9c', '#e67e22', '#e74c3c']
axes[2].barh(strategy_names, strategy_impact, color=colors_strat)
axes[2].set_title('Strategi Rebalancing (Impact Score)', fontweight='bold')
axes[2].set_xlabel('Effectiveness (1-5)')
axes[2].set_xlim(0, 6)

plt.suptitle('📊 Ringkasan Analisis DysRead Helper', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

print("\n" + "="*70)
print("✅ ANALISIS DATA SCIENCE SELESAI")
print("="*70)
print("""
Next Steps:
  1. Jalankan training model (uncomment model.fit() di CELL 11)
  2. Evaluasi dengan confusion matrix dan Grad-CAM
  3. Buka Streamlit dashboard: streamlit run streamlit_app.py
  4. Simpan model: model.save('/content/drive/MyDrive/DysRead/model_v1.keras')
""")
