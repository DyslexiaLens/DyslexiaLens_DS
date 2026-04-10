"""
preprocessing.py
=================
Pipeline preprocessing gambar tulisan tangan untuk DysRead Helper.
Dirancang untuk menjaga fitur visual disleksia selama transformasi.

Usage:
    from src.preprocessing import preprocess_for_cnn, batch_preprocess

    # Single image
    result = preprocess_for_cnn("path/to/image.png")
    tensor = result['tensor']   # shape: (128, 128, 1), range [0, 1]

    # Batch
    stats = batch_preprocess("raw/dyslexia_kaggle/", "processed/train/dyslexic/")
"""

import cv2
import numpy as np
from skimage.morphology import skeletonize
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import logging
import yaml

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════
# KONFIGURASI DEFAULT
# ═══════════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    'target_size': (128, 128),          # Output size untuk CNN
    'blur_kernel': (3, 3),              # Kernel Gaussian blur
    'morph_kernel_size': 3,             # Kernel morfologi
    'binarize_method': 'otsu',          # 'otsu', 'sauvola', atau 'adaptive'
    'sauvola_window': 25,               # Window size untuk Sauvola
    'pad_color': 0,                     # Warna padding (hitam untuk binary-inv)
    'min_contour_area': 50,             # Min area kontour (noise filter)
    'laplacian_threshold': 100,         # Threshold blur detection
    'noise_reduction_method': 'bilateral',  # 'gaussian', 'median', 'bilateral'
}


def load_config(config_path: str = None) -> dict:
    """
    Load konfigurasi dari file YAML, fallback ke DEFAULT_CONFIG.

    Args:
        config_path: Path ke file YAML konfigurasi (opsional)

    Returns:
        dict konfigurasi preprocessing
    """
    config = DEFAULT_CONFIG.copy()
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            if user_config:
                config.update(user_config)
    return config


# ═══════════════════════════════════════════════════════════
# STEP 1: LOAD & VALIDATE
# ═══════════════════════════════════════════════════════════

def load_and_validate(
    image_path: str,
    config: dict = None
) -> Optional[np.ndarray]:
    """
    Load gambar dan validasi kualitas dasar.

    Args:
        image_path: Path ke file gambar
        config: Dict konfigurasi (opsional, gunakan DEFAULT_CONFIG)

    Returns:
        Grayscale image (np.ndarray) atau None jika gagal validasi.
    """
    if config is None:
        config = DEFAULT_CONFIG

    img = cv2.imread(image_path)
    if img is None:
        logger.warning(f"Gagal load: {image_path}")
        return None

    # Convert ke grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Blur detection via Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < config['laplacian_threshold']:
        logger.warning(
            f"Gambar terlalu buram (var={laplacian_var:.1f}): "
            f"{image_path}"
        )
        return None

    return gray


# ═══════════════════════════════════════════════════════════
# STEP 2: NOISE REDUCTION
# ═══════════════════════════════════════════════════════════

def reduce_noise(
    gray_img: np.ndarray,
    method: str = 'bilateral',
    config: dict = None
) -> np.ndarray:
    """
    Kurangi noise sambil menjaga tepi goresan.

    Args:
        gray_img: Grayscale image
        method: 'gaussian', 'median', atau 'bilateral'
        config: Dict konfigurasi (opsional)

    Returns:
        Denoised grayscale image
    """
    if config is None:
        config = DEFAULT_CONFIG

    if method == 'gaussian':
        return cv2.GaussianBlur(
            gray_img, config['blur_kernel'], 0
        )
    elif method == 'median':
        return cv2.medianBlur(gray_img, 3)
    elif method == 'bilateral':
        # Bilateral: menjaga tepi lebih baik daripada Gaussian
        return cv2.bilateralFilter(gray_img, 9, 75, 75)
    else:
        raise ValueError(f"Unknown noise reduction method: {method}")


# ═══════════════════════════════════════════════════════════
# STEP 3: BINARIZATION
# ═══════════════════════════════════════════════════════════

def binarize(
    gray_img: np.ndarray,
    method: str = 'otsu',
    config: dict = None
) -> np.ndarray:
    """
    Konversi ke biner (hitam-putih) untuk isolasi goresan.

    Methods:
        - 'otsu': Cocok untuk kontras tinggi, cahaya merata.
        - 'sauvola': Cocok untuk cahaya tidak merata (foto smartphone).
        - 'adaptive': Adaptive Gaussian thresholding.

    Args:
        gray_img: Grayscale image
        method: Metode binarisasi
        config: Dict konfigurasi (opsional)

    Returns:
        Binary image (foreground=255, background=0)
    """
    if config is None:
        config = DEFAULT_CONFIG

    if method == 'otsu':
        _, binary = cv2.threshold(
            gray_img, 0, 255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        return binary

    elif method == 'sauvola':
        from skimage.filters import threshold_sauvola
        thresh = threshold_sauvola(
            gray_img,
            window_size=config['sauvola_window']
        )
        binary = (gray_img < thresh).astype(np.uint8) * 255
        return binary

    elif method == 'adaptive':
        return cv2.adaptiveThreshold(
            gray_img, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
    else:
        raise ValueError(f"Unknown binarization method: {method}")


# ═══════════════════════════════════════════════════════════
# STEP 4: MORPHOLOGICAL CLEANING
# ═══════════════════════════════════════════════════════════

def morphological_clean(
    binary_img: np.ndarray,
    config: dict = None
) -> np.ndarray:
    """
    Bersihkan noise morfologis dan sambungkan goresan putus.

    Pipeline:
        1. Opening (erode→dilate): Hapus noise kecil
        2. Closing (dilate→erode): Sambungkan celah kecil
        3. Remove small components: Filter komponen < threshold

    Args:
        binary_img: Binary image (foreground=255)
        config: Dict konfigurasi (opsional)

    Returns:
        Cleaned binary image
    """
    if config is None:
        config = DEFAULT_CONFIG

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (config['morph_kernel_size'],) * 2
    )

    # Opening: hapus titik noise
    cleaned = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

    # Closing: sambungkan gap kecil di goresan
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

    # Filter komponen kecil (noise)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        cleaned, connectivity=8
    )

    result = np.zeros_like(cleaned)
    for i in range(1, num_labels):  # Skip background (label 0)
        if stats[i, cv2.CC_STAT_AREA] >= config['min_contour_area']:
            result[labels == i] = 255

    return result


# ═══════════════════════════════════════════════════════════
# STEP 5: SKELETONIZATION
# ═══════════════════════════════════════════════════════════

def skeletonize_strokes(binary_img: np.ndarray) -> np.ndarray:
    """
    Reduksi goresan ke skeleton 1-pixel menggunakan Zhang-Suen thinning.

    Berguna untuk analisis:
        - Stroke direction dan flow
        - Jumlah endpoint & junction (kompleksitas huruf)
        - Perbandingan topologi huruf normal vs disleksia

    CATATAN: Untuk input CNN, JANGAN gunakan skeleton.
             Skeleton hanya untuk feature extraction / EDA.

    Args:
        binary_img: Binary image (foreground=255)

    Returns:
        Skeleton image (1-pixel wide strokes, value=255)
    """
    # skimage.morphology.skeletonize expects boolean input
    bool_img = (binary_img > 0)
    skeleton = skeletonize(bool_img)
    return (skeleton.astype(np.uint8) * 255)


# ═══════════════════════════════════════════════════════════
# STEP 6: RESIZE WITH ASPECT RATIO PRESERVATION + PADDING
# ═══════════════════════════════════════════════════════════

def resize_with_padding(
    img: np.ndarray,
    target_size: Tuple[int, int] = (128, 128),
    pad_color: int = 0
) -> np.ndarray:
    """
    Resize gambar sambil menjaga aspek rasio, lalu pad ke target size.

    KRITIS: Jangan distort aspek rasio! Distorsi bisa mengubah fitur
    proporsi huruf yang penting untuk membedakan disleksia vs normal.

    Strategi:
        1. Hitung scale factor berdasarkan sisi terpanjang
        2. Resize proporsional
        3. Pad sisi terpendek (center padding)

    Args:
        img: Input image (grayscale atau binary)
        target_size: (height, width) output yang diinginkan
        pad_color: Warna padding (0=hitam untuk binary-inv images)

    Returns:
        Resized + padded image dengan shape target_size
    """
    h, w = img.shape[:2]
    target_h, target_w = target_size

    # Hitung scale factor
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Resize
    resized = cv2.resize(img, (new_w, new_h),
                         interpolation=cv2.INTER_AREA)

    # Center padding
    delta_w = target_w - new_w
    delta_h = target_h - new_h
    top = delta_h // 2
    bottom = delta_h - top
    left = delta_w // 2
    right = delta_w - left

    padded = cv2.copyMakeBorder(
        resized, top, bottom, left, right,
        cv2.BORDER_CONSTANT, value=pad_color
    )

    return padded


# ═══════════════════════════════════════════════════════════
# STEP 7: NORMALIZATION
# ═══════════════════════════════════════════════════════════

def normalize_for_cnn(img: np.ndarray) -> np.ndarray:
    """
    Normalisasi pixel ke range [0, 1] untuk CNN input.

    Args:
        img: Image dengan pixel range [0, 255]

    Returns:
        Normalized image dengan pixel range [0.0, 1.0]
    """
    return img.astype(np.float32) / 255.0


# ═══════════════════════════════════════════════════════════
# MASTER PIPELINE
# ═══════════════════════════════════════════════════════════

def preprocess_for_cnn(
    image_path: str,
    target_size: Tuple[int, int] = (128, 128),
    binarize_method: str = 'otsu',
    return_intermediate: bool = False,
    config: dict = None
) -> Optional[Dict[str, Any]]:
    """
    Pipeline preprocessing end-to-end: Raw Image → CNN-Ready Tensor.

    Args:
        image_path: Path ke gambar mentah
        target_size: Ukuran output (H, W)
        binarize_method: Metode binarisasi ('otsu', 'sauvola', 'adaptive')
        return_intermediate: Jika True, simpan hasil per step
        config: Dict konfigurasi (opsional)

    Returns:
        dict dengan key:
        - 'tensor': np.ndarray shape (H, W, 1), range [0,1] — CNN input
        - 'binary': gambar biner (untuk feature extraction)
        - 'skeleton': gambar skeleton (untuk EDA)
        - 'intermediates': dict hasil per step (opsional)

        Returns None jika gambar gagal validasi.
    """
    if config is None:
        config = DEFAULT_CONFIG

    intermediates = {}

    # Step 1: Load & Validate
    gray = load_and_validate(image_path, config)
    if gray is None:
        return None
    if return_intermediate:
        intermediates['01_grayscale'] = gray.copy()

    # Step 2: Noise Reduction
    noise_method = config.get('noise_reduction_method', 'bilateral')
    denoised = reduce_noise(gray, method=noise_method, config=config)
    if return_intermediate:
        intermediates['02_denoised'] = denoised.copy()

    # Step 3: Binarization
    binary = binarize(denoised, method=binarize_method, config=config)
    if return_intermediate:
        intermediates['03_binary'] = binary.copy()

    # Step 4: Morphological Cleaning
    cleaned = morphological_clean(binary, config)
    if return_intermediate:
        intermediates['04_cleaned'] = cleaned.copy()

    # Step 5: Skeletonization (untuk EDA, bukan CNN input)
    skeleton = skeletonize_strokes(cleaned)

    # Step 6: Resize + Padding (dari gambar bersih, bukan skeleton)
    pad_color = config.get('pad_color', 0)
    resized = resize_with_padding(cleaned, target_size, pad_color=pad_color)
    if return_intermediate:
        intermediates['05_resized'] = resized.copy()

    # Step 7: Normalize
    normalized = normalize_for_cnn(resized)

    # Reshape untuk CNN: (H, W) → (H, W, 1)
    tensor = np.expand_dims(normalized, axis=-1)

    result = {
        'tensor': tensor,           # → CNN input
        'binary': cleaned,          # → Feature extraction
        'skeleton': skeleton,       # → EDA analisis
    }

    if return_intermediate:
        result['intermediates'] = intermediates

    return result


# ═══════════════════════════════════════════════════════════
# BATCH PROCESSOR
# ═══════════════════════════════════════════════════════════

def batch_preprocess(
    input_dir: str,
    output_dir: str,
    target_size: Tuple[int, int] = (128, 128),
    binarize_method: str = 'otsu',
    save_binary: bool = False,
    save_skeleton: bool = False,
    config: dict = None
) -> Dict[str, int]:
    """
    Proses seluruh folder gambar secara batch.

    Args:
        input_dir: Path ke folder input berisi gambar mentah
        output_dir: Path ke folder output untuk tensor .npy
        target_size: Ukuran output per gambar
        binarize_method: Metode binarisasi
        save_binary: Jika True, simpan juga gambar binary ke subfolder
        save_skeleton: Jika True, simpan juga skeleton ke subfolder
        config: Dict konfigurasi (opsional)

    Returns:
        dict statistik: {'total', 'success', 'failed'}
    """
    if config is None:
        config = DEFAULT_CONFIG

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Subfolder opsional
    if save_binary:
        (output_path / 'binary').mkdir(exist_ok=True)
    if save_skeleton:
        (output_path / 'skeleton').mkdir(exist_ok=True)

    stats = {'total': 0, 'success': 0, 'failed': 0}

    # Support multiple image extensions
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tif', '*.tiff']
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(ext))

    for img_file in sorted(image_files):
        stats['total'] += 1
        result = preprocess_for_cnn(
            str(img_file), target_size, binarize_method, config=config
        )

        if result is not None:
            # Simpan tensor sebagai .npy
            npy_file = output_path / f"{img_file.stem}.npy"
            np.save(str(npy_file), result['tensor'])

            # Opsional: simpan binary
            if save_binary:
                bin_file = output_path / 'binary' / f"{img_file.stem}.png"
                cv2.imwrite(str(bin_file), result['binary'])

            # Opsional: simpan skeleton
            if save_skeleton:
                skel_file = output_path / 'skeleton' / f"{img_file.stem}.png"
                cv2.imwrite(str(skel_file), result['skeleton'])

            stats['success'] += 1
        else:
            stats['failed'] += 1

    logger.info(f"Batch preprocessing complete: {stats}")
    return stats


# ═══════════════════════════════════════════════════════════
# UTILITY: Visualisasi Pipeline Steps
# ═══════════════════════════════════════════════════════════

def visualize_pipeline(
    image_path: str,
    save_path: str = None,
    config: dict = None
) -> Optional[np.ndarray]:
    """
    Visualisasi semua tahap preprocessing dalam satu grid image.
    Berguna untuk debugging dan presentasi.

    Args:
        image_path: Path ke gambar mentah
        save_path: Path untuk menyimpan visualisasi (opsional)
        config: Dict konfigurasi (opsional)

    Returns:
        Grid image (np.ndarray) atau None jika gagal
    """
    result = preprocess_for_cnn(
        image_path, return_intermediate=True, config=config
    )
    if result is None:
        return None

    intermediates = result['intermediates']
    skeleton = result['skeleton']

    # Kumpulkan semua step images
    steps = []
    titles = []
    for key in sorted(intermediates.keys()):
        steps.append(intermediates[key])
        titles.append(key)

    # Tambahkan skeleton
    steps.append(skeleton)
    titles.append('06_skeleton')

    # Tentukan grid layout
    n = len(steps)
    cols = min(3, n)
    rows = (n + cols - 1) // cols

    # Resize semua ke ukuran seragam untuk grid
    cell_h, cell_w = 200, 300
    grid_h = rows * (cell_h + 30)  # +30 untuk label
    grid_w = cols * cell_w
    grid = np.ones((grid_h, grid_w), dtype=np.uint8) * 240

    for i, (step_img, title) in enumerate(zip(steps, titles)):
        row = i // cols
        col = i % cols
        y = row * (cell_h + 30)
        x = col * cell_w

        # Resize step image ke cell size
        resized = cv2.resize(step_img, (cell_w - 10, cell_h - 10))
        grid[y+25:y+25+cell_h-10, x+5:x+5+cell_w-10] = resized

        # Tambah label
        cv2.putText(
            grid, title, (x + 5, y + 18),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1
        )

    if save_path:
        cv2.imwrite(save_path, grid)

    return grid


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"Processing: {image_path}")

        result = preprocess_for_cnn(image_path, return_intermediate=True)
        if result:
            print(f"  Tensor shape: {result['tensor'].shape}")
            print(f"  Tensor range: [{result['tensor'].min():.3f}, {result['tensor'].max():.3f}]")
            print(f"  Binary shape: {result['binary'].shape}")
            print(f"  Skeleton shape: {result['skeleton'].shape}")

            vis = visualize_pipeline(image_path, save_path='pipeline_vis.png')
            if vis is not None:
                print(f"  Visualization saved: pipeline_vis.png")
        else:
            print("  FAILED: Image did not pass validation.")
    else:
        print("Usage: python preprocessing.py <image_path>")
