import os
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report
import time

print("Memuat Dataset Master...")
df = pd.read_csv('master_dataset_dyslexia.csv')

# Ambil sampel kecil saja (10.000 gambar) untuk mempercepat proses Baseline
sample_train = df[df['split'] == 'Train'].sample(8000, random_state=42)
sample_test = df[df['split'] == 'Test'].sample(2000, random_state=42)

def load_images_to_arrays(df_subset, dataset_ready_dir='Dataset_Ready'):
    X, y = [], []
    for _, row in df_subset.iterrows():
        # Konstruksi path dari folder Dataset_Ready
        cls_folder = 'Normal' if row['target_class'] == 0 else 'Dyslexia'
        file_name = f"{row.get('source', '')}_{row['file_name']}"
        path = os.path.join(dataset_ready_dir, row['split'], cls_folder, file_name)
        
        # Fallback ke path asli jika folder belum selesai di-copy
        if not os.path.exists(path):
            path = row['image_path']
            
        try:
            img = Image.open(path).convert('L').resize((28,28))
            arr = np.array(img).flatten() # Flatten 28x28 menjadi 1D array (784 fitur)
            X.append(arr)
            y.append(row['target_class'])
        except:
            pass
    return np.array(X), np.array(y)

print("Memuat gambar fisik ke memori...")
start = time.time()
X_train, y_train = load_images_to_arrays(sample_train)
X_test, y_test = load_images_to_arrays(sample_test)

# Normalisasi 0-1
X_train = X_train / 255.0
X_test = X_test / 255.0

print(f"Selesai memuat {len(X_train)} Train dan {len(X_test)} Test dalam {time.time()-start:.1f} detik.")

print("\n=== MELATIH BASELINE MODEL (SGD Classifier) ===")
# SGD Classifier setara dengan Linear SVM / Regresi Logistik sangat cepat
clf = SGDClassifier(random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

print("\n=== EVALUASI MODEL BASELINE ===")
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"Validation Accuracy : {acc:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Dyslexia']))

if acc > 0.5:
    print("\n✅ SUKSES: Model Baseline Linear berhasil mengalahkan tebakan acak (Random Guess > 50%).")
    print("Meskipun akurasi mungkin masih di bawah 80%, ini wajar untuk model Linear.")
    print("Dataset ini tervalidasi bisa dipelajari. Serahkan tugas optimasi Deep Learning ke AI Engineer!")
else:
    print("\n⚠️ PERINGATAN: Model Baseline setara tebakan acak. Perlu investigasi lebih lanjut.")
