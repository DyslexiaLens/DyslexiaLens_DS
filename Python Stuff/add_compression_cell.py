import json
import sys

path = 'notebooks/Dyslexia_NoAugmentation.ipynb'
try:
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    new_cell = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '---\n',
            '## 📦 Kompresi Dataset\n',
            'Kompilasi folder `Dataset/Gambo` menjadi `.zip` agar mudah dibagikan kepada kolega.'
        ]
    }
    
    code_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'import shutil\n',
            'import os\n',
            '\n',
            'folder_to_zip = \'Dataset/Gambo\'\n',
            'output_zip = \'Dataset_Gambo_Final\'\n',
            '\n',
            'if os.path.exists(folder_to_zip):\n',
            '    print(f"Mengompresi {folder_to_zip} menjadi {output_zip}.zip...")\n',
            '    shutil.make_archive(output_zip, \'zip\', folder_to_zip)\n',
            '    print("✅ Selesai! File zip berhasil dibuat di direktori saat ini.")\n',
            'else:\n',
            '    print(f"❌ Folder {folder_to_zip} tidak ditemukan!")\n'
        ]
    }
    
    nb['cells'].extend([new_cell, code_cell])
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
        
    print(f"Berhasil menambahkan cell kompresi ke {path}")
except Exception as e:
    print(f"Error: {e}")
