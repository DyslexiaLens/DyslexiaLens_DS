import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

# === KONFIGURASI PATH ===
GAMBO_DIR = 'Gambo'
EMNIST_DIR = 'EMNIST_Processed'
OUTPUT_DIR = 'Dataset_Ready'

def gather_all_data():
    data = []
    
    # 1. Kumpulkan Data Gambo
    print("Mengumpulkan data Gambo...")
    for root, _, files in os.walk(GAMBO_DIR):
        for file in files:
            if file.endswith('.png'):
                path_full = os.path.join(root, file)
                # Buang label noise
                if 'Normal' in file and 'Normal' not in root:
                    continue
                    
                target_class = 0 if 'Normal' in root else 1
                source = 'Gambo'
                data.append({
                    'image_path': path_full,
                    'file_name': file,
                    'target_class': target_class,
                    'source': source
                })
                
    # 2. Kumpulkan Data EMNIST
    print("Mengumpulkan data EMNIST Processed...")
    if os.path.exists(EMNIST_DIR):
        for root, _, files in os.walk(EMNIST_DIR):
            for file in files:
                if file.endswith('.png'):
                    path_full = os.path.join(root, file)
                    data.append({
                        'image_path': path_full,
                        'file_name': file,
                        'target_class': 0, # EMNIST selalu kelas Normal
                        'source': 'EMNIST'
                    })
    
    return pd.DataFrame(data)

def create_stratified_split(df):
    print(f"\nTotal Dataset Keseluruhan: {len(df):,} gambar")
    
    # Stratify berdasarkan kelas (Normal/Dyslexia) DAN sumber (Gambo/EMNIST)
    # Ini memastikan proporsi EMNIST dan Gambo merata di Train dan Test
    # Kita gabungkan kolom target_class dan source untuk stratifikasi ganda
    df['stratify_key'] = df['target_class'].astype(str) + "_" + df['source']
    
    # Split 80% Train, 20% Test
    train_df, test_df = train_test_split(
        df, 
        test_size=0.20, 
        random_state=42, 
        stratify=df['stratify_key']
    )
    
    print("\n=== DISTRIBUSI TRAIN (80%) ===")
    print(train_df['target_class'].value_counts(normalize=True).apply(lambda x: f"{x:.1%}"))
    
    print("\n=== DISTRIBUSI TEST (20%) ===")
    print(test_df['target_class'].value_counts(normalize=True).apply(lambda x: f"{x:.1%}"))
    
    return train_df, test_df

def copy_to_ready_dataset(train_df, test_df):
    print("\nMembuat struktur folder Dataset_Ready...")
    # Buat direktori tujuan
    for split in ['Train', 'Test']:
        for cls in ['Normal', 'Dyslexia']:
            os.makedirs(os.path.join(OUTPUT_DIR, split, cls), exist_ok=True)
            
    # Copy fungsi bantuan
    def copy_files(df_subset, split_name):
        print(f"Menyalin file {split_name}...")
        for _, row in df_subset.iterrows():
            cls_name = 'Normal' if row['target_class'] == 0 else 'Dyslexia'
            # Tambahkan prefix sumber agar nama file unik saat digabung
            new_filename = f"{row['source']}_{row['file_name']}"
            dest = os.path.join(OUTPUT_DIR, split_name, cls_name, new_filename)
            shutil.copy2(row['image_path'], dest)
            
    copy_files(train_df, 'Train')
    copy_files(test_df, 'Test')
    
    print("\n✅ Penyalinan fisik selesai! Folder 'Dataset_Ready' siap digunakan oleh AI Engineer.")

if __name__ == "__main__":
    df = gather_all_data()
    train_df, test_df = create_stratified_split(df)
    copy_to_ready_dataset(train_df, test_df)
    
    # Update master_dataset_dyslexia.csv agar menunjuk ke Dataset_Ready
    df_combined = pd.concat([train_df.assign(split='Train'), test_df.assign(split='Test')])
    df_combined.drop(columns=['stratify_key'], inplace=True)
    df_combined.to_csv('master_dataset_dyslexia.csv', index=False)
    print("✅ File 'master_dataset_dyslexia.csv' telah diperbarui!")
