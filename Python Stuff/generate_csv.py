import os
import pandas as pd

def generate_master_csv():
    root_dir = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\Gambo"
    
    # 1. Kumpulkan semua rute file 
    print("Membaca seluruh file dataset...")
    data = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.png'):
                # Dapatkan jalur folder relatif
                parts = Path(root).parts
                
                # Format folder: ...\Gambo\[Train/Test]\[Corrected/Normal/Reversal]
                try:
                    split_type = parts[-2]
                    category = parts[-1] 
                except:
                    continue
                    
                path_full = os.path.join(root, file)
                
                data.append({
                    'image_path': path_full,
                    'file_name': file,
                    'split': split_type,
                    'folder_category': category
                })
                
    df = pd.DataFrame(data)
    print(f"Total gambar awal berserakan: {len(df)} file.")
    
    # 2. Proses ekstraksi Label & Menemukan Data "Sampah" (Noise)
    # Trik pintar: Kita bikin kolom baru berdasarkan namannya
    
    def get_score(row):
        filename = row['file_name']
        folder = row['folder_category']
        
        # 1. Mendeteksi Kontaminasi Label (Gambar bernama Normal di folder Corrected)
        if 'Normal' in filename and folder != 'Normal':
            return 'DROP_CONTAIMINATED' # Kita tandai untuk dibuang
            
        # 2. Tentukan Skor untuk model klasifikasi Disleksia
        if folder == 'Normal':
            return 0 # 0 artinya sehat / tidak ada ciri disleksia
            
        if folder in ['Corrected', 'Reversal']:
            # Ekstrak angkanya
            if '_' in filename:
                prefix = filename.split('_')[0]
                if prefix.isdigit() and 1 <= int(prefix) <= 9:
                    return int(prefix)
            if '-' in filename:
                prefix = filename.split('-')[0]
                if prefix.isdigit() and 1 <= int(prefix) <= 9:
                    return int(prefix)
            
            return 'DROP_UNKNOWN' # Format tak terduga
            
        return 'DROP'
        
    df['severity_score'] = df.apply(get_score, axis=1)
    
    # Berapa banyak data yang ternyata cacat/noise?
    total_noise = len(df[df['severity_score'].astype(str).str.contains('DROP')])
    print(f"Ditemukan {total_noise} file dengan format aneh/kontaminasi. Menyingkirkan data kotor tersebut...")
    
    # 3. KEAJAIBAN DATA SCIENCE: Hapus File Kotor Cuma Lewat Tabel!
    df_clean = df[~df['severity_score'].astype(str).str.contains('DROP')].copy()
    
    # Tentukan Target Classification Utama (0 = Normal, 1 = Ada Disleksia)
    df_clean['target_class'] = df_clean['severity_score'].apply(lambda x: 0 if x == 0 else 1)
    
    # Simpan ke CSV
    output_csv = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\dyslexialens_master_dataset.csv"
    df_clean.to_csv(output_csv, index=False)
    
    print(f"\nSelesai! Berhasil menyimpan data bersih sebanyak: {len(df_clean)} file ke dalam 'dyslexialens_master_dataset.csv'")
    print("Contoh 3 Baris Tabel Yang Akan Dibaca AI nanti:")
    print(df_clean[['image_path', 'target_class', 'severity_score']].sample(3).to_string(index=False))

if __name__ == '__main__':
    from pathlib import Path
    generate_master_csv()
