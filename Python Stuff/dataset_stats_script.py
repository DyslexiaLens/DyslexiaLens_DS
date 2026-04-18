import os
from PIL import Image
import json
from collections import defaultdict

def analyze_dataset(root_dir):
    stats = {}
    total_images = 0
    extensions = defaultdict(int)
    corrupted_files = []
    resolutions = defaultdict(int)
    image_modes = defaultdict(int)

    for split in ['Train', 'Test']:
        stats[split] = {}
        split_path = os.path.join(root_dir, split)
        if not os.path.exists(split_path):
            continue
            
        for cls in ['Corrected', 'Normal', 'Reversal']:
            cls_path = os.path.join(split_path, cls)
            if not os.path.exists(cls_path):
                continue
                
            files = [f for f in os.listdir(cls_path) if os.path.isfile(os.path.join(cls_path, f))]
            stats[split][cls] = {
                'count': len(files),
                'extensions': defaultdict(int)
            }
            
            for i, f in enumerate(files):
                ext = os.path.splitext(f)[1].lower()
                stats[split][cls]['extensions'][ext] += 1
                extensions[ext] += 1
                total_images += 1
                
                # Check a few resolutions/modes per class per split
                if i < 50: # Check up to 50 images per class for resolution stats
                    try:
                        img_path = os.path.join(cls_path, f)
                        with Image.open(img_path) as img:
                            res = f"{img.size[0]}x{img.size[1]}"
                            resolutions[res] += 1
                            image_modes[img.mode] += 1
                    except Exception as e:
                        corrupted_files.append(img_path)

    # Convert defaultdict to print safely
    for split in stats:
        for cls in stats[split]:
            stats[split][cls]['extensions'] = dict(stats[split][cls]['extensions'])

    report = {
        'total_images': total_images,
        'split_stats': stats,
        'global_extensions': dict(extensions),
        'corrupted_files_count': len(corrupted_files),
        'corrupted_files_sample': corrupted_files[:5],
        'sample_resolutions': dict(resolutions),
        'sample_image_modes': dict(image_modes)
    }
    
    print(json.dumps(report, indent=4))

if __name__ == '__main__':
    analyze_dataset(r'd:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\dataset_test1\Gambo')
