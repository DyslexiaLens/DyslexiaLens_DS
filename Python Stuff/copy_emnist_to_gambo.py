"""
Script: Salin data EMNIST_Processed ke Gambo_EMNIST (Train/Normal & Test/Normal)
- Split 80:20 (Train:Test) per huruf
- Penamaan melanjutkan index terakhir yang sudah ada di folder tujuan
- Format: {Huruf}-{index}.png
"""
import os
import re
import shutil
import random
from collections import defaultdict

random.seed(42)

BASE = 'notebooks/Dataset'
EMNIST_SRC = os.path.join(BASE, 'EMNIST_Processed')
TRAIN_DST = os.path.join(BASE, 'Gambo_EMNIST', 'Train', 'Normal')
TEST_DST = os.path.join(BASE, 'Gambo_EMNIST', 'Test', 'Normal')

SPLIT_RATIO = 0.8  # 80% Train, 20% Test

# =====================================================
# STEP 1: Scan index terakhir per huruf di folder tujuan
# =====================================================
def get_max_index_per_letter(folder):
    max_idx = defaultdict(int)
    for f in os.listdir(folder):
        m = re.match(r'^([A-Za-z])[-_](\d+)\.png$', f)
        if m:
            letter = m.group(1)
            idx = int(m.group(2))
            if idx > max_idx[letter]:
                max_idx[letter] = idx
    return max_idx

print("Scanning existing max indices...")
train_max = get_max_index_per_letter(TRAIN_DST)
test_max = get_max_index_per_letter(TEST_DST)

# =====================================================
# STEP 2: Mapping subfolder EMNIST -> huruf target
# =====================================================
# EMNIST_Processed subfolders: "A-41", "a-61", etc.
# Kita ambil huruf pertama dari nama subfolder
emnist_dirs = sorted(os.listdir(EMNIST_SRC))
print(f"Found {len(emnist_dirs)} EMNIST letter folders.\n")

total_train_copied = 0
total_test_copied = 0

for edir in emnist_dirs:
    edir_path = os.path.join(EMNIST_SRC, edir)
    if not os.path.isdir(edir_path):
        continue

    # Extract letter (first character of folder name)
    letter = edir[0]

    # Collect all files in this EMNIST subfolder
    files = [f for f in os.listdir(edir_path) if f.endswith('.png')]
    random.shuffle(files)

    # Split 80:20
    split_idx = int(len(files) * SPLIT_RATIO)
    train_files = files[:split_idx]
    test_files = files[split_idx:]

    # Start index = current max + 1
    train_start = train_max.get(letter, 0) + 1
    test_start = test_max.get(letter, 0) + 1

    # Copy to Train/Normal
    for i, src_file in enumerate(train_files):
        new_idx = train_start + i
        new_name = f"{letter}-{new_idx}.png"
        src_path = os.path.join(edir_path, src_file)
        dst_path = os.path.join(TRAIN_DST, new_name)
        shutil.copy2(src_path, dst_path)

    # Update max index for Train
    if train_files:
        train_max[letter] = train_start + len(train_files) - 1

    # Copy to Test/Normal
    for i, src_file in enumerate(test_files):
        new_idx = test_start + i
        new_name = f"{letter}-{new_idx}.png"
        src_path = os.path.join(edir_path, src_file)
        dst_path = os.path.join(TEST_DST, new_name)
        shutil.copy2(src_path, dst_path)

    # Update max index for Test
    if test_files:
        test_max[letter] = test_start + len(test_files) - 1

    total_train_copied += len(train_files)
    total_test_copied += len(test_files)

    print(f"  [{edir}] -> '{letter}': Train +{len(train_files)} (idx {train_start}-{train_max[letter]}), "
          f"Test +{len(test_files)} (idx {test_start}-{test_max[letter]})")

# =====================================================
# STEP 3: Laporan Akhir
# =====================================================
print(f"\n{'='*50}")
print(f"SELESAI!")
print(f"  Total disalin ke Train/Normal: {total_train_copied}")
print(f"  Total disalin ke Test/Normal:  {total_test_copied}")
print(f"  Grand Total EMNIST disalin:    {total_train_copied + total_test_copied}")
print(f"\nJumlah file akhir:")
print(f"  Train/Normal: {len(os.listdir(TRAIN_DST))}")
print(f"  Test/Normal:  {len(os.listdir(TEST_DST))}")
