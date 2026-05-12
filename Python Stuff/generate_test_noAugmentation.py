import pandas as pd
import numpy as np
from PIL import Image
import os

# Target CSV
CSV_SRC = r'd:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\csv_metadata\Dataset_Dyslexia_NoAugmentation.csv'
# Target Output
OUTPUT = r'd:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\csv_metadata\dyslexialens_test_noAugmentation.csv.gz'
ROOT_DIR = r'd:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks'

df = pd.read_csv(CSV_SRC)
test_df = df[df['split'] == 'Test'].copy()
print(f'Test images to process: {len(test_df):,}')

rows = []
errors = 0
for i, (_, row) in enumerate(test_df.iterrows()):
    img_path = row['image_path']
    # Check if absolute path
    if not os.path.exists(img_path):
        img_path = os.path.join(ROOT_DIR, row['image_path'])
        
    if not os.path.exists(img_path):
        errors += 1
        continue

    try:
        img = Image.open(img_path).convert('L').resize((28, 28))
        pixels = np.array(img, dtype=np.uint8).flatten()
        pixel_row = [int(row['target_class'])] + pixels.tolist()
        rows.append(pixel_row)
    except Exception as e:
        errors += 1
        print(f"Error reading {img_path}: {e}")

    if (i + 1) % 5000 == 0:
        print(f'  Processed {i+1:,}/{len(test_df):,}...')

# Build DataFrame
print("Building dataframe...")
cols = ['label'] + [f'pixel{i}' for i in range(784)]
df_out = pd.DataFrame(rows, columns=cols)
df_out = df_out.astype(np.uint8)

# Save compressed
print("Compressing and saving to disk...")
df_out.to_csv(OUTPUT, index=False, compression='gzip')
size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
print(f'\nDone! {OUTPUT} ({size_mb:.1f} MB)')
print(f'Total images: {len(df_out):,} | Errors: {errors}')
print(df_out['label'].value_counts().rename({0:'Normal', 1:'Disleksia'}))
