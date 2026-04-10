# DysRead Helper — Data Card v1.0

## Dataset Overview

| Field | Value |
|-------|-------|
| **Nama** | DysRead Helper Training Dataset v1.0 |
| **Tujuan** | Early screening disleksia pada anak melalui analisis citra tulisan tangan |
| **Task** | Binary classification: `dyslexic` (1) / `non_dyslexic` (0) |
| **Pendekatan** | Vision-based (CNN) — deteksi pola kognitif, bukan OCR |

## Data Sources

| # | Sumber | Kontribusi | Lisensi | Link |
|---|--------|-----------|---------|------|
| 1 | Dyslexia Handwriting Dataset (Kaggle/Zenodo) | Primary — 3 kelas (Normal/Reversal/Corrected) | CC BY | [Kaggle](https://www.kaggle.com/) |
| 2 | Synthetic Dyslexia Handwriting Dataset (Zenodo) | Supplementary | CC BY | [Zenodo](https://zenodo.org/) |
| 3 | IAM Handwriting Database | Non-dyslexic baseline | Research only | [FKI](https://fki.tic.heia-fr.ch/) |
| 4 | Kaggle A-Z Handwritten Alphabets | Glyph source for synthetic gen | CC0 | [Kaggle](https://www.kaggle.com/) |
| 5 | Synthetic (Generated) | Augmented dyslexic samples | N/A | Generated in-house |

## Label Mapping

```
Original Dataset          →  DysRead Helper Binary Label
─────────────────────────────────────────────────────────
Normal                    →  non_dyslexic (0)
Reversal                  →  dyslexic (1)
Corrected                 →  dyslexic (1)
IAM samples               →  non_dyslexic (0)
Synthetic dyslexic        →  dyslexic (1)
```

## Dataset Statistics

> ⚠️ **Catatan:** Isi tabel ini setelah dataset final selesai dikurasi.

| Metric | Train | Validation | Test | Total |
|--------|-------|------------|------|-------|
| Non-Dyslexic | — | — | — | — |
| Dyslexic | — | — | — | — |
| **Total** | — | — | — | — |
| Imbalance Ratio | — | — | — | — |

## Preprocessing

| Step | Method | Parameter |
|------|--------|-----------|
| 1. Grayscale Conversion | `cv2.cvtColor` | BGR → GRAY |
| 2. Noise Reduction | Bilateral Filter | d=9, σColor=75, σSpace=75 |
| 3. Binarization | Otsu Thresholding | Automatic threshold |
| 4. Morphological Cleaning | Opening + Closing | Kernel 3×3 ellipse |
| 5. Component Filtering | Connected Components | min_area=50px |
| 6. Resize + Padding | Aspect-ratio preserving | 128×128, center pad |
| 7. Normalization | Min-Max | [0, 1] float32 |

## Output Format

| Field | Specification |
|-------|--------------|
| Format | NumPy arrays (.npy) |
| Shape | (128, 128, 1) |
| Dtype | float32 |
| Range | [0.0, 1.0] |
| Channel | Grayscale (1 channel) |

## Data Split

| Split | Ratio | Strategy |
|-------|-------|----------|
| Training | 70% | Stratified random |
| Validation | 15% | Stratified random |
| Test | 15% | Stratified random |

**Random Seed:** 42

## Augmentation Strategy

### Non-Dyslexic (Safe Augmentation)
- Rotation: ±5°
- Brightness/Contrast: ±15%
- Gaussian Noise: σ=0.01-0.03
- Elastic Distortion: mild (α=1, σ=50)
- Shift/Scale: ±5%

### Dyslexic (Reinforced Augmentation)
- Semua safe augmentations di atas, PLUS:
- Baseline Wave: amplitude=4px, freq=0.015
- Strong Elastic: α=2, σ=30
- Local Elastic Distortion
- Spacing Perturbation

### ⚠️ FORBIDDEN Augmentations
- **Horizontal Flip on Normal class** — bisa mengubah label!

## Known Limitations

1. **Synthetic bias** — Sampel sintetis mungkin tidak merepresentasikan semua variasi disleksia yang sebenarnya
2. **Age range** — Dataset primer dari anak SD (6-12 tahun), mungkin tidak generalize ke usia lain
3. **Language** — Mayoritas Latin script, belum ada dukungan aksara lain
4. **Clinical validation** — Belum divalidasi secara formal oleh ahli psikologi klinis

## Ethical Considerations

- Dataset berisi tulisan tangan anak-anak yang memerlukan pertimbangan privasi
- Model ini untuk **screening awal**, BUKAN diagnosis klinis
- Keputusan akhir harus selalu melibatkan profesional kesehatan
- False negative (miss dyslexic child) lebih berbahaya dari false positive

## Citation

```
Jika menggunakan dataset ini, harap cite:
- Isa, I. S., et al. (2021). "CNN Comparisons Models on Dyslexia Handwriting Classification"
- IAM Handwriting Database: Marti & Bunke (2002)
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-04-11 | Initial dataset creation |
