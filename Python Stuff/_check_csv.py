import os, pandas as pd

# Let's check what's actually in the CSV files.
csv_files = [
    r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\master_dataset_dyslexia.csv",
    r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\csv_metadata\Dataset_Dyslexia_NoAugmentation.csv"
]

print("Scanning CSVs for anomalies...")
for csv in csv_files:
    if not os.path.exists(csv):
        print(f"NOT FOUND: {csv}")
        continue
    
    df = pd.read_csv(csv)
    print(f"\n--- {os.path.basename(csv)} ---")
    
    # 1. Normal with parenthesis
    anomalies_paren = df[df['file_name'].str.contains(r'\(.*?\)', na=False)]
    print(f"Files with parenthesis: {len(anomalies_paren)}")
    if len(anomalies_paren) > 0:
        print(anomalies_paren['file_name'].head(5).tolist())

    # 2. Files with .qNcy3 or weird extensions
    weird = df[df['file_name'].str.contains(r'\.qNcy', na=False)]
    print(f"Files with .qNcy: {len(weird)}")
    if len(weird) > 0:
        print(weird['file_name'].head(5).tolist())
    
    # Let's also check for EMNIST-style files like e-491 in Reversal
    # Usually EMNIST is e_123.png or E-123.png, if they slipped into Reversal it's bad.
    emnist_in_rev = df[(df['folder_category'] == 'Reversal') & (df['file_name'].str.match(r'^[a-zA-Z]-[0-9]+', na=False))]
    print(f"EMNIST format in Reversal/Corrected: {len(emnist_in_rev)}")
    if len(emnist_in_rev) > 0:
        print(emnist_in_rev['file_name'].head(5).tolist())

