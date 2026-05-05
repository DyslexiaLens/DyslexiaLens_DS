import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/Dyslexia_NoAugmentation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:120].replace('\n', ' ').encode('ascii', 'replace').decode()
    print(f"  [{i}] {c['cell_type']}: {src}")
