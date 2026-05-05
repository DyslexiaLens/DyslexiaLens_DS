"""
Script ini menambahkan sel Feature Engineering ke dalam
notebooks/Dyslexia_NoAugmentation.ipynb (sebelum sel kompresi zip).

Fitur yang diekstrak:
  1. ink_density      - Persentase piksel hitam (goresan) terhadap total piksel
  2. center_of_mass_x - Titik tengah goresan sumbu X
  3. center_of_mass_y - Titik tengah goresan sumbu Y
  4. bounding_box_ratio - Rasio tinggi/lebar area goresan (tanpa whitespace)
  5. stroke_transitions - Jumlah transisi putih↔hitam secara horizontal
"""

import json

NB_PATH = 'notebooks/Dyslexia_NoAugmentation.ipynb'

# === Sel-sel baru yang akan disisipkan ===
new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n",
            "# Tahap 7: Feature Engineering (Side Quest)\n",
            "\n",
            "Tahap ini mengekstrak **fitur turunan matematis** dari setiap gambar 28×28 piksel.\n",
            "Alih-alih hanya menyerahkan matriks piksel mentah kepada AI Engineer, kita menghitung variabel-variabel tabular baru yang merepresentasikan **karakteristik goresan tulisan** secara numerik.\n",
            "\n",
            "Fitur ini sangat berguna jika AI Engineer ingin membangun **Multi-Input Model** (Functional API) yang menggabungkan CNN (untuk gambar) dengan Dense Layer (untuk fitur tabular) secara bersamaan.\n",
            "\n",
            "### Fitur yang Diekstrak:\n",
            "| Fitur | Deskripsi |\n",
            "|---|---|\n",
            "| `ink_density` | Persentase piksel hitam (tinta) terhadap total area gambar (784 piksel). Tulisan yang banyak dicoreng akan memiliki kepadatan tinta lebih tinggi. |\n",
            "| `center_of_mass_x` | Posisi titik tengah goresan pada sumbu horizontal (0-27). Huruf yang miring atau asimetris akan memiliki centroid yang melenceng. |\n",
            "| `center_of_mass_y` | Posisi titik tengah goresan pada sumbu vertikal (0-27). |\n",
            "| `bounding_box_ratio` | Rasio tinggi/lebar area goresan setelah whitespace dipangkas. Huruf yang direvisi berulang kali cenderung melebar (rasio < 1). |\n",
            "| `stroke_transitions` | Rata-rata jumlah transisi warna putih↔hitam per baris horizontal. Goresan berantakan memiliki transisi lebih tinggi. |"
        ]
    },
    {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "import pandas as pd\n",
            "import numpy as np\n",
            "from PIL import Image\n",
            "import os\n",
            "\n",
            "# === Konfigurasi ===\n",
            "CSV_INPUT = 'master_dataset_final.csv'  # Output dari Tahap 5\n",
            "CSV_OUTPUT = 'master_dataset_final_featured.csv'\n",
            "IMG_SIZE = 28\n",
            "THRESHOLD = 128  # Piksel < 128 = hitam (goresan), >= 128 = putih (latar)\n",
            "\n",
            "df = pd.read_csv(CSV_INPUT)\n",
            "print(f'Memuat {len(df):,} baris dari {CSV_INPUT}')\n",
            "print(f'Kolom awal: {df.columns.tolist()}')"
        ],
        "outputs": [],
        "execution_count": None
    },
    {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "def extract_features(image_path):\n",
            "    \"\"\"\n",
            "    Mengekstrak 5 fitur turunan dari satu gambar grayscale 28x28.\n",
            "    Returns dict of features, atau dict berisi NaN jika gambar error.\n",
            "    \"\"\"\n",
            "    try:\n",
            "        img = Image.open(image_path).convert('L').resize((28, 28))\n",
            "        pixels = np.array(img, dtype=np.float64)\n",
            "        binary = (pixels < THRESHOLD).astype(np.float64)  # 1 = tinta, 0 = latar\n",
            "        \n",
            "        # 1. Ink Density (kepadatan tinta)\n",
            "        total_pixels = IMG_SIZE * IMG_SIZE\n",
            "        ink_density = np.sum(binary) / total_pixels\n",
            "        \n",
            "        # 2 & 3. Center of Mass (titik tengah goresan)\n",
            "        ink_sum = np.sum(binary)\n",
            "        if ink_sum > 0:\n",
            "            y_coords, x_coords = np.where(binary == 1)\n",
            "            center_x = np.mean(x_coords)\n",
            "            center_y = np.mean(y_coords)\n",
            "        else:\n",
            "            center_x, center_y = IMG_SIZE / 2, IMG_SIZE / 2\n",
            "        \n",
            "        # 4. Bounding Box Ratio (rasio tinggi/lebar area goresan)\n",
            "        if ink_sum > 0:\n",
            "            rows_with_ink = np.any(binary, axis=1)\n",
            "            cols_with_ink = np.any(binary, axis=0)\n",
            "            height = np.sum(rows_with_ink)\n",
            "            width = np.sum(cols_with_ink)\n",
            "            bbox_ratio = height / max(width, 1)\n",
            "        else:\n",
            "            bbox_ratio = 1.0\n",
            "        \n",
            "        # 5. Stroke Transitions (rata-rata transisi putih-hitam per baris)\n",
            "        transitions = 0\n",
            "        for row in binary:\n",
            "            diffs = np.abs(np.diff(row))\n",
            "            transitions += np.sum(diffs)\n",
            "        stroke_transitions = transitions / IMG_SIZE\n",
            "        \n",
            "        return {\n",
            "            'ink_density': round(ink_density, 6),\n",
            "            'center_of_mass_x': round(center_x, 4),\n",
            "            'center_of_mass_y': round(center_y, 4),\n",
            "            'bounding_box_ratio': round(bbox_ratio, 4),\n",
            "            'stroke_transitions': round(stroke_transitions, 4)\n",
            "        }\n",
            "    except Exception as e:\n",
            "        return {\n",
            "            'ink_density': np.nan,\n",
            "            'center_of_mass_x': np.nan,\n",
            "            'center_of_mass_y': np.nan,\n",
            "            'bounding_box_ratio': np.nan,\n",
            "            'stroke_transitions': np.nan\n",
            "        }\n",
            "\n",
            "print('Fungsi extract_features() siap digunakan.')"
        ],
        "outputs": [],
        "execution_count": None
    },
    {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# === Eksekusi Feature Extraction ===\n",
            "features_list = []\n",
            "errors = 0\n",
            "\n",
            "for i, row in df.iterrows():\n",
            "    img_path = row['image_path']\n",
            "    features = extract_features(img_path)\n",
            "    features_list.append(features)\n",
            "    \n",
            "    if np.isnan(features['ink_density']):\n",
            "        errors += 1\n",
            "    \n",
            "    if (i + 1) % 20000 == 0:\n",
            "        print(f'  Processed {i+1:,}/{len(df):,}...')\n",
            "\n",
            "# Gabungkan fitur ke DataFrame utama\n",
            "df_features = pd.DataFrame(features_list)\n",
            "df_final = pd.concat([df.reset_index(drop=True), df_features], axis=1)\n",
            "\n",
            "print(f'\\n=== Hasil Feature Engineering ===')\n",
            "print(f'Kolom baru: {df_features.columns.tolist()}')\n",
            "print(f'Total baris: {len(df_final):,} | Error: {errors}')\n",
            "print(f'Shape akhir: {df_final.shape}')\n",
            "df_final.head()"
        ],
        "outputs": [],
        "execution_count": None
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 7A. Validasi Statistik Fitur Baru\n",
            "\n",
            "Memvalidasi bahwa fitur-fitur yang diekstrak memiliki **distribusi yang bermakna** dan berbeda antara kelas Normal vs Disleksia."
        ]
    },
    {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "sns.set_theme(style='whitegrid')\n",
            "\n",
            "feature_cols = ['ink_density', 'center_of_mass_x', 'center_of_mass_y', \n",
            "                'bounding_box_ratio', 'stroke_transitions']\n",
            "\n",
            "fig, axes = plt.subplots(2, 3, figsize=(16, 10))\n",
            "fig.suptitle('Distribusi Fitur Turunan: Normal vs Disleksia', fontsize=14, fontweight='bold')\n",
            "\n",
            "for idx, feat in enumerate(feature_cols):\n",
            "    ax = axes[idx // 3][idx % 3]\n",
            "    for label, color, name in [(0, '#2ECC71', 'Normal'), (1, '#E74C3C', 'Disleksia')]:\n",
            "        subset = df_final[df_final['target_class'] == label][feat].dropna()\n",
            "        ax.hist(subset, bins=40, alpha=0.6, color=color, label=name, density=True)\n",
            "    ax.set_title(feat, fontweight='bold')\n",
            "    ax.legend()\n",
            "\n",
            "# Kosongkan subplot ke-6 yang tidak terpakai\n",
            "axes[1][2].axis('off')\n",
            "plt.tight_layout()\n",
            "plt.savefig('assets/feature_engineering_distribution.png', dpi=150, bbox_inches='tight')\n",
            "plt.show()\n",
            "print('Grafik distribusi fitur tersimpan di assets/feature_engineering_distribution.png')"
        ],
        "outputs": [],
        "execution_count": None
    },
    {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# === Ringkasan Statistik per Kelas ===\n",
            "print('=== Rata-rata Fitur per Kelas ===')\n",
            "summary = df_final.groupby('target_class')[feature_cols].mean()\n",
            "summary.index = ['Normal (0)', 'Disleksia (1)']\n",
            "print(summary.round(4).to_string())\n",
            "\n",
            "print('\\n=== Selisih Absolut (Disleksia - Normal) ===')\n",
            "diff = summary.loc['Disleksia (1)'] - summary.loc['Normal (0)']\n",
            "print(diff.round(4).to_string())\n",
            "print('\\nFitur dengan selisih terbesar menunjukkan potensi diskriminatif tertinggi untuk model AI.')"
        ],
        "outputs": [],
        "execution_count": None
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 7B. Simpan Dataset Final + Fitur Turunan"
        ]
    },
    {
        "cell_type": "code",
        "metadata": {},
        "source": [
            "# === Simpan CSV dengan kolom fitur baru ===\n",
            "df_final.to_csv(CSV_OUTPUT, index=False)\n",
            "print(f'Dataset tersimpan: {CSV_OUTPUT}')\n",
            "print(f'Kolom final: {df_final.columns.tolist()}')\n",
            "print(f'Total baris: {len(df_final):,}')\n",
            "print(f'\\nData Dictionary Fitur Baru:')\n",
            "print('  ink_density        : Kepadatan tinta (0.0-1.0). Semakin tinggi = semakin banyak coretan.')\n",
            "print('  center_of_mass_x   : Titik tengah goresan sumbu-X (0-27). Menyimpang = asimetris.')\n",
            "print('  center_of_mass_y   : Titik tengah goresan sumbu-Y (0-27).')\n",
            "print('  bounding_box_ratio : Rasio tinggi/lebar bounding box goresan. <1 = melebar, >1 = memanjang.')\n",
            "print('  stroke_transitions : Rata-rata transisi warna per baris. Tinggi = goresan berantakan.')"
        ],
        "outputs": [],
        "execution_count": None
    }
]

# === Sisipkan sel-sel baru ke notebook ===
with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Sisipkan SEBELUM sel kompresi zip (index 56 = markdown "Kompresi Dataset")
insert_idx = 56
for i, cell in enumerate(new_cells):
    nb['cells'].insert(insert_idx + i, cell)

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Berhasil menyisipkan {len(new_cells)} sel Feature Engineering ke {NB_PATH}")
print(f"Total sel sekarang: {len(nb['cells'])}")
