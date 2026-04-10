# DysRead Helper — Dataset Preparation & Preprocessing Pipeline

## 📋 Overview

Pipeline data untuk proyek DysRead Helper: early screening disleksia pada anak melalui 
analisis citra tulisan tangan menggunakan pendekatan Vision-based (CNN).

**Pendekatan:** Deteksi pola kognitif visual, BUKAN OCR.

## 📁 Project Structure

```
dataset/
├── raw/                          # Data mentah (belum diproses)
│   ├── dyslexia_kaggle/         # Dyslexia Handwriting Dataset
│   ├── iam_database/            # IAM Handwriting Database
│   ├── az_handwritten/          # Kaggle A-Z Glyphs
│   └── synthetic_generated/     # Output synthetic engine
├── processed/                    # Data siap training
│   ├── train/
│   │   ├── dyslexic/
│   │   └── non_dyslexic/
│   ├── val/
│   │   ├── dyslexic/
│   │   └── non_dyslexic/
│   └── test/
│       ├── dyslexic/
│       └── non_dyslexic/
├── metadata/
├── src/                         # Source code pipeline
│   ├── preprocessing.py         # 7-step preprocessing pipeline
│   ├── feature_extraction.py    # 12+ visual features for EDA
│   ├── synthetic_generator.py   # Dyslexia pattern simulation
│   ├── augmentation.py          # Label-safe augmentation
│   ├── rebalancing.py           # Class balancing utilities
│   ├── balanced_loader.py       # Balanced batch generators
│   └── loss_functions.py        # Focal Loss & class weighting
├── notebooks/                   # Jupyter notebooks (EDA, etc)
├── reports/
├── configs/
│   └── preprocessing_config.yaml
├── data_card.md                 # Dataset documentation
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### ☁️ Google Colab (Recommended)

Cara termudah — tidak perlu install apapun di komputer lokal:

**Step 1:** Upload folder `src/` ke Google Drive (misal: `My Drive/DysRead/dataset/src/`)

**Step 2:** Buat Colab notebook baru, paste cell ini:

```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Install dependencies
!pip install -q opencv-python-headless scikit-image scipy albumentations PyYAML tqdm

# Set path ke project
import sys
sys.path.insert(0, '/content/drive/MyDrive/DysRead/dataset')

# Test import
from src.preprocessing import preprocess_for_cnn
from src.feature_extraction import extract_all_features
from src.synthetic_generator import DyslexiaSimulator
from src.augmentation import get_augmentation_pipeline
from src.loss_functions import FocalLoss, get_evaluation_metrics
print("✅ All modules ready!")
```

**Step 3:** Gunakan modul seperti biasa (lihat contoh di bawah)

> 📝 Lihat `colab_setup.py` untuk panduan lengkap cell-by-cell termasuk download dataset Kaggle dan training model.

---

### 💻 Lokal

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Preprocess Single Image

```bash
python src/preprocessing.py path/to/image.png
```

### 3. Batch Preprocessing

```python
from src.preprocessing import batch_preprocess

stats = batch_preprocess(
    input_dir='raw/dyslexia_kaggle/',
    output_dir='processed/train/dyslexic/',
    target_size=(128, 128),
    binarize_method='otsu'
)
```

### 4. Extract Features for EDA

```python
from src.feature_extraction import extract_all_features
import cv2

img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
features = extract_all_features(binary)
```

### 5. Generate Synthetic Data

```python
from src.synthetic_generator import DyslexiaSimulator

sim = DyslexiaSimulator(reversal_prob=0.3, tremor_intensity=0.15)
dyslexic_img = sim.generate_dyslexic_sample(normal_img)
```

### 6. Train with Balanced Loading

```python
from src.balanced_loader import DirectoryBalancedGenerator
from src.loss_functions import FocalLoss, get_evaluation_metrics

train_gen = DirectoryBalancedGenerator('processed/train/', batch_size=32)

model.compile(
    optimizer='adam',
    loss=FocalLoss(gamma=2.0, alpha=0.75),
    metrics=get_evaluation_metrics()
)

model.fit(train_gen, epochs=50)
```

## 📊 Pipeline Modules

| Module | Purpose |
|--------|---------|
| `preprocessing.py` | Raw image → CNN-ready tensor (128×128×1) |
| `feature_extraction.py` | 12+ quantitative visual features for EDA |
| `synthetic_generator.py` | Simulate dyslexia patterns on normal handwriting |
| `augmentation.py` | Label-safe + label-reinforcing augmentation |
| `rebalancing.py` | Dataset rebalancing (targeted augmentation) |
| `balanced_loader.py` | 50/50 balanced batch generators for Keras |
| `loss_functions.py` | Focal Loss, Weighted BCE, evaluation metrics |

## ⚠️ Important Notes

1. **TIDAK menggunakan OCR** — Pendekatan ini mendeteksi pola visual, bukan membaca teks
2. **Horizontal flip DILARANG** untuk kelas Normal — bisa mengubah label menjadi Reversal
3. **Skeleton JANGAN digunakan sebagai CNN input** — hanya untuk feature extraction/EDA
4. **Recall > Precision** — Untuk screening klinis, lebih baik false positive daripada false negative
5. **Target Recall ≥ 0.90**

## 📄 License

Dataset ini menggunakan kombinasi sumber dengan lisensi berbeda. 
Lihat `data_card.md` untuk detail per sumber.
