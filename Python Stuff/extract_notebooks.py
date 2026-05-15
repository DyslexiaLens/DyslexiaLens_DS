import json
import os

notebooks = [
    r"D:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dyslexia_EMNIST.ipynb",
    r"D:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dyslexia_NoAugmentation_hapusPutih.ipynb",
    r"D:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\EMNIST_to_Gambo.ipynb"
]

def ipynb_to_md(ipynb_path):
    if not os.path.exists(ipynb_path):
        print(f"[ERROR] File tidak ditemukan: {ipynb_path}")
        return

    # Buat nama file output dengan ekstensi .md
    md_path = ipynb_path.replace('.ipynb', '.md')
    
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
            
        with open(md_path, 'w', encoding='utf-8') as f:
            for cell in nb.get('cells', []):
                cell_type = cell.get('cell_type')
                source = "".join(cell.get('source', []))
                
                if cell_type == 'markdown':
                    f.write(source + "\n\n")
                elif cell_type == 'code':
                    # Abaikan cell code yang kosong
                    if source.strip() != "":
                        f.write("```python\n")
                        f.write(source + "\n")
                        f.write("```\n\n")
                    
        print(f"[SUCCESS] Berhasil diekstrak: {os.path.basename(md_path)}")
    except Exception as e:
        print(f"[ERROR] Gagal mengekstrak {os.path.basename(ipynb_path)}: {e}")

print("Mengekstrak Notebooks ke Markdown...")
for nb in notebooks:
    ipynb_to_md(nb)
print("Selesai!")
