import os
import cv2
import pandas as pd
import numpy as np
import shutil

def process_images():
    base_dir = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\Dataset"
    source_dir = os.path.join(base_dir, "Gambo")
    target_dir = os.path.join(base_dir, "Gambo_Standardized")
    
    # 1. Hapus target_dir jika ada
    if os.path.exists(target_dir):
        print(f"Menghapus direktori lama: {target_dir}")
        shutil.rmtree(target_dir)
    
    os.makedirs(target_dir, exist_ok=True)
    
    # 2. Iterasi semua file gambar
    image_paths = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                image_paths.append(os.path.join(root, file))
                
    print(f"Total gambar ditemukan: {len(image_paths)}")
    
    # Titik ideal: Kita tidak memaksakan scaling untuk yang beresolusi kecil/besar yang beda sedikit. 
    # Kita gunakan PADDING ke ukuran seragam agar tidak ada distorsi dan kehilangan fitur.
    # Karena max resolusi Gambo adalah 31x31 (berdasarkan notebook), kita pad ke 32x32.
    TARGET_SIZE = 32 
    
    print(f"Memulai proses standardisasi (Grayscale & Pad to {TARGET_SIZE}x{TARGET_SIZE})...")
    
    processed_count = 0
    for img_path in image_paths:
        # Baca gambar sebagai Grayscale ('L' mode)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            continue
            
        h, w = img.shape[:2]
        
        # Jika gambar lebih besar dari 32x32, kita resize turun dengan ratio sama (jarang terjadi)
        if h > TARGET_SIZE or w > TARGET_SIZE:
            scale = TARGET_SIZE / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            h, w = img.shape[:2]
            
        # PADDING (menambah border putih agar menjadi 32x32, tanpa distorsi aspek rasio)
        top = (TARGET_SIZE - h) // 2
        bottom = TARGET_SIZE - h - top
        left = (TARGET_SIZE - w) // 2
        right = TARGET_SIZE - w - left
        
        # Background Gambo putih (255)
        img_padded = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=255)
        
        # Tentukan path simpan
        rel_path = os.path.relpath(img_path, source_dir)
        save_path = os.path.join(target_dir, rel_path)
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Simpan
        cv2.imwrite(save_path, img_padded)
        processed_count += 1
        
        if processed_count % 10000 == 0:
            print(f"Diproses: {processed_count} / {len(image_paths)}")
            
    print(f"Selesai memproses {processed_count} gambar.")
    print(f"Dataset tersimpan di: {target_dir}")
    
    # 3. Update CSV untuk mereferensikan folder baru
    csv_path = os.path.join(base_dir, "master_dataset_final.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['image_path'] = df['image_path'].str.replace('^Gambo\\\\', 'Gambo_Standardized\\\\', regex=True)
        df['image_path'] = df['image_path'].str.replace('^Gambo/', 'Gambo_Standardized/', regex=True)
        new_csv_path = os.path.join(base_dir, "master_dataset_final_standardized.csv")
        df.to_csv(new_csv_path, index=False)
        print(f"CSV baru telah dibuat dengan path yang diperbarui: {new_csv_path}")

if __name__ == "__main__":
    process_images()
