import os
import shutil

src_base = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dataset\Gambo_Split"
dst_base = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dataset\Gambo_Fixed"

def parse_duplicate_filename(filename):
    name_without_ext = filename.rsplit('.', 1)[0]
    parts = name_without_ext.split('_')
    # Expected format: Split_Category_OriginalName_DupMarker
    # e.g. Test_Corrected_1_1161_2
    if len(parts) >= 4 and parts[-1].isdigit():
        category = parts[1]
        original_stem = '_'.join(parts[2:-1])
        original_name = f"{original_stem}.png"
        return category, original_name
    return None, None

def main():
    print("=== Memulai Proses Pembuatan Gambo_Fixed ===")
    if not os.path.exists(src_base):
        print(f"Error: Folder asal {src_base} tidak ditemukan!")
        return

    # 1. Copy Train, Test, Validation
    splits = ['Train', 'Test', 'Validation']
    for split in splits:
        src_dir = os.path.join(src_base, split)
        dst_dir = os.path.join(dst_base, split)
        if os.path.exists(src_dir):
            if not os.path.exists(dst_dir):
                print(f"Copying {split} folder ke Gambo_Fixed... (Mohon tunggu, ini akan memakan waktu beberapa menit)")
                shutil.copytree(src_dir, dst_dir)
                print(f"Selesai copy {split}!")
            else:
                print(f"{split} folder sudah ada di Gambo_Fixed. Lewati tahap copy.")

    # 2. Process Duplicate folder
    dup_dir = os.path.join(src_base, 'Duplicate')
    if not os.path.exists(dup_dir):
        print("Folder Duplicate tidak ditemukan.")
        return

    print("\nMemproses file di folder Duplicate...")
    moved_count = 0
    failed_count = 0
    
    # Collect all png files in Duplicate
    dup_files = []
    for root, _, files in os.walk(dup_dir):
        for f in files:
            if f.lower().endswith('.png'):
                dup_files.append((root, f))
                
    total_dups = len(dup_files)
    print(f"Ditemukan {total_dups} file duplikat. Mulai menyebarkan...")
    
    for i, (root, f) in enumerate(dup_files):
        if i % 1000 == 0 and i > 0:
            print(f"  Memproses {i}/{total_dups} file...")
            
        category, orig_name = parse_duplicate_filename(f)
        if not category or not orig_name:
            print(f"  [SKIP] Format nama tidak dikenali: {f}")
            failed_count += 1
            continue
            
        src_path = os.path.join(root, f)
        moved = False
        
        # Cek urutan Train -> Test -> Validation
        for split in splits:
            target_filename = f"{split}_{category}_{orig_name}"
            target_dir = os.path.join(dst_base, split, category)
            target_path = os.path.join(target_dir, target_filename)
            
            if not os.path.exists(target_path):
                # Ketemu tempat kosong!
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy2(src_path, target_path)
                moved = True
                moved_count += 1
                break
                
        if not moved:
            print(f"  [FULL] Tidak ada tempat kosong untuk {f} (semua split sudah punya {orig_name})")
            failed_count += 1

    print("\n=== Ringkasan ===")
    print(f"Total file duplikat yang berhasil disebar: {moved_count}")
    print(f"Total file duplikat yang gagal disebar   : {failed_count}")
    print(f"Folder hasil akhir berada di: {dst_base}")
    print("Selesai!")

if __name__ == '__main__':
    main()
