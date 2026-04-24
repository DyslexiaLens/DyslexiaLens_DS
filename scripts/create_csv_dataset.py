import os
import pandas as pd
import numpy as np
from PIL import Image
import time

DATASET_DIR = 'Dataset_Ready'

def images_to_csv(split_name, output_filename):
    print(f"Memproses {split_name} menjadi {output_filename}...")
    start_time = time.time()
    
    rows = []
    split_dir = os.path.join(DATASET_DIR, split_name)
    
    # Label: 0 = Normal, 1 = Dyslexia
    classes = {'Normal': 0, 'Dyslexia': 1}
    
    for cls_name, cls_label in classes.items():
        cls_dir = os.path.join(split_dir, cls_name)
        if not os.path.exists(cls_dir):
            continue
            
        for file in os.listdir(cls_dir):
            if file.endswith('.png'):
                path = os.path.join(cls_dir, file)
                try:
                    # Buka gambar, pastikan Grayscale (L), resize ke 28x28 (jika belum)
                    img = Image.open(path).convert('L').resize((28,28))
                    pixels = np.array(img).flatten().tolist()
                    
                    # Format baris: [label, pixel1, pixel2, ..., pixel784]
                    row = [cls_label] + pixels
                    rows.append(row)
                except Exception as e:
                    pass
                    
    # Buat nama kolom: label, pixel0, pixel1, ..., pixel783
    columns = ['label'] + [f'pixel{i}' for i in range(784)]
    
    print(f"Menyusun DataFrame untuk {split_name}...")
    df = pd.DataFrame(rows, columns=columns)
    
    print(f"Menyimpan ke {output_filename} (Highly Compressed GZIP)...")
    # Simpan sebagai CSV yang dikompres GZIP (Pandas akan otomatis mengenali dari ekstensi)
    df.to_csv(output_filename, index=False, compression='gzip')
    
    file_size = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"✅ Selesai! {split_name} ({len(df):,} baris) -> {file_size:.1f} MB (Waktu: {time.time() - start_time:.1f} detik)")

if __name__ == "__main__":
    print("🚀 Memulai Konversi Dataset_Ready ke CSV (Format EMNIST/MNIST)...")
    images_to_csv('Test', 'dyslexialens_test.csv.gz')
    images_to_csv('Train', 'dyslexialens_train.csv.gz')
    print("\nFile CSV berhasil dibuat! File ini sangat cocok untuk di-upload ke GitHub Releases.")
