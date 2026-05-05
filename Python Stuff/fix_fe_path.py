"""Fix path assets di sel Feature Engineering notebook"""
import json

NB_PATH = 'notebooks/Dyslexia_NoAugmentation.ipynb'

with open(NB_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed = 0
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            if 'assets/feature_engineering' in line:
                line = line.replace("'assets/", "'../assets/")
                fixed += 1
            new_source.append(line)
        cell['source'] = new_source

with open(NB_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Fixed {fixed} path references.")
