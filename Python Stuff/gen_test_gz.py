"""
Generate dyslexialens_test_EMNIST.csv.gz dari Test split master_dataset_emnist_final.csv.
Format output: kolom 'label' (target_class) + pixel0-pixel783 (784 piksel grayscale 28x28).
"""
import pandas as pd
import numpy as np
from PIL import Image
import os

CSV_SRC = 'notebooks/master_dataset_emnist_final.csv'
OUTPUT = 'dyslexialens_test_EMNIST.csv.gz'

df = pd.read_csv(CSV_SRC)
test_df = df[df['split'] == 'Test'].copy()
print(f'Test images to process: {len(test_df):,}')

rows = []
errors = 0
for i, (_, row) in enumerate(test_df.iterrows()):
    # Path relatif dari root project
    img_path = row['image_path']
    # Coba dari notebooks/ dulu (karena CSV dibuat dari sana)
    if not os.path.exists(img_path):
        img_path = os.path.join('notebooks', row['image_path'])
    if not os.path.exists(img_path):
        errors += 1
        continue

    img = Image.open(img_path).convert('L').resize((28, 28))
    pixels = np.array(img, dtype=np.uint8).flatten()
    pixel_row = [int(row['target_class'])] + pixels.tolist()
    rows.append(pixel_row)

    if (i + 1) % 10000 == 0:
        print(f'  Processed {i+1:,}/{len(test_df):,}...')

# Build DataFrame
cols = ['label'] + [f'pixel{i}' for i in range(784)]
df_out = pd.DataFrame(rows, columns=cols)
df_out = df_out.astype(np.uint8)

# Save compressed
df_out.to_csv(OUTPUT, index=False, compression='gzip')
size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
print(f'\nDone! {OUTPUT} ({size_mb:.1f} MB)')
print(f'Total images: {len(df_out):,} | Errors: {errors}')
print(df_out['label'].value_counts().rename({0:'Normal', 1:'Disleksia'}))
