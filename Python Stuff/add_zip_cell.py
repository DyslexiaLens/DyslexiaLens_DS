import json

with open('notebooks/Dyslexia_EMNIST.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'].append({
    "cell_type": "markdown", "metadata": {},
    "source": ["---\n", "## Kompresi Dataset\n",
               "Kompilasi folder `Dataset/Gambo_EMNIST` menjadi `.zip` agar mudah dibagikan kepada kolega."]
})

nb['cells'].append({
    "cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
    "source": [
        "import shutil\n",
        "import os\n",
        "\n",
        "folder_to_zip = 'Dataset/Gambo_EMNIST'\n",
        "output_zip = 'Dataset_Gambo_EMNIST'\n",
        "\n",
        "if os.path.exists(folder_to_zip):\n",
        "    print(f'Mengompresi {folder_to_zip} menjadi {output_zip}.zip...')\n",
        "    shutil.make_archive(output_zip, 'zip', folder_to_zip)\n",
        "    zip_size = os.path.getsize(f'{output_zip}.zip') / (1024**3)\n",
        "    print(f'Selesai! Ukuran: {zip_size:.2f} GB')\n",
        "else:\n",
        "    print(f'Folder {folder_to_zip} tidak ditemukan!')"
    ]
})

with open('notebooks/Dyslexia_EMNIST.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
print('Cell kompresi berhasil ditambahkan.')
