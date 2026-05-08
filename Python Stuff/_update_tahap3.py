"""
Script untuk memperbarui Tahap 3 di Dyslexia_NoAugmentation.ipynb:
- Menambahkan filter eksplisit untuk file-file "sampah" yang tidak valid
- Mendokumentasikan filter di markdown cell
- Menambahkan log output yang menunjukkan berapa file yang dibuang
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NB_PATH = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dyslexia_NoAugmentation.ipynb"

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# ============================================================
# UPDATE CELL 11: Markdown Tahap 3 — tambahkan dokumentasi filter
# ============================================================
nb["cells"][11] = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "# Tahap 3: Cleaning Data & Pembuatan Master CSV\n",
        "\n",
        "Kode ini melakukan **Logical Cleaning** — memfilter semua file kotor (*Label Noise*) langsung dari tabel Pandas **tanpa menghapus file fisik aslinya**, lalu menyimpan daftar data bersih ke `master_dataset_dyslexia.csv`.\n",
        "\n",
        "Fungsi `get_score` dirancang untuk bekerja dalam **dua kondisi secara otomatis**:\n",
        "- **Jika Tahap 2 dijalankan:** nama file sudah berprefix 1–6, kode membaca langsung.\n",
        "- **Jika Tahap 2 dilewati:** nama file masih berprefix asli (1, 4, 5, 6, 7, 8, 9), kode menerapkan *Dictionary Mapping* secara otomatis ke rentang 0–6.\n",
        "\n",
        "### Filter Pembersihan Eksplisit\n",
        "Selain filter skor, pipeline ini juga membuang file-file **non-sampel** yang terdeteksi di dalam dataset asli periset:\n",
        "\n",
        "| Pola File | Contoh | Alasan Dibuang |\n",
        "|---|---|---|\n",
        "| `Normal.png`, `Normal (N).png` | `Normal.png`, `Normal (1).png` | File placeholder/label, bukan sampel tulisan tangan yang sesungguhnya |\n",
        "| `Reversal.png`, `ReversalN (N).png` | `Reversal.png`, `Reversal1 (1).png` | File placeholder/label, bukan data goresan yang valid |\n",
        "| Huruf abjad tunggal di Corrected/Reversal | `A.png`, `b.png`, `Z (1).png` | File abjad referensi yang bukan merupakan sampel tulisan pasien |\n",
        "| `NormalXXXX.png` di folder non-Normal | `Normal123.png` di Corrected | Label Noise — file Normal yang terselip ke folder disleksia |\n",
        "\n",
        "> **PENTING:** Jalankan sel ini hanya SEKALI setelah Tahap 1 (dan opsional Tahap 2)."
    ]
}

# ============================================================
# UPDATE CELL 12: Code Tahap 3 — tambahkan filter eksplisit
# ============================================================
nb["cells"][12] = {
    "cell_type": "code",
    "metadata": {},
    "source": [
        "import os\n",
        "import re\n",
        "import pandas as pd\n",
        "from pathlib import Path\n",
        "\n",
        "root_dir = r'Dataset/Gambo'\n",
        "\n",
        "# Dictionary Mapping: Skor asli periset (terbalik) -> Skor AI (linear 0-6)\n",
        "# Digunakan sebagai fallback jika Tahap 2 (Physical Renaming) dilewati.\n",
        "SCORE_MAP_ORIGINAL = {1: 6, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}\n",
        "\n",
        "# ============================================================\n",
        "# REGEX FILTER: Pola nama file yang HARUS DIBUANG\n",
        "# ============================================================\n",
        "# 1. File placeholder: Normal.png, Normal (1).png, Normal (2).png, dll.\n",
        "#    -> Bukan sampel tulisan tangan, hanya file label/referensi\n",
        "RE_NORMAL_BARE = re.compile(r'^Normal(\\s*\\(\\d+\\))?\\.png$', re.IGNORECASE)\n",
        "\n",
        "# 2. File placeholder: Reversal.png, Reversal1.png, Reversal1 (1).png, dll.\n",
        "#    -> Bukan data goresan yang valid\n",
        "RE_REVERSAL_BARE = re.compile(r'^Reversal\\d*(\\s*\\(\\d+\\))?\\.png$', re.IGNORECASE)\n",
        "\n",
        "# 3. File abjad tunggal di Corrected/Reversal: A.png, b.png, Z (1).png, dll.\n",
        "#    -> File referensi huruf, bukan sampel tulisan pasien\n",
        "RE_ALPHA_ONLY = re.compile(r'^[A-Za-z](\\s*\\(\\d+\\))?\\.png$')\n",
        "\n",
        "print('Membaca seluruh direktori...')\n",
        "data = []\n",
        "filtered_out = {'normal_bare': 0, 'reversal_bare': 0, 'alpha_only': 0}\n",
        "\n",
        "for root, dirs, files in os.walk(root_dir):\n",
        "    for file in files:\n",
        "        if not file.endswith('.png'):\n",
        "            continue\n",
        "        parts = Path(root).parts\n",
        "        try:\n",
        "            split_type = parts[-2]\n",
        "            category = parts[-1]\n",
        "        except:\n",
        "            continue\n",
        "        \n",
        "        # === FILTER EKSPLISIT ===\n",
        "        # Filter 1: Buang file \"Normal.png\", \"Normal (1).png\", dll.\n",
        "        if RE_NORMAL_BARE.match(file):\n",
        "            filtered_out['normal_bare'] += 1\n",
        "            continue\n",
        "        \n",
        "        # Filter 2: Buang file \"Reversal.png\", \"Reversal1 (1).png\", dll.\n",
        "        if RE_REVERSAL_BARE.match(file):\n",
        "            filtered_out['reversal_bare'] += 1\n",
        "            continue\n",
        "        \n",
        "        # Filter 3: Buang file abjad tunggal di folder Corrected/Reversal\n",
        "        if category in ['Corrected', 'Reversal'] and RE_ALPHA_ONLY.match(file):\n",
        "            filtered_out['alpha_only'] += 1\n",
        "            continue\n",
        "        \n",
        "        path_full = os.path.join(root, file)\n",
        "        data.append({\n",
        "            'image_path': path_full,\n",
        "            'file_name': file,\n",
        "            'split': split_type,\n",
        "            'folder_category': category\n",
        "        })\n",
        "\n",
        "df = pd.DataFrame(data)\n",
        "print(f'Total gambar ditemukan: {len(df)} file.')\n",
        "print(f'\\n=== File Dibuang (Filter Eksplisit) ===')\n",
        "print(f'  Normal placeholder  (Normal.png, dll.)      : {filtered_out[\"normal_bare\"]}')\n",
        "print(f'  Reversal placeholder (Reversal.png, dll.)    : {filtered_out[\"reversal_bare\"]}')\n",
        "print(f'  Abjad tunggal di Corrected/Reversal          : {filtered_out[\"alpha_only\"]}')\n",
        "print(f'  TOTAL dibuang oleh filter eksplisit          : {sum(filtered_out.values())}\\n')\n",
        "\n",
        "def get_score(row):\n",
        "    \"\"\"Ekstrak & normalisasi Severity Score dari nama file.\n",
        "    Bekerja otomatis untuk dataset pre-Tahap 2 (skor asli) maupun post-Tahap 2 (skor 1-6).\n",
        "    \"\"\"\n",
        "    filename = row['file_name']\n",
        "    folder = row['folder_category']\n",
        "\n",
        "    # Buang file NormalXXXX yang tersesat ke kelas non-Normal (Label Noise)\n",
        "    if 'Normal' in filename and folder != 'Normal':\n",
        "        return 'DROP'\n",
        "\n",
        "    # Kelas Normal -> Skor 0 (Sehat)\n",
        "    if folder == 'Normal':\n",
        "        return 0\n",
        "\n",
        "    # Kelas Corrected & Reversal -> Ekstrak prefix angka\n",
        "    if folder in ['Corrected', 'Reversal']:\n",
        "        for sep in ['_', '-']:\n",
        "            if sep in filename:\n",
        "                prefix = filename.split(sep)[0]\n",
        "                if prefix.isdigit():\n",
        "                    val = int(prefix)\n",
        "                    if 1 <= val <= 6:\n",
        "                        # Post-Tahap 2: nama file sudah di-rename ke skala 1-6\n",
        "                        return val\n",
        "                    elif val in SCORE_MAP_ORIGINAL:\n",
        "                        # Pre-Tahap 2: terapkan Dictionary Mapping ke skala AI 0-6\n",
        "                        return SCORE_MAP_ORIGINAL[val]\n",
        "                break\n",
        "\n",
        "    return 'DROP'  # Buang file tak dikenal\n",
        "\n",
        "df['severity_score'] = df.apply(get_score, axis=1)\n",
        "\n",
        "# Hitung berapa yang di-DROP oleh get_score\n",
        "dropped_by_score = len(df[df['severity_score'].astype(str) == 'DROP'])\n",
        "print(f'File dibuang oleh get_score (Label Noise)      : {dropped_by_score}')\n",
        "\n",
        "df_clean = df[~df['severity_score'].astype(str).str.contains('DROP')].copy()\n",
        "df_clean['severity_score'] = df_clean['severity_score'].astype(int)\n",
        "df_clean['target_class'] = df_clean['severity_score'].apply(lambda x: 0 if x == 0 else 1)\n",
        "\n",
        "output_csv = 'master_dataset_dyslexia.csv'\n",
        "df_clean.to_csv(output_csv, index=False)\n",
        "\n",
        "print(f'\\nSUCCESS! Disimpan ke \\'{output_csv}\\' sebanyak {len(df_clean):,} file gambar bersih.')\n",
        "df_clean.sample(5)"
    ],
    "outputs": [],
    "execution_count": None
}

# ============================================================
# SAVE
# ============================================================
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Notebook berhasil diperbarui!")
print(f"  Cell 11 (Markdown Tahap 3): Dokumentasi filter ditambahkan")
print(f"  Cell 12 (Code Tahap 3): Filter eksplisit regex ditambahkan")
print(f"  Total sel: {len(nb['cells'])}")
