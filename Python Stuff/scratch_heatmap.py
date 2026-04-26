import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

def compute_mean_image(subset, prefix='notebooks/', n=500):
    samples = subset.sample(min(n, len(subset)), random_state=42)
    arrays = []
    loaded = 0
    missing = 0
    for _, row in samples.iterrows():
        # Path di CSV: Dataset\Gambo\Train\...
        # Folder sebenarnya: notebooks\Dataset\Gambo\Train\...
        img_path = os.path.join(prefix, row['image_path'])
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path).convert('L').resize((28, 28))
                arrays.append(np.array(img, dtype=np.float32))
                loaded += 1
            else:
                missing += 1
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
            continue
    print(f"  Loaded: {loaded}, Missing: {missing}")
    return np.mean(arrays, axis=0) if len(arrays) > 0 else np.zeros((28,28))

print("Loading Rainy's Dataset...")
df = pd.read_csv('csv_metadata/Rainy/master_dataset_final.csv')

print(f"Score 1 count: {len(df[df['severity_score'] == 1])}")
print(f"Score 6 count: {len(df[df['severity_score'] == 6])}")

print("\nComputing mean image for Score 1...")
mean_s1 = compute_mean_image(df[df['severity_score'] == 1])

print("Computing mean image for Score 6...")
mean_s6 = compute_mean_image(df[df['severity_score'] == 6])

print(f"\nMean S1 range: {mean_s1.min():.1f} - {mean_s1.max():.1f}")
print(f"Mean S6 range: {mean_s6.min():.1f} - {mean_s6.max():.1f}")
diff = np.abs(mean_s1 - mean_s6)
print(f"Diff range: {diff.min():.1f} - {diff.max():.1f}")

print("\nGenerating Heatmap Plot...")
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(mean_s1, cmap='gray')
axes[0].set_title('Rata-rata Skor 1 (Ringan)', fontweight='bold')
axes[0].axis('off')
axes[1].imshow(mean_s6, cmap='gray')
axes[1].set_title('Rata-rata Skor 6 (Parah)', fontweight='bold')
axes[1].axis('off')
axes[2].imshow(diff, cmap='hot')
axes[2].set_title('Perbedaan (|Skor 1 - Skor 6|)', fontweight='bold')
axes[2].axis('off')

plt.suptitle('Heatmap Rata-rata Piksel: Skor 1 vs Skor 6', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()

print("Saving to assets/heatmap_rainy.png...")
plt.savefig('assets/heatmap_rainy.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Done!")
