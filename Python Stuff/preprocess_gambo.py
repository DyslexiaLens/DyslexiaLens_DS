import os
import shutil
from PIL import Image
from multiprocessing import Pool, cpu_count
from pathlib import Path

def process_image(task):
    src_path, dst_path = task
    try:
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        
        # Open image, convert to grayscale, then binarize
        with Image.open(src_path) as img:
            img = img.convert('L')
            # Binarization (0 or 255)
            img = img.point(lambda p: 255 if p > 127 else 0, mode='1')
            img.save(dst_path)
        return True
    except Exception as e:
        print(f"Error processing {src_path}: {e}")
        return False

def main():
    source_dir = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\dataset_test1\Gambo"
    dest_dir = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\dataset_test1\Gambo_Processed"
    
    tasks = []
    
    print("Memindai dataset untuk di-restrukturisasi...")
    
    # Iterate through Train and Test
    for split in ['Train', 'Test']:
        split_path = os.path.join(source_dir, split)
        if not os.path.exists(split_path):
            continue
            
        for cls in ['Corrected', 'Normal', 'Reversal']:
            cls_path = os.path.join(split_path, cls)
            if not os.path.exists(cls_path):
                continue
                
            for filename in os.listdir(cls_path):
                if not filename.endswith('.png'):
                    continue
                    
                src_path = os.path.join(cls_path, filename)
                
                # Extract character from filename
                # Filenames look like: A-0.png, A-1000.png, 4_10.png, d_1541.png, 1_1.png
                if '-' in filename:
                    char_prefix = filename.split('-')[0]
                elif '_' in filename:
                    char_prefix = filename.split('_')[0]
                else:
                    char_prefix = 'unknown'
                
                # Build new destination path
                # Structure: Gambo_Processed/<Character>/<Class>/<filename>
                # e.g., Gambo_Processed/d/Normal/d_1541.png
                dst_path = os.path.join(dest_dir, char_prefix, cls, filename)
                
                tasks.append((src_path, dst_path))

    print(f"Total gambar yang akan diproses: {len(tasks)}")
    
    # Use multiprocessing to speed up image processing
    pool = Pool(processes=cpu_count())
    results = pool.map(process_image, tasks)
    
    pool.close()
    pool.join()
    
    success_count = sum(results)
    print(f"Selesai! {success_count}/{len(tasks)} gambar berhasil diproses dan direstrukturisasi di dalam folder 'Gambo_Processed'.")

if __name__ == '__main__':
    main()
