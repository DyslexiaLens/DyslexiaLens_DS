import json

cells = []

def md(src): cells.append({"cell_type":"markdown","metadata":{},"source":src})
def code(src): cells.append({"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":src})

# ========== HEADER ==========
md(["# \U0001f9e0 DyslexiaLens — Dataset Dengan Augmentasi EMNIST\n",
    "\n",
    "Notebook ini merupakan versi **augmented** dari `Dyslexia_NoAugmentation.ipynb`.\n",
    "Dataset Gambo asli diperkaya dengan data EMNIST untuk menyeimbangkan kelas Normal vs Disleksia.\n",
    "\n",
    "**Sumber data:** `Dataset/Gambo_EMNIST/` (Gambo + EMNIST ByClass)\n"])

# ========== IMPORTS ==========
code(["import pandas as pd\n","import numpy as np\n","import matplotlib.pyplot as plt\n",
      "import matplotlib.image as mpimg\n","import seaborn as sns\n","import os, re, warnings\n",
      "from PIL import Image\n","from collections import defaultdict\n",
      "warnings.filterwarnings('ignore')\n","sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)\n",
      "\n","BASE = 'Dataset/Gambo_EMNIST'\n",
      "CSV_OUTPUT = 'master_dataset_emnist.csv'\n",
      "CSV_FINAL = 'master_dataset_emnist_final.csv'"])

# ========== TAHAP 3: MASTER CSV ==========
md(["---\n","# Tahap 3: Pembuatan Master CSV\n","\n",
    "Membangun `master_dataset_emnist.csv` dari struktur folder `Gambo_EMNIST`."])

code(["rows = []\n",
      "for split in ['Train', 'Test']:\n",
      "    for category in ['Normal', 'Corrected', 'Reversal']:\n",
      "        folder = os.path.join(BASE, split, category)\n",
      "        if not os.path.exists(folder):\n",
      "            continue\n",
      "        for fname in os.listdir(folder):\n",
      "            if not fname.endswith('.png'):\n",
      "                continue\n",
      "            img_path = os.path.join('Dataset', 'Gambo_EMNIST', split, category, fname)\n",
      "            target = 0 if category == 'Normal' else 1\n",
      "            # Severity from filename prefix\n",
      "            prefix = fname.split('_')[0] if '_' in fname else fname.split('-')[0]\n",
      "            try:\n",
      "                score = int(prefix) if prefix.isdigit() else 0\n",
      "            except:\n",
      "                score = 0\n",
      "            rows.append({\n",
      "                'image_path': img_path,\n",
      "                'file_name': fname,\n",
      "                'split': split,\n",
      "                'folder_category': category,\n",
      "                'severity_score': score,\n",
      "                'target_class': target\n",
      "            })\n",
      "\n",
      "df = pd.DataFrame(rows)\n",
      "df.to_csv(CSV_OUTPUT, index=False)\n",
      "print(f'Master CSV: {len(df):,} baris')\n",
      "print(f'Kolom: {list(df.columns)}')\n",
      "print(f'\\nDistribusi Split:')\n",
      "print(df['split'].value_counts())\n",
      "print(f'\\nDistribusi Kelas:')\n",
      "print(df['target_class'].value_counts().rename({0:\"Normal\",1:\"Disleksia\"}))"])

# ========== TAHAP 4: EDA ==========
md(["---\n","# Tahap 4: Exploratory Data Analysis (EDA)\n","\n",
    "### Pertanyaan Bisnis\n",
    "> *Dapatkah pola goresan tulisan tangan digunakan sebagai indikator awal disleksia?*\n",
    "> *Seberapa efektif penambahan data EMNIST untuk menyeimbangkan kelas?*"])

# 4A: Distribusi kelas per split
md(["### 4A. Distribusi Kelas per Split"])
code(["fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
      "\n","for idx, split in enumerate(['Train', 'Test']):\n",
      "    subset = df[df['split'] == split]\n",
      "    counts = subset['folder_category'].value_counts()\n",
      "    colors = {'Normal':'#2ecc71','Corrected':'#e74c3c','Reversal':'#9b59b6'}\n",
      "    bars = counts.plot(kind='bar', ax=axes[idx],\n",
      "                       color=[colors.get(c,'#95a5a6') for c in counts.index])\n",
      "    axes[idx].set_title(f'Distribusi Kelas - {split}', fontweight='bold')\n",
      "    axes[idx].set_ylabel('Jumlah Gambar')\n",
      "    axes[idx].tick_params(axis='x', rotation=0)\n",
      "    for bar in bars.patches:\n",
      "        axes[idx].text(bar.get_x()+bar.get_width()/2, bar.get_height()+200,\n",
      "                       f'{int(bar.get_height()):,}', ha='center', fontweight='bold', fontsize=9)\n",
      "\n","plt.suptitle('Distribusi Kelas per Split (Gambo + EMNIST)', fontsize=14, fontweight='bold')\n",
      "plt.tight_layout()\n","plt.savefig('../assets/class_distribution_emnist.png', dpi=150, bbox_inches='tight')\n",
      "plt.show()"])

# 4B: Distribusi severity
md(["### 4B. Distribusi Severity Score"])
code(["fig, ax = plt.subplots(figsize=(10, 5))\n",
      "sev = df['severity_score'].value_counts().sort_index()\n",
      "colors_sev = ['#2ecc71'] + [plt.cm.YlOrRd(i/6) for i in range(1,7)]\n",
      "sev.plot(kind='bar', ax=ax, color=colors_sev[:len(sev)])\n",
      "ax.set_title('Distribusi Severity Score', fontweight='bold', fontsize=14)\n",
      "ax.set_xlabel('Severity Score')\n","ax.set_ylabel('Jumlah Gambar')\n",
      "ax.tick_params(axis='x', rotation=0)\n",
      "for bar in ax.patches:\n",
      "    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+100,\n",
      "            f'{int(bar.get_height()):,}', ha='center', fontweight='bold', fontsize=9)\n",
      "plt.tight_layout()\n","plt.savefig('../assets/severity_distribution_emnist.png', dpi=150, bbox_inches='tight')\n",
      "plt.show()"])

# 4C: Sampel visual per kelas
md(["### 4C. Sampel Visual: Normal vs Corrected vs Reversal"])
code(["fig, axes = plt.subplots(3, 5, figsize=(14, 9))\n",
      "categories = ['Normal', 'Corrected', 'Reversal']\n",
      "\n","for row, cat in enumerate(categories):\n",
      "    subset = df[(df['folder_category'] == cat) & (df['split'] == 'Train')]\n",
      "    samples = subset.sample(min(5, len(subset)), random_state=42)\n",
      "    for col, (_, sample) in enumerate(samples.iterrows()):\n",
      "        img_path = os.path.join('..', sample['image_path']) if not os.path.exists(sample['image_path']) else sample['image_path']\n",
      "        try:\n",
      "            img = Image.open(img_path).convert('L').resize((28,28))\n",
      "            axes[row][col].imshow(np.array(img), cmap='gray')\n",
      "        except:\n",
      "            axes[row][col].text(0.5,0.5,'N/A',ha='center',va='center')\n",
      "        axes[row][col].set_title(f'{cat}', fontsize=9)\n",
      "        axes[row][col].axis('off')\n",
      "\n","plt.suptitle('Sampel Visual per Kelas (Train)', fontsize=14, fontweight='bold')\n",
      "plt.tight_layout()\n","plt.savefig('../assets/class_samples_emnist.png', dpi=150, bbox_inches='tight')\n",
      "plt.show()"])

# 4D: Sampel severity
md(["### 4D. Sampel Visual per Severity Score"])
code(["scores = sorted(df[df['severity_score']>0]['severity_score'].unique())\n",
      "n_scores = len(scores)\n",
      "if n_scores > 0:\n",
      "    fig, axes = plt.subplots(n_scores, 5, figsize=(14, 3*n_scores))\n",
      "    if n_scores == 1: axes = [axes]\n",
      "    for row, score in enumerate(scores):\n",
      "        subset = df[df['severity_score'] == score]\n",
      "        samples = subset.sample(min(5, len(subset)), random_state=42)\n",
      "        for col, (_, s) in enumerate(samples.iterrows()):\n",
      "            img_path = os.path.join('..', s['image_path']) if not os.path.exists(s['image_path']) else s['image_path']\n",
      "            try:\n",
      "                img = Image.open(img_path).convert('L').resize((28,28))\n",
      "                axes[row][col].imshow(np.array(img), cmap='gray')\n",
      "            except:\n",
      "                axes[row][col].text(0.5,0.5,'N/A',ha='center',va='center')\n",
      "            axes[row][col].set_title(f'Skor {score}', fontsize=9)\n",
      "            axes[row][col].axis('off')\n",
      "    plt.suptitle('Sampel Visual per Severity Score', fontsize=14, fontweight='bold')\n",
      "    plt.tight_layout()\n",
      "    plt.savefig('../assets/severity_samples_emnist.png', dpi=150, bbox_inches='tight')\n",
      "    plt.show()"])

# 4E: Heatmap
md(["### 4E. Heatmap Rata-rata Piksel (Skor Terendah vs Tertinggi)"])
code(["def compute_mean_image(subset, n=500):\n",
      "    samples = subset.sample(min(n, len(subset)), random_state=42)\n",
      "    arrays = []\n",
      "    for _, row in samples.iterrows():\n",
      "        p = row['image_path']\n",
      "        if not os.path.exists(p): p = os.path.join('..', p)\n",
      "        try:\n",
      "            img = Image.open(p).convert('L').resize((28,28))\n",
      "            arrays.append(np.array(img, dtype=np.float32))\n",
      "        except: continue\n",
      "    return np.mean(arrays, axis=0) if arrays else np.zeros((28,28))\n",
      "\n",
      "dys = df[df['severity_score'] > 0]\n",
      "if len(dys) > 0:\n",
      "    min_s = dys['severity_score'].min()\n",
      "    max_s = dys['severity_score'].max()\n",
      "    mean_low = compute_mean_image(dys[dys['severity_score']==min_s])\n",
      "    mean_high = compute_mean_image(dys[dys['severity_score']==max_s])\n",
      "    diff = np.abs(mean_high - mean_low)\n",
      "\n",
      "    fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n",
      "    axes[0].imshow(mean_low, cmap='gray'); axes[0].set_title(f'Skor {min_s} (Ringan)')\n",
      "    axes[1].imshow(mean_high, cmap='gray'); axes[1].set_title(f'Skor {max_s} (Parah)')\n",
      "    im = axes[2].imshow(diff, cmap='hot'); axes[2].set_title('Selisih Intensitas')\n",
      "    plt.colorbar(im, ax=axes[2])\n",
      "    for ax in axes: ax.axis('off')\n",
      "    plt.suptitle(f'Heatmap: Skor {min_s} vs Skor {max_s}', fontsize=14, fontweight='bold')\n",
      "    plt.tight_layout()\n",
      "    plt.savefig('../assets/heatmap_emnist.png', dpi=150, bbox_inches='tight')\n",
      "    plt.show()\n",
      "    print(f'Rata-rata selisih intensitas: {np.mean(diff):.2f}')"])

# 4F: Keseimbangan kelas (EMNIST impact)
md(["### 4F. Analisis Keseimbangan Kelas (Impact EMNIST)\n","\n",
    "Visualisasi perbandingan rasio kelas sebelum dan sesudah penambahan EMNIST."])
code(["normal_count = len(df[df['target_class']==0])\n",
      "dys_count = len(df[df['target_class']==1])\n",
      "\n","fig, ax = plt.subplots(figsize=(8, 5))\n",
      "bars = ax.bar(['Normal (0)', 'Disleksia (1)'], [normal_count, dys_count],\n",
      "              color=['#2ecc71', '#e74c3c'], edgecolor='white', linewidth=2)\n",
      "for bar in bars:\n",
      "    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+500,\n",
      "            f'{int(bar.get_height()):,}', ha='center', fontweight='bold', fontsize=12)\n",
      "ax.set_title('Keseimbangan Kelas: Normal vs Disleksia (Gambo + EMNIST)', fontweight='bold')\n",
      "ax.set_ylabel('Jumlah Gambar')\n",
      "ratio = dys_count/normal_count if normal_count > 0 else 0\n",
      "ax.axhline(y=normal_count, color='gray', linestyle='--', alpha=0.5)\n",
      "plt.tight_layout()\n","plt.show()\n",
      "print(f'Normal: {normal_count:,} | Disleksia: {dys_count:,} | Rasio 1:{ratio:.2f}')"])

# 4G: Karakter paling sering
md(["### 4G. Karakter Paling Sering Muncul"])
code(["chars = df['file_name'].str.extract(r'([a-zA-Z])')[0].str.lower()\n",
      "char_counts = chars.value_counts().head(20)\n",
      "\n","fig, ax = plt.subplots(figsize=(12, 4))\n",
      "char_counts.plot(kind='bar', color='#9b59b6', ax=ax)\n",
      "ax.set_title('Top 20 Karakter Terbanyak dalam Dataset', fontweight='bold')\n",
      "ax.set_ylabel('Jumlah Kemunculan')\n","ax.set_xlabel('Karakter')\n",
      "ax.tick_params(axis='x', rotation=0)\n","plt.tight_layout()\n","plt.show()"])

# ========== TAHAP 5: STRATIFIED SPLIT ==========
md(["---\n","# Tahap 5: Stratified Splitting\n","\n",
    "Membuat split Train/Validation/Test yang stratified."])

md(["### 5A. Stratified Split (Train -> Train + Validation)"])
code(["from sklearn.model_selection import train_test_split\n",
      "\n","train_df = df[df['split'] == 'Train'].copy()\n",
      "test_df = df[df['split'] == 'Test'].copy()\n",
      "\n","# Split Train -> 80% Train + 20% Validation\n",
      "train_final, val_final = train_test_split(\n",
      "    train_df, test_size=0.2, random_state=42,\n",
      "    stratify=train_df['target_class']\n",")\n",
      "\n","train_final = train_final.copy()\n","val_final = val_final.copy()\n",
      "test_final = test_df.copy()\n",
      "\n","train_final['split'] = 'Train'\n","val_final['split'] = 'Validation'\n",
      "test_final['split'] = 'Test'\n",
      "\n","df_final = pd.concat([train_final, val_final, test_final], ignore_index=True)\n",
      "df_final.to_csv(CSV_FINAL, index=False)\n",
      "\n","print(f'Total: {len(df_final):,}')\n",
      "for s in ['Train','Validation','Test']:\n",
      "    n = len(df_final[df_final[\"split\"]==s])\n",
      "    print(f'  {s:12s}: {n:>8,} ({n/len(df_final)*100:.1f}%)')"])

# 5B: Class weights
md(["### 5B. Class Weights untuk AI Engineer"])
code(["from sklearn.utils.class_weight import compute_class_weight\n",
      "\n","binary_classes = np.array([0, 1])\n",
      "binary_weights = compute_class_weight('balanced', classes=binary_classes, y=train_final['target_class'].values)\n",
      "binary_weight_dict = dict(zip(binary_classes.astype(int), binary_weights))\n",
      "\n","print('=== CLASS WEIGHTS ===')\n",
      "for cls, w in binary_weight_dict.items():\n",
      "    label = 'Normal' if cls == 0 else 'Disleksia'\n",
      "    print(f'  Kelas {cls} ({label}): {w:.4f}')"])

# 5C: Visual split
md(["### 5C. Validasi Visual Distribusi Split"])
code(["fig = plt.figure(figsize=(16, 5))\n",
      "\n","ax1 = fig.add_subplot(1, 3, 1)\n",
      "split_sizes = df_final['split'].value_counts().reindex(['Train','Validation','Test'])\n",
      "ax1.pie(split_sizes, labels=[f'{s}\\n({v:,})' for s,v in split_sizes.items()],\n",
      "        colors=['#3498db','#f39c12','#2ecc71'], autopct='%1.1f%%', startangle=90,\n",
      "        textprops={'fontsize':10,'fontweight':'bold'}, wedgeprops={'edgecolor':'white','linewidth':2})\n",
      "ax1.set_title('Proporsi Split', fontweight='bold')\n",
      "\n","ax2 = fig.add_subplot(1, 3, 2)\n",
      "bd = df_final.groupby(['split','target_class']).size().unstack(fill_value=0)\n",
      "bd = bd.reindex(['Train','Validation','Test'])\n",
      "bd.columns = ['Normal','Disleksia']\n",
      "bd.plot(kind='bar', ax=ax2, color=['#2ecc71','#e74c3c'], edgecolor='white')\n",
      "ax2.set_title('Binary Class per Split', fontweight='bold')\n",
      "ax2.set_ylabel('Jumlah')\n","ax2.tick_params(axis='x', rotation=0)\n",
      "\n","ax3 = fig.add_subplot(1, 3, 3)\n",
      "for split in ['Train','Validation','Test']:\n",
      "    sub = df_final[df_final['split']==split]\n",
      "    props = sub['target_class'].value_counts(normalize=True).sort_index()\n",
      "    ax3.bar([f'{split}\\nNormal', f'{split}\\nDyslexia'],\n",
      "            props.values, color=['#2ecc71','#e74c3c'], alpha=0.7)\n",
      "ax3.set_title('Proporsi Kelas per Split', fontweight='bold')\n",
      "ax3.set_ylabel('Proporsi')\n",
      "\n","plt.tight_layout()\n","plt.show()"])

# ========== TAHAP 6: KESIAPAN DATA ==========
md(["---\n","# Tahap 6: Kesiapan Data untuk Pemodelan"])

md(["### 6A. Data Dictionary\n","\n",
    "| Kolom | Tipe | Deskripsi | Nilai |\n",
    "|---|---|---|---|\n",
    "| `image_path` | String | Path relatif ke file gambar | `Dataset/Gambo_EMNIST/Train/Normal/A-1.png` |\n",
    "| `file_name` | String | Nama file gambar | `A-1.png` |\n",
    "| `split` | String | Pembagian dataset | `Train`, `Validation`, `Test` |\n",
    "| `folder_category` | String | Kategori kelas asal | `Normal`, `Corrected`, `Reversal` |\n",
    "| `severity_score` | Integer | Skor keparahan | `0`=Normal, `1`-`6`=Ringan-Parah |\n",
    "| `target_class` | Integer | Label biner | `0`=Normal, `1`=Disleksia |\n",
    "\n","### Aturan untuk AI Engineer\n",
    "| Aturan | Penjelasan |\n","|---|---|\n",
    "| **Input model** | Hanya `image_path` (baca piksel gambar) |\n",
    "| **Output utama** | `target_class` (klasifikasi biner) |\n",
    "| **JANGAN sebagai fitur** | `severity_score`, `folder_category`, `file_name` |\n",
    "| **Horizontal Flip** | DILARANG |\n"])

# 6B: Validasi akhir
md(["### 6B. Validasi Akhir"])
code(["df_check = pd.read_csv(CSV_FINAL)\n",
      "print(f'Total baris: {len(df_check):,}')\n",
      "print(f'Kolom: {list(df_check.columns)}')\n",
      "\n","total = len(df_check)\n",
      "print(f'\\n=== PROPORSI SPLIT ===')\n",
      "for split in ['Train','Validation','Test']:\n",
      "    n = len(df_check[df_check['split']==split])\n",
      "    print(f'{split:12s}: {n:>8,} ({n/total*100:.1f}%)')\n",
      "\n","val_p = set(df_check[df_check['split']=='Validation']['image_path'])\n",
      "train_p = set(df_check[df_check['split']=='Train']['image_path'])\n",
      "test_p = set(df_check[df_check['split']=='Test']['image_path'])\n",
      "\n","print(f'\\n=== CEK DATA LEAKAGE ===')\n",
      "print(f'Train & Validation: {len(train_p & val_p)}')\n",
      "print(f'Train & Test:       {len(train_p & test_p)}')\n",
      "print(f'Validation & Test:  {len(val_p & test_p)}')\n",
      "\n","if len(train_p&val_p)==0 and len(train_p&test_p)==0:\n",
      "    print('\\nAMAN - Nol data leakage.')\n","else:\n",
      "    print('\\nPERINGATAN - Ada overlap!')\n",
      "\n","print(f'\\nDataset siap untuk handover ke AI Engineer.')"])

# 6C: Kesimpulan
md(["### Kesimpulan Pipeline\n","\n",
    "| Tahap | Output | Status |\n","|---|---|---|\n",
    "| 3. Master CSV | `master_dataset_emnist.csv` | Done |\n",
    "| 4. EDA | Visualisasi distribusi, heatmap, sampel | Done |\n",
    "| 5. Stratified Split | Train/Validation/Test | Done |\n",
    "| 6. Kesiapan Data | Data Dictionary + class weights | Done |\n",
    "\n","**File output:** `master_dataset_emnist_final.csv`\n"])

nb = {"nbformat":4,"nbformat_minor":5,
      "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                  "language_info":{"name":"python","version":"3.10.0"}},
      "cells":cells}

with open('notebooks/Dyslexia_EMNIST.ipynb','w',encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print('Notebook berhasil dibuat: notebooks/Dyslexia_EMNIST.ipynb')
print(f'Total cells: {len(cells)}')
