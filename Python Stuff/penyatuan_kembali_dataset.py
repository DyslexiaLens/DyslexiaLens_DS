import os
import re
import pandas as pd

from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

root_dir = r'Dataset/Gambo_hapusPutihFinal'

output_csv = 'master_dataset_final.csv'

SCORE_MAP_ORIGINAL = {
    1: 6,
    4: 6,
    5: 5,
    6: 4,
    7: 3,
    8: 2,
    9: 1
}

# ============================================================
# REGEX FILTER
# ============================================================

RE_DUPLICATE_WIN = re.compile(r'\(\d+\)')
RE_PLACEHOLDER = re.compile(
    r'^(Normal|Reversal|Corrected)\.png$',
    re.IGNORECASE
)

RE_GLITCH = re.compile(r'\.qNcy', re.IGNORECASE)

RE_ALPHA_ONLY = re.compile(r'^[A-Za-z]\.png$')

RE_NORMAL_NUMBER = re.compile(r'^Normal\d+', re.IGNORECASE)

RE_REVERSAL_NUMBER = re.compile(r'^Reversal\d+', re.IGNORECASE)

RE_STARTS_WITH_ALPHA = re.compile(r'^[A-Za-z][-_.]')

# ============================================================
# SCAN DATASET
# ============================================================

print('Scanning dataset...\n')

data = []

filtered_out = {
    'duplicate': 0,
    'placeholder': 0,
    'glitch': 0,
    'alpha_only': 0,
    'normal_number': 0,
    'reversal_number': 0,
    'starts_alpha': 0,
    'missing_file': 0
}

processed = 0

for root, dirs, files in os.walk(root_dir):

    for file in files:

        if not file.lower().endswith('.png'):
            continue

        processed += 1

        if processed % 10000 == 0:
            print(f'Processed: {processed:,}')

        parts = Path(root).parts

        try:
            split_type = parts[-2]
            category = parts[-1]
        except:
            continue

        # ====================================================
        # STRIP PREFIX
        # ====================================================
        
        prefix = f"{split_type}_{category}_"
        if file.startswith(prefix):
            original_filename = file[len(prefix):]
        else:
            original_filename = file

        # ====================================================
        # FILTER
        # ====================================================

        if RE_DUPLICATE_WIN.search(original_filename):
            filtered_out['duplicate'] += 1
            continue

        if RE_GLITCH.search(original_filename):
            filtered_out['glitch'] += 1
            continue

        if RE_PLACEHOLDER.match(original_filename):
            filtered_out['placeholder'] += 1
            continue

        if category in ['Corrected', 'Reversal'] and RE_ALPHA_ONLY.match(original_filename):
            filtered_out['alpha_only'] += 1
            continue

        if category == 'Normal' and RE_NORMAL_NUMBER.match(original_filename):
            filtered_out['normal_number'] += 1
            continue

        if category == 'Reversal' and RE_REVERSAL_NUMBER.match(original_filename):
            filtered_out['reversal_number'] += 1
            continue

        if category in ['Corrected', 'Reversal'] and RE_STARTS_WITH_ALPHA.match(original_filename):
            filtered_out['starts_alpha'] += 1
            continue

        # ====================================================
        # VALIDASI FILE
        # ====================================================

        path_full = os.path.normpath(os.path.join(root, file))

        if not os.path.exists(path_full):
            filtered_out['missing_file'] += 1
            continue

        # ====================================================
        # SAVE ROW
        # ====================================================

        data.append({
            'image_path': path_full,
            'file_name': file,
            'original_filename': original_filename,
            'split': split_type,
            'folder_category': category
        })

# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(data)

print(f'\nTotal kandidat bersih: {len(df):,}')

# ============================================================
# LABELING
# ============================================================

def get_score(row):

    filename = row['original_filename']
    folder = row['folder_category']

    # mismatch
    if 'Normal' in filename and folder != 'Normal':
        return 'DROP'

    # normal
    if folder == 'Normal':
        return 0

    # corrected/reversal
    if folder in ['Corrected', 'Reversal']:

        for sep in ['_', '-']:

            if sep in filename:

                prefix = filename.split(sep)[0]

                if prefix.isdigit():

                    val = int(prefix)

                    if 1 <= val <= 6:
                        return val

                    elif val in SCORE_MAP_ORIGINAL:
                        return SCORE_MAP_ORIGINAL[val]

                break

    return 'DROP'

# ============================================================
# APPLY SCORE
# ============================================================

df['severity_score'] = df.apply(get_score, axis=1)

dropped_by_score = len(
    df[df['severity_score'].astype(str) == 'DROP']
)

print(f'\nDropped by get_score: {dropped_by_score:,}')

# ============================================================
# CLEAN FINAL
# ============================================================

df_clean = df[
    ~df['severity_score'].astype(str).str.contains('DROP')
].copy()

df_clean['severity_score'] = df_clean['severity_score'].astype(int)

df_clean['target_class'] = df_clean['severity_score'].apply(
    lambda x: 0 if x == 0 else 1
)

# ============================================================
# SAVE CSV
# ============================================================

df_clean.drop(columns=['original_filename'], inplace=True, errors='ignore')
df_clean.to_csv(output_csv, index=False)

# ============================================================
# SUMMARY
# ============================================================

print('\n=== FILTER SUMMARY ===')

for k, v in filtered_out.items():
    print(f'{k:20s}: {v:,}')

print(f'\nFinal dataset: {len(df_clean):,} rows')

print(f'\nCSV saved:')
print(output_csv)

print('\nContoh data:')
print(df_clean.sample(5))