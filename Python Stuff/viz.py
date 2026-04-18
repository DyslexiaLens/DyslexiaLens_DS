import os
from PIL import Image

def viz(path, count=2):
    files = os.listdir(path)[:count]
    chars = ['@', ' ']
    for f in files:
        print(f"\n--- {f} ---")
        img = Image.open(os.path.join(path, f)).convert('L')
        w, h = img.size
        for y in range(h):
            row = ''.join(chars[0] if img.getpixel((x,y)) < 128 else chars[1] for x in range(w))
            print(row)

if __name__ == '__main__':
    viz(r'Gambo_Processed\4\Corrected', 2)
    viz(r'Gambo_Processed\b\Reversal', 2)
    viz(r'Gambo_Processed\A\Normal', 2)
