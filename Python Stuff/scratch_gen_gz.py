import pandas as pd
import numpy as np
import os
from PIL import Image

print("=== Membuat dyslexialens_test_rainy.csv.gz ===\n")

# 1. Load metadata Rainy
df = pd.read_csv('csv_metadata/Rainy/master_dataset_final.csv')
print(f"Total baris di CSV: {len(df):,}")

# 2. Filter hanya split Test
df_test = df[df['split'] == 'Test'].copy()
print(f"Baris Test: {len(df_test):,}")
print(f"  Normal (0): {len(df_test[df_test['target_class'] == 0]):,}")
print(f"  Dyslexia (1): {len(df_test[df_test['target_class'] == 1]):,}")

# 3. Baca tiap gambar, resize ke 28x28 grayscale, flatten jadi 784 piksel
PREFIX = 'notebooks/'
rows = []
loaded = 0
skipped = 0

for i, (_, row) in enumerate(df_test.iterrows()):
    img_path = os.path.join(PREFIX, row['image_path'])
    try:
        if os.path.exists(img_path):
            img = Image.open(img_path).convert('L').resize((28, 28))
            pixels = np.array(img, dtype=np.uint8).flatten()  # 784 values
            row_data = [row['target_class']] + pixels.tolist()
            rows.append(row_data)
            loaded += 1
        else:
            skipped += 1
    except Exception as e:
        skipped += 1
    
    if (i + 1) % 5000 == 0:
        print(f"  Proses: {i+1}/{len(df_test)} (loaded={loaded}, skipped={skipped})")

print(f"\nSelesai memproses! Loaded: {loaded:,}, Skipped: {skipped}")

# 4. Buat DataFrame
col_names = ['label'] + [f'pixel{i}' for i in range(784)]
df_out = pd.DataFrame(rows, columns=col_names)
df_out['label'] = df_out['label'].astype(int)

print(f"\nDataFrame shape: {df_out.shape}")
print(f"Label distribution: {df_out['label'].value_counts().to_dict()}")

# 5. Simpan ke .csv.gz
output_file = 'dyslexialens_test_rainy.csv.gz'
df_out.to_csv(output_file, index=False, compression='gzip')

file_size = os.path.getsize(output_file) / (1024 * 1024)
print(f"\n✅ Berhasil disimpan ke '{output_file}' ({file_size:.1f} MB)")
