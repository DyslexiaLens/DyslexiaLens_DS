import sys, pandas as pd, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CSV = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\csv_metadata\Dataset_Dyslexia_NoAugmentation.csv"
df = pd.read_csv(CSV)
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Check for problematic files
patterns = {
    "Normal_bare": r'^Normal(\s*\(\d+\))?\.png$',
    "Reversal_bare": r'^Reversal\d*(\s*\(\d+\))?\.png$',
    "Alpha_only": r'^[A-Za-z]\.png$',
    "Alpha_paren": r'^[A-Za-z]\s*\(\d+\)\.png$',
}

for label, pat in patterns.items():
    matches = df[df['file_name'].str.match(pat, na=False)]
    if len(matches) > 0:
        print(f"\n[{label}] Found {len(matches)} matches:")
        for _, row in matches.head(10).iterrows():
            print(f"  {row['folder_category']:10s} | {row['file_name']}")
    else:
        print(f"[{label}] None found")

# Also check: any file_name that doesn't match digit_digit or Letter-digit or NormalNNN patterns
print("\n--- Non-standard names sample ---")
normal_rows = df[df['folder_category'] == 'Normal']
standard = normal_rows['file_name'].str.match(r'^([A-Za-z]-\d+|Normal\d+\s*\(\d+\)|[a-zA-Z]_\d+)\.png$', na=False)
bad_normal = normal_rows[~standard]
print(f"Normal folder non-standard: {len(bad_normal)}")
if len(bad_normal) > 0:
    print(bad_normal['file_name'].head(20).tolist())

for cat in ['Corrected', 'Reversal']:
    cat_rows = df[df['folder_category'] == cat]
    standard_c = cat_rows['file_name'].str.match(r'^\d+_\d+\.png$', na=False)
    bad_c = cat_rows[~standard_c]
    print(f"\n{cat} folder non-standard: {len(bad_c)}")
    if len(bad_c) > 0:
        print(bad_c['file_name'].head(20).tolist())
