import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NB_PATH = r"d:\Tugas\Kuliah\Semester 6\Dicoding\Capstone Project\Dataset Disleksia\notebooks\Dyslexia_NoAugmentation.ipynb"

with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# ============================================================
# UPDATE CELL 11: Markdown Tahap 3
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
        "### Filter Pembersihan Eksplisit\n",
        "Selain filter skor, pipeline ini membuang file-file **sampah / duplikat / anomali**:\n",
        "\n",
        "| Pola File | Contoh | Alasan Dibuang |\n",
        "|---|---|---|\n",
        "| Duplikat Windows `(1)` | `Normal1305 (11).png`, `Reversal (1).png` | File hasil *copy-paste* berulang di Windows (menghindari duplikasi data) |\n",
        "| Placeholder Murni | `Normal.png`, `Reversal.png` | Bukan sampel tulisan tangan yang sesungguhnya |\n",
        "| Temporary / Glitch | `e-491.qNcy3.png` | File arsip rusak / ekstensi ganda dari *download* terputus |\n",
        "| Abjad di Disleksia | `A.png`, `b.png` | File abjad referensi murni, bukan tulisan pasien |\n",
        "| Label Noise (Normal) | `Normal123.png` di Corrected | File Normal yang terselip ke folder disleksia |\n",
        "\n",
        "> **PENTING:** Jalankan sel ini hanya SEKALI setelah Tahap 1 (dan opsional Tahap 2)."
    ]
}

# ============================================================
# UPDATE CELL 12: Code Tahap 3
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
        "SCORE_MAP_ORIGINAL = {1: 6, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}\n",
        "\n",
        "# ============================================================\n",
        "# REGEX FILTER: Pola nama file sampah\n",
        "# ============================================================\n",
        "RE_DUPLICATE_WIN = re.compile(r'\\(\\d+\\)')  # Mengandung (1), (2), (11) dsb\n",
        "RE_PLACEHOLDER = re.compile(r'^(Normal|Reversal|Corrected)\\.png$', re.IGNORECASE)\n",
        "RE_GLITCH = re.compile(r'\\.qNcy', re.IGNORECASE)  # File glitch dari donwload/ekstrak\n",
        "RE_ALPHA_ONLY = re.compile(r'^[A-Za-z]\\.png$')  # A.png, b.png\n",
        "\n",
        "print('Membaca seluruh direktori...')\n",
        "data = []\n",
        "filtered_out = {'duplicate': 0, 'placeholder': 0, 'glitch': 0, 'alpha_only': 0}\n",
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
        "        # 1. Duplikat Windows (misal: Normal1305 (11).png)\n",
        "        if RE_DUPLICATE_WIN.search(file):\n",
        "            filtered_out['duplicate'] += 1\n",
        "            continue\n",
        "            \n",
        "        # 2. Glitch File (misal: e-491.qNcy3.png)\n",
        "        if RE_GLITCH.search(file):\n",
        "            filtered_out['glitch'] += 1\n",
        "            continue\n",
        "            \n",
        "        # 3. Placeholder murni (misal: Normal.png)\n",
        "        if RE_PLACEHOLDER.match(file):\n",
        "            filtered_out['placeholder'] += 1\n",
        "            continue\n",
        "            \n",
        "        # 4. Abjad tunggal di Corrected/Reversal\n",
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
        "print(f'Total gambar bersih sementara: {len(df)} file.')\n",
        "print(f'\\n=== File Dibuang (Filter Eksplisit) ===')\n",
        "print(f'  Duplikat Windows `(X)`         : {filtered_out[\"duplicate\"]}')\n",
        "print(f'  File Glitch (`.qNcy`)          : {filtered_out[\"glitch\"]}')\n",
        "print(f'  Placeholder (Normal.png dll)   : {filtered_out[\"placeholder\"]}')\n",
        "print(f'  Abjad tunggal di Disleksia     : {filtered_out[\"alpha_only\"]}')\n",
        "print(f'  TOTAL dibuang oleh regex       : {sum(filtered_out.values())}\\n')\n",
        "\n",
        "def get_score(row):\n",
        "    filename = row['file_name']\n",
        "    folder = row['folder_category']\n",
        "    if 'Normal' in filename and folder != 'Normal': return 'DROP'\n",
        "    if folder == 'Normal': return 0\n",
        "    if folder in ['Corrected', 'Reversal']:\n",
        "        for sep in ['_', '-']:\n",
        "            if sep in filename:\n",
        "                prefix = filename.split(sep)[0]\n",
        "                if prefix.isdigit():\n",
        "                    val = int(prefix)\n",
        "                    if 1 <= val <= 6: return val\n",
        "                    elif val in SCORE_MAP_ORIGINAL: return SCORE_MAP_ORIGINAL[val]\n",
        "                break\n",
        "    return 'DROP'\n",
        "\n",
        "df['severity_score'] = df.apply(get_score, axis=1)\n",
        "dropped_by_score = len(df[df['severity_score'].astype(str) == 'DROP'])\n",
        "print(f'File dibuang oleh get_score (Label Noise / Tidak Dikenal) : {dropped_by_score}')\n",
        "\n",
        "df_clean = df[~df['severity_score'].astype(str).str.contains('DROP')].copy()\n",
        "df_clean['severity_score'] = df_clean['severity_score'].astype(int)\n",
        "df_clean['target_class'] = df_clean['severity_score'].apply(lambda x: 0 if x == 0 else 1)\n",
        "\n",
        "output_csv = 'master_dataset_dyslexia.csv'\n",
        "df_clean.to_csv(output_csv, index=False)\n",
        "print(f'\\nSUCCESS! Disimpan ke \\'{output_csv}\\' sebanyak {len(df_clean):,} file gambar bersih.')\n",
        "df_clean.sample(5)"
    ],
    "outputs": [],
    "execution_count": None
}

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Berhasil diperbarui!")
