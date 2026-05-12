import glob, os

dup_files = glob.glob(r'd:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dataset\Gambo_Split\Duplicate\**\*.png', recursive=True)
final_files = glob.glob(r'd:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dataset\Gambo_hapusPutihFinal\**\*.png', recursive=True)

final_basenames = [os.path.basename(f) for f in final_files]

def parse_duplicate_filename(filename):
    name_without_ext = filename.rsplit('.', 1)[0]
    parts = name_without_ext.split('_')
    if len(parts) >= 4 and parts[-1].isdigit():
        category = parts[1]
        original_stem = '_'.join(parts[2:-1])
        original_name = f"{original_stem}.png"
        return category, original_name
    return None, None

missing = []
for f in dup_files:
    fname = os.path.basename(f)
    category, orig_name = parse_duplicate_filename(fname)
    if not orig_name:
        missing.append((fname, 'Failed to parse'))
        continue
    
    # Check if this orig_name exists in ANY of the splits in final
    found = False
    for split in ['Train', 'Test', 'Validation']:
        expected = f"{split}_{category}_{orig_name}"
        if expected in final_basenames:
            # We found ONE. We remove it from final_basenames so we can find duplicates
            final_basenames.remove(expected)
            found = True
            break
    if not found:
        missing.append((fname, f'Not found as {orig_name}'))

print(f'Missing files from Duplicate: {len(missing)}')
for m in missing:
    print(m)
