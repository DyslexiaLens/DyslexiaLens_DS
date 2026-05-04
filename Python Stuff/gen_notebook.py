import json

nb = {
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.10.0"}
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Ekstraksi EMNIST ByClass (Test) ke Gambo_EMNIST\n",
    "\n",
    "Notebook ini mengekstrak gambar huruf dari `emnist-byclass-test.csv` lalu menyalinnya ke folder\n",
    "`Gambo_EMNIST/Train/Normal` dan `Gambo_EMNIST/Test/Normal` dengan:\n",
    "\n",
    "- **Hanya alfabet** (A-Z, a-z) — digit 0-9 dibuang\n",
    "- **Split 80:20** per huruf (Train:Test) untuk mencegah data leakage\n",
    "- **Penamaan** melanjutkan index terakhir yang sudah ada di folder tujuan\n",
    "- **Format nama file:** `{Huruf}-{index}.png`\n",
    "- **Seed acak tetap** (42) agar reprodusibel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from PIL import Image\n",
    "import os\n",
    "import re\n",
    "import random\n",
    "from collections import defaultdict\n",
    "\n",
    "random.seed(42)\n",
    "np.random.seed(42)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 1. Load Mapping Label (ASCII)"]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "mapping_path = 'Dataset/emnist-byclass-mapping.txt'\n",
    "df_mapping = pd.read_csv(mapping_path, sep=' ', header=None, names=['label', 'ascii_code'])\n",
    "\n",
    "label_to_ascii = dict(zip(df_mapping['label'], df_mapping['ascii_code']))\n",
    "label_to_char = {k: chr(v) for k, v in label_to_ascii.items()}\n",
    "\n",
    "# Filter: hanya alfabet (label 10-61, ASCII 65-90 dan 97-122)\n",
    "alpha_labels = {k: v for k, v in label_to_char.items() if v.isalpha()}\n",
    "\n",
    "print(f'Total kelas dalam mapping: {len(label_to_char)}')\n",
    "print(f'Kelas alfabet saja: {len(alpha_labels)}')\n",
    "print(f'Kelas digit (dibuang): {len(label_to_char) - len(alpha_labels)}')\n",
    "print()\n",
    "print('Contoh mapping alfabet:')\n",
    "for k, v in list(alpha_labels.items())[:5]:\n",
    "    print(f'  Label {k} -> \"{v}\"')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Load CSV EMNIST ByClass (Test Only)\n",
    "\n",
    "Kita hanya menggunakan `emnist-byclass-test.csv` (~116k gambar).\n",
    "File `train.csv` terlalu besar dan tidak diperlukan."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "csv_path = 'Dataset/emnist-byclass-test.csv'\n",
    "\n",
    "print(f'Loading {csv_path}...')\n",
    "df = pd.read_csv(csv_path, header=None, dtype=np.uint8)\n",
    "print(f'Shape: {df.shape}  ({df.shape[0]:,} gambar, {df.shape[1]} kolom)')\n",
    "\n",
    "# Kolom 0 = label, kolom 1-784 = piksel\n",
    "labels = df.iloc[:, 0].values\n",
    "pixels = df.iloc[:, 1:].values\n",
    "\n",
    "del df\n",
    "print('DataFrame dihapus dari RAM.')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 3. Filter Hanya Alfabet (Buang Digit 0-9)"]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "alpha_label_set = set(alpha_labels.keys())\n",
    "mask = np.isin(labels, list(alpha_label_set))\n",
    "\n",
    "alpha_labels_arr = labels[mask]\n",
    "alpha_pixels = pixels[mask]\n",
    "\n",
    "print(f'Total gambar sebelum filter: {len(labels):,}')\n",
    "print(f'Total gambar setelah filter (alfabet saja): {len(alpha_labels_arr):,}')\n",
    "print(f'Gambar digit yang dibuang: {len(labels) - len(alpha_labels_arr):,}')\n",
    "\n",
    "# Bebaskan memori\n",
    "del labels, pixels, mask"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 4. Visualisasi Sample (Verifikasi Orientasi)"]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "fig, axes = plt.subplots(2, 5, figsize=(12, 5))\n",
    "fig.suptitle('Sample Alfabet dari EMNIST ByClass Test', fontsize=14)\n",
    "\n",
    "indices = np.random.choice(len(alpha_labels_arr), 10, replace=False)\n",
    "for i, ax in enumerate(axes.flatten()):\n",
    "    idx = indices[i]\n",
    "    # EMNIST: perlu transpose karena column-major\n",
    "    img = alpha_pixels[idx].reshape(28, 28).T\n",
    "    ax.imshow(img, cmap='gray')\n",
    "    char = label_to_char[int(alpha_labels_arr[idx])]\n",
    "    ax.set_title(f'\"{char}\"')\n",
    "    ax.axis('off')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Konfigurasi Path & Scan Index Terakhir\n",
    "\n",
    "Memindai file yang sudah ada di `Gambo_EMNIST` untuk menentukan index awal penamaan."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "BASE = 'Dataset'\n",
    "TRAIN_DST = os.path.join(BASE, 'Gambo_EMNIST', 'Train', 'Normal')\n",
    "TEST_DST = os.path.join(BASE, 'Gambo_EMNIST', 'Test', 'Normal')\n",
    "SPLIT_RATIO = 0.8\n",
    "\n",
    "def get_max_index_per_letter(folder):\n",
    "    max_idx = defaultdict(int)\n",
    "    if not os.path.exists(folder):\n",
    "        return max_idx\n",
    "    for f in os.listdir(folder):\n",
    "        m = re.match(r'^([A-Za-z])[-_](\\d+)\\.png$', f)\n",
    "        if m:\n",
    "            letter = m.group(1)\n",
    "            idx = int(m.group(2))\n",
    "            if idx > max_idx[letter]:\n",
    "                max_idx[letter] = idx\n",
    "    return max_idx\n",
    "\n",
    "train_max = get_max_index_per_letter(TRAIN_DST)\n",
    "test_max = get_max_index_per_letter(TEST_DST)\n",
    "\n",
    "before_train = len(os.listdir(TRAIN_DST)) if os.path.exists(TRAIN_DST) else 0\n",
    "before_test = len(os.listdir(TEST_DST)) if os.path.exists(TEST_DST) else 0\n",
    "\n",
    "print(f'Train/Normal saat ini: {before_train:,} file')\n",
    "print(f'Test/Normal saat ini:  {before_test:,} file')\n",
    "print(f'Huruf terlacak di Train: {len(train_max)}')\n",
    "print(f'Huruf terlacak di Test:  {len(test_max)}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Ekstrak & Simpan ke Gambo_EMNIST\n",
    "\n",
    "Untuk setiap huruf:\n",
    "1. Kumpulkan semua piksel gambar huruf tersebut\n",
    "2. Shuffle secara deterministik\n",
    "3. Split 80% Train / 20% Test\n",
    "4. Reshape 28x28, transpose, simpan sebagai PNG\n",
    "5. Penamaan melanjutkan index terakhir"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "os.makedirs(TRAIN_DST, exist_ok=True)\n",
    "os.makedirs(TEST_DST, exist_ok=True)\n",
    "\n",
    "total_train = 0\n",
    "total_test = 0\n",
    "\n",
    "# Proses per huruf\n",
    "unique_labels = sorted(set(alpha_labels_arr))\n",
    "\n",
    "for label_id in unique_labels:\n",
    "    char = label_to_char[int(label_id)]\n",
    "    \n",
    "    # Ambil semua gambar untuk huruf ini\n",
    "    mask = alpha_labels_arr == label_id\n",
    "    char_pixels = alpha_pixels[mask]\n",
    "    \n",
    "    # Shuffle indices\n",
    "    indices = list(range(len(char_pixels)))\n",
    "    random.shuffle(indices)\n",
    "    \n",
    "    # Split 80:20\n",
    "    split_idx = int(len(indices) * SPLIT_RATIO)\n",
    "    train_indices = indices[:split_idx]\n",
    "    test_indices = indices[split_idx:]\n",
    "    \n",
    "    # Index awal\n",
    "    train_start = train_max.get(char, 0) + 1\n",
    "    test_start = test_max.get(char, 0) + 1\n",
    "    \n",
    "    # Simpan Train\n",
    "    for i, idx in enumerate(train_indices):\n",
    "        img = char_pixels[idx].reshape(28, 28).T\n",
    "        img_pil = Image.fromarray(img, mode='L')\n",
    "        fname = f'{char}-{train_start + i}.png'\n",
    "        img_pil.save(os.path.join(TRAIN_DST, fname))\n",
    "    \n",
    "    if train_indices:\n",
    "        train_max[char] = train_start + len(train_indices) - 1\n",
    "    \n",
    "    # Simpan Test\n",
    "    for i, idx in enumerate(test_indices):\n",
    "        img = char_pixels[idx].reshape(28, 28).T\n",
    "        img_pil = Image.fromarray(img, mode='L')\n",
    "        fname = f'{char}-{test_start + i}.png'\n",
    "        img_pil.save(os.path.join(TEST_DST, fname))\n",
    "    \n",
    "    if test_indices:\n",
    "        test_max[char] = test_start + len(test_indices) - 1\n",
    "    \n",
    "    total_train += len(train_indices)\n",
    "    total_test += len(test_indices)\n",
    "    \n",
    "    print(\n",
    "        f'  \"{char}\": {len(char_pixels):,} gambar -> '\n",
    "        f'Train +{len(train_indices)} (idx {train_start}-{train_max[char]}), '\n",
    "        f'Test +{len(test_indices)} (idx {test_start}-{test_max[char]})'\n",
    "    )\n",
    "\n",
    "print(f'\\nTotal EMNIST disimpan ke Train/Normal: {total_train:,}')\n",
    "print(f'Total EMNIST disimpan ke Test/Normal:  {total_test:,}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["## 7. Verifikasi & Laporan Akhir"]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "after_train = len(os.listdir(TRAIN_DST))\n",
    "after_test = len(os.listdir(TEST_DST))\n",
    "\n",
    "print('=' * 55)\n",
    "print('LAPORAN AKHIR')\n",
    "print('=' * 55)\n",
    "print(f'\\nTrain/Normal: {before_train:,} -> {after_train:,} (+{after_train - before_train:,})')\n",
    "print(f'Test/Normal:  {before_test:,} -> {after_test:,} (+{after_test - before_test:,})')\n",
    "print(f'\\nTotal Normal (Train+Test): {after_train + after_test:,}')\n",
    "\n",
    "# Cek keseimbangan kelas\n",
    "train_corr = len(os.listdir(os.path.join(BASE, 'Gambo_EMNIST', 'Train', 'Corrected')))\n",
    "train_rev = len(os.listdir(os.path.join(BASE, 'Gambo_EMNIST', 'Train', 'Reversal')))\n",
    "test_corr = len(os.listdir(os.path.join(BASE, 'Gambo_EMNIST', 'Test', 'Corrected')))\n",
    "test_rev = len(os.listdir(os.path.join(BASE, 'Gambo_EMNIST', 'Test', 'Reversal')))\n",
    "\n",
    "total_normal = after_train + after_test\n",
    "total_dyslexia = train_corr + train_rev + test_corr + test_rev\n",
    "\n",
    "print(f'\\n--- Keseimbangan Kelas ---')\n",
    "print(f'Total Normal (0):   {total_normal:,}')\n",
    "print(f'Total Dyslexia (1): {total_dyslexia:,} (Corrected: {train_corr+test_corr:,}, Reversal: {train_rev+test_rev:,})')\n",
    "\n",
    "if total_normal > 0:\n",
    "    ratio = total_dyslexia / total_normal\n",
    "    print(f'Rasio Normal:Dyslexia = 1:{ratio:.2f}')\n",
    "    if 0.8 <= ratio <= 1.2:\n",
    "        print('Status: SEIMBANG')\n",
    "    elif ratio > 1.2:\n",
    "        print(f'Status: Dyslexia masih lebih banyak ({(ratio-1)*100:.0f}% lebih)')\n",
    "    else:\n",
    "        print(f'Status: Normal sudah lebih banyak')"
   ]
  }
 ]
}

with open('notebooks/EMNIST_to_Gambo.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print('Notebook berhasil dibuat: notebooks/EMNIST_to_Gambo.ipynb')
