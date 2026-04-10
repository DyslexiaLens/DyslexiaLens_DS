"""
feature_extraction.py
======================
Ekstraksi fitur kuantitatif dari gambar tulisan tangan
untuk EDA dan analisis statistik disleksia.

Fitur dikelompokkan dalam 3 kategori:
    A. Character-level: aspect ratio, rotation, stroke width, skeleton complexity
    B. Word/Line-level: spacing CV, baseline deviation, slant consistency
    C. Page-level: line straightness, density uniformity, ink ratio

Usage:
    from src.feature_extraction import extract_all_features

    features = extract_all_features(binary_image)
    # Returns dict of numeric features for EDA/ML
"""

import cv2
import numpy as np
from scipy import stats
from scipy.ndimage import distance_transform_edt
from skimage.morphology import skeletonize
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════

@dataclass
class HandwritingFeatures:
    """Container untuk semua fitur terukur satu sampel tulisan tangan."""

    # ── Character-level features ──
    char_count: int                     # Jumlah karakter terdeteksi
    char_aspect_ratio_mean: float       # Mean aspek rasio huruf
    char_aspect_ratio_var: float        # Variance aspek rasio huruf
    char_rotation_mean: float           # Mean sudut rotasi huruf
    char_rotation_std: float            # Std deviasi rotasi huruf
    stroke_width_mean: float            # Mean tebal goresan
    stroke_width_std: float             # Std tebal goresan
    stroke_width_cv: float              # CV tebal goresan
    skeleton_endpoints: int             # Jumlah endpoint skeleton
    skeleton_junctions: int             # Jumlah junction skeleton

    # ── Word/Line-level features ──
    inter_char_spacing_mean: float      # Mean spasi antar huruf
    inter_char_spacing_cv: float        # CV spasi antar huruf
    baseline_rmse: float                # RMSE deviasi baseline
    baseline_slope: float               # Slope garis baseline (derajat)
    slant_angle_mean: float             # Mean sudut kemiringan
    slant_angle_std: float              # Std sudut kemiringan

    # ── Page-level features ──
    line_straightness: float            # Skor kelurusan baris
    density_uniformity: float           # Uniformitas kepadatan
    ink_ratio: float                    # Rasio tinta (pixel hitam / total)
    ink_ratio_cv: float                 # CV rasio tinta per region
    contour_area_cv: float              # CV luas area kontour

    def to_dict(self) -> dict:
        """Konversi ke dictionary untuk pandas DataFrame."""
        return asdict(self)


# ═══════════════════════════════════════════════════════════
# CHARACTER SEGMENTATION
# ═══════════════════════════════════════════════════════════

def extract_character_bboxes(
    binary_img: np.ndarray,
    min_area: int = 20,
    max_area: int = None
) -> List[dict]:
    """
    Segmentasi huruf individual dari gambar baris teks.

    Args:
        binary_img: Binary image (foreground=255, background=0)
        min_area: Minimum contour area (filter noise kecil)
        max_area: Maximum contour area (filter blok besar, opsional)

    Returns:
        List of dict per karakter, sorted kiri ke kanan:
        - 'bbox': (x, y, w, h)
        - 'contour': np.ndarray
        - 'center': (cx, cy)
        - 'area': float
        - 'crop': np.ndarray (cropped char image)
    """
    if max_area is None:
        max_area = binary_img.shape[0] * binary_img.shape[1] * 0.5

    contours, _ = cv2.findContours(
        binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    chars = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)

        if min_area <= area <= max_area and w > 3 and h > 3:
            chars.append({
                'bbox': (x, y, w, h),
                'contour': cnt,
                'center': (x + w // 2, y + h // 2),
                'area': area,
                'crop': binary_img[y:y+h, x:x+w].copy(),
            })

    # Sort kiri ke kanan (reading order)
    chars.sort(key=lambda c: c['bbox'][0])
    return chars


# ═══════════════════════════════════════════════════════════
# KATEGORI A: CHARACTER-LEVEL FEATURES
# ═══════════════════════════════════════════════════════════

def compute_aspect_ratio_features(chars: List[dict]) -> dict:
    """
    Hitung statistik aspek rasio (width/height) karakter.

    Hipotesis: Anak disleksia menunjukkan variance aspek rasio
    yang lebih tinggi (ukuran huruf tidak konsisten).
    """
    if not chars:
        return {
            'char_aspect_ratio_mean': 0.0,
            'char_aspect_ratio_var': 0.0,
        }

    ratios = [c['bbox'][2] / max(c['bbox'][3], 1) for c in chars]
    return {
        'char_aspect_ratio_mean': float(np.mean(ratios)),
        'char_aspect_ratio_var': float(np.var(ratios)),
    }


def compute_rotation_features(chars: List[dict]) -> dict:
    """
    Hitung statistik sudut rotasi huruf menggunakan fitEllipse.

    Hipotesis: Disleksia menunjukkan distribusi sudut rotasi
    yang lebih lebar (huruf miring tidak konsisten).
    """
    angles = []
    for c in chars:
        if len(c['contour']) >= 5:
            try:
                _, _, angle = cv2.fitEllipse(c['contour'])
                angles.append(angle)
            except cv2.error:
                continue

    if not angles:
        return {
            'char_rotation_mean': 0.0,
            'char_rotation_std': 0.0,
        }

    return {
        'char_rotation_mean': float(np.mean(angles)),
        'char_rotation_std': float(np.std(angles)),
    }


def compute_stroke_features(binary_img: np.ndarray) -> dict:
    """
    Hitung fitur stroke (goresan) menggunakan distance transform.

    Metode: Distance transform memberikan jarak setiap pixel
    ke edge terdekat. Nilai pada medial axis (skeleton) = stroke width / 2.

    Hipotesis: Disleksia menunjukkan CV stroke width lebih tinggi
    (tekanan pena tidak stabil / kontrol motorik lemah).
    """
    if binary_img.sum() == 0:
        return {
            'stroke_width_mean': 0.0,
            'stroke_width_std': 0.0,
            'stroke_width_cv': 0.0,
        }

    # Distance transform: setiap foreground pixel = jarak ke background
    dist = distance_transform_edt(binary_img > 0)

    # Skeleton sebagai medial axis
    skel = skeletonize(binary_img > 0)

    # Stroke width = 2 * distance values di skeleton
    stroke_widths = dist[skel] * 2.0

    if len(stroke_widths) == 0:
        return {
            'stroke_width_mean': 0.0,
            'stroke_width_std': 0.0,
            'stroke_width_cv': 0.0,
        }

    mean_sw = float(np.mean(stroke_widths))
    std_sw = float(np.std(stroke_widths))
    cv = std_sw / mean_sw if mean_sw > 0 else 0.0

    return {
        'stroke_width_mean': mean_sw,
        'stroke_width_std': std_sw,
        'stroke_width_cv': cv,
    }


def compute_skeleton_complexity(binary_img: np.ndarray) -> dict:
    """
    Hitung kompleksitas topologi skeleton: endpoints dan junctions.

    - Endpoint: pixel skeleton dengan hanya 1 neighbor
    - Junction: pixel skeleton dengan 3+ neighbors

    Hipotesis: Disleksia mungkin menunjukkan skeleton complexity
    yang lebih rendah (formasi huruf simplified/kurang detail).
    """
    if binary_img.sum() == 0:
        return {
            'skeleton_endpoints': 0,
            'skeleton_junctions': 0,
        }

    skel = skeletonize(binary_img > 0).astype(np.uint8)

    # Hitung jumlah neighbor untuk setiap pixel skeleton
    # menggunakan convolution dengan kernel 3x3
    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 0  # Jangan hitung diri sendiri
    neighbor_count = cv2.filter2D(skel, -1, kernel)

    # Endpoints: exactly 1 neighbor
    endpoints = int(np.sum((skel == 1) & (neighbor_count == 1)))

    # Junctions: 3 or more neighbors
    junctions = int(np.sum((skel == 1) & (neighbor_count >= 3)))

    return {
        'skeleton_endpoints': endpoints,
        'skeleton_junctions': junctions,
    }


# ═══════════════════════════════════════════════════════════
# KATEGORI B: WORD/LINE-LEVEL FEATURES
# ═══════════════════════════════════════════════════════════

def compute_spacing_features(chars: List[dict]) -> dict:
    """
    Hitung fitur spasi antar huruf.

    Coefficient of Variation (CV) = std/mean — mengukur
    konsistensi relatif spasi.

    Hipotesis: CV tinggi = spasi tidak konsisten → indikasi disleksia.
    """
    if len(chars) < 2:
        return {
            'inter_char_spacing_mean': 0.0,
            'inter_char_spacing_cv': 0.0,
        }

    spacings = []
    for i in range(1, len(chars)):
        # Jarak antara sisi kanan karakter sebelumnya dan kiri berikutnya
        x1_right = chars[i-1]['bbox'][0] + chars[i-1]['bbox'][2]
        x2_left = chars[i]['bbox'][0]
        spacings.append(x2_left - x1_right)

    spacings = np.array(spacings, dtype=np.float64)
    mean_sp = np.mean(spacings)
    std_sp = np.std(spacings)

    # Hindari division by zero
    cv = std_sp / abs(mean_sp) if abs(mean_sp) > 1e-6 else 0.0

    return {
        'inter_char_spacing_mean': float(mean_sp),
        'inter_char_spacing_cv': float(cv),
    }


def compute_baseline_deviation(chars: List[dict]) -> dict:
    """
    Fit garis regresi pada bottom-points karakter,
    hitung RMSE deviasi dari garis tersebut.

    Bottom-point = titik terbawah dari bounding box karakter,
    yang secara ideal berada pada baseline tulisan.

    Hipotesis: RMSE tinggi = huruf 'melompat-lompat' dari baseline
    → indikasi disleksia.
    """
    if len(chars) < 3:
        return {
            'baseline_rmse': 0.0,
            'baseline_slope': 0.0,
        }

    # Titik bawah setiap karakter
    bottom_points = [
        (c['bbox'][0] + c['bbox'][2] // 2,   # x center
         c['bbox'][1] + c['bbox'][3])          # y bottom
        for c in chars
    ]

    x_coords = np.array([p[0] for p in bottom_points], dtype=np.float64)
    y_coords = np.array([p[1] for p in bottom_points], dtype=np.float64)

    # Linear regression
    slope, intercept, _, _, _ = stats.linregress(x_coords, y_coords)

    # Predicted y values
    y_pred = slope * x_coords + intercept

    # RMSE deviasi dari garis baseline
    rmse = float(np.sqrt(np.mean((y_coords - y_pred) ** 2)))

    # Konversi slope ke derajat
    slope_degrees = float(np.degrees(np.arctan(slope)))

    return {
        'baseline_rmse': rmse,
        'baseline_slope': slope_degrees,
    }


def compute_slant_features(chars: List[dict]) -> dict:
    """
    Hitung sudut kemiringan (slant) menggunakan minAreaRect.

    Hipotesis: Disleksia menunjukkan std kemiringan lebih tinggi
    (huruf miring ke arah berbeda-beda dalam satu baris).
    """
    slant_angles = []
    for c in chars:
        if len(c['contour']) >= 5:
            try:
                rect = cv2.minAreaRect(c['contour'])
                angle = rect[2]
                # Normalisasi angle ke range [-45, 45]
                if angle < -45:
                    angle += 90
                slant_angles.append(angle)
            except cv2.error:
                continue

    if not slant_angles:
        return {
            'slant_angle_mean': 0.0,
            'slant_angle_std': 0.0,
        }

    return {
        'slant_angle_mean': float(np.mean(slant_angles)),
        'slant_angle_std': float(np.std(slant_angles)),
    }


# ═══════════════════════════════════════════════════════════
# KATEGORI C: PAGE-LEVEL FEATURES
# ═══════════════════════════════════════════════════════════

def compute_line_straightness(chars: List[dict]) -> dict:
    """
    Ukur seberapa lurus baris tulisan.

    Metode: RMSE antara center-of-mass setiap karakter
    dan garis regresi yang fit ke pusat-pusat tersebut.

    Skor rendah = baris lebih berliku → indikasi disleksia.
    """
    if len(chars) < 3:
        return {'line_straightness': 1.0}

    centers_x = np.array([c['center'][0] for c in chars], dtype=np.float64)
    centers_y = np.array([c['center'][1] for c in chars], dtype=np.float64)

    slope, intercept, _, _, _ = stats.linregress(centers_x, centers_y)
    y_pred = slope * centers_x + intercept

    rmse = np.sqrt(np.mean((centers_y - y_pred) ** 2))

    # Normalize ke skor 0-1 (1 = sangat lurus)
    max_deviation = np.ptp(centers_y) if np.ptp(centers_y) > 0 else 1.0
    straightness = max(0.0, 1.0 - rmse / max_deviation)

    return {'line_straightness': float(straightness)}


def compute_density_features(
    binary_img: np.ndarray,
    grid_size: int = 4
) -> dict:
    """
    Bagi gambar jadi grid, hitung variance pixel density per sel.

    Hipotesis: Variance tinggi = kepadatan tulisan sangat fluktuatif
    → indikasi disleksia.

    Args:
        binary_img: Binary image
        grid_size: Jumlah divisi per sisi (4 = 16 sel grid)
    """
    h, w = binary_img.shape[:2]
    cell_h = max(1, h // grid_size)
    cell_w = max(1, w // grid_size)

    densities = []
    for i in range(grid_size):
        for j in range(grid_size):
            y1 = i * cell_h
            y2 = min((i + 1) * cell_h, h)
            x1 = j * cell_w
            x2 = min((j + 1) * cell_w, w)

            cell = binary_img[y1:y2, x1:x2]
            cell_area = cell.shape[0] * cell.shape[1]

            if cell_area > 0:
                density = np.sum(cell > 0) / cell_area
                densities.append(density)

    if not densities:
        return {'density_uniformity': 0.0}

    # CV sebagai ukuran (in)uniformity
    mean_d = np.mean(densities)
    std_d = np.std(densities)
    uniformity = 1.0 - (std_d / mean_d if mean_d > 0 else 0.0)

    return {'density_uniformity': float(max(0.0, uniformity))}


def compute_ink_ratio_features(binary_img: np.ndarray) -> dict:
    """
    Hitung rasio tinta (pixel foreground / total pixel).

    Juga hitung CV rasio tinta per baris horizontal
    untuk menilai konsistensi vertikal.
    """
    total_pixels = binary_img.size
    ink_pixels = np.sum(binary_img > 0)
    ink_ratio = ink_pixels / total_pixels if total_pixels > 0 else 0.0

    # CV per baris horizontal
    h = binary_img.shape[0]
    row_ratios = []
    for i in range(h):
        row = binary_img[i, :]
        row_ink = np.sum(row > 0) / max(len(row), 1)
        if row_ink > 0:
            row_ratios.append(row_ink)

    if row_ratios:
        mean_rr = np.mean(row_ratios)
        std_rr = np.std(row_ratios)
        ink_cv = std_rr / mean_rr if mean_rr > 0 else 0.0
    else:
        ink_cv = 0.0

    return {
        'ink_ratio': float(ink_ratio),
        'ink_ratio_cv': float(ink_cv),
    }


def compute_contour_area_cv(chars: List[dict]) -> dict:
    """
    CV luas area kontour karakter.

    Hipotesis: CV tinggi = ukuran huruf sangat bervariasi
    → indikasi disleksia.
    """
    if len(chars) < 2:
        return {'contour_area_cv': 0.0}

    areas = [c['area'] for c in chars]
    mean_a = np.mean(areas)
    std_a = np.std(areas)
    cv = std_a / mean_a if mean_a > 0 else 0.0

    return {'contour_area_cv': float(cv)}


# ═══════════════════════════════════════════════════════════
# MASTER EXTRACTION
# ═══════════════════════════════════════════════════════════

def extract_all_features(
    binary_img: np.ndarray,
    min_char_area: int = 20
) -> Dict[str, float]:
    """
    Ekstraksi semua fitur dari satu gambar tulisan tangan.

    Args:
        binary_img: Binary image (foreground=255, background=0)
        min_char_area: Minimum area untuk segmentasi karakter

    Returns:
        dict fitur numerik untuk EDA/ML.
        Key names match HandwritingFeatures dataclass fields.
    """
    # Segmentasi karakter
    chars = extract_character_bboxes(binary_img, min_area=min_char_area)

    features = {
        'char_count': len(chars),
    }

    # Kategori A: Character-level
    features.update(compute_aspect_ratio_features(chars))
    features.update(compute_rotation_features(chars))
    features.update(compute_stroke_features(binary_img))
    features.update(compute_skeleton_complexity(binary_img))

    # Kategori B: Word/Line-level
    features.update(compute_spacing_features(chars))
    features.update(compute_baseline_deviation(chars))
    features.update(compute_slant_features(chars))

    # Kategori C: Page-level
    features.update(compute_line_straightness(chars))
    features.update(compute_density_features(binary_img))
    features.update(compute_ink_ratio_features(binary_img))
    features.update(compute_contour_area_cv(chars))

    return features


def extract_features_batch(
    image_paths: List[str],
    labels: List[int] = None
) -> List[dict]:
    """
    Ekstraksi fitur secara batch dari multiple images.

    Args:
        image_paths: List path ke gambar binary
        labels: List label (0=non_dyslexic, 1=dyslexic), opsional

    Returns:
        List of feature dicts (siap dikonversi ke pandas DataFrame)
    """
    results = []

    for i, path in enumerate(image_paths):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            logger.warning(f"Gagal load: {path}")
            continue

        # Pastikan binary
        if img.max() > 1:
            _, img = cv2.threshold(
                img, 127, 255, cv2.THRESH_BINARY
            )

        features = extract_all_features(img)
        features['file_path'] = path
        features['file_name'] = Path(path).name

        if labels is not None and i < len(labels):
            features['label'] = labels[i]

        results.append(features)

    logger.info(f"Extracted features from {len(results)}/{len(image_paths)} images")
    return results


if __name__ == '__main__':
    import sys
    import json
    from pathlib import Path

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"Extracting features from: {image_path}")

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # Binarize jika belum
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            features = extract_all_features(binary)

            print(json.dumps(features, indent=2))
        else:
            print(f"ERROR: Cannot load {image_path}")
    else:
        print("Usage: python feature_extraction.py <binary_image_path>")
