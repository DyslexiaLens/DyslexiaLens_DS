"""
augmentation.py
================
Pipeline augmentasi untuk DysRead Helper.
Mengimplementasikan strategi label-safe dan label-reinforcing.

PRINSIP EMAS:
    Augmentasi TIDAK BOLEH menambah atau menghapus ciri disleksia.
    Contoh BERBAHAYA: horizontal flip pada huruf Normal bisa
    membuatnya terlihat seperti Reversal → label menjadi salah!

Strategi:
    1. safe_augmentation — Aman untuk kedua kelas
    2. dyslexic_reinforcement — Memperkuat pola disleksia (hanya kelas dyslexic)
    3. get_augmentation_pipeline() — Auto-select berdasarkan label

Usage:
    from src.augmentation import get_augmentation_pipeline

    pipeline = get_augmentation_pipeline('dyslexic')
    augmented = pipeline(image=image)['image']
"""

import cv2
import numpy as np
import albumentations as A
from albumentations.core.transforms_interface import ImageOnlyTransform
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# CUSTOM TRANSFORMS
# ═══════════════════════════════════════════════════════════

class BaselineWave(ImageOnlyTransform):
    """
    Tambahkan undulasi sinusoidal ke baseline tulisan.

    Mensimulasikan efek baseline drift yang sering terlihat
    pada tulisan anak disleksia — huruf 'bergelombang'
    mengikuti garis yang tidak lurus.

    Args:
        amplitude: Amplitudo gelombang dalam pixel
        frequency: Frekuensi gelombang (cycles per pixel)
    """

    def __init__(
        self,
        amplitude: int = 5,
        frequency: float = 0.02,
        always_apply: bool = False,
        p: float = 0.5
    ):
        super().__init__(always_apply, p)
        self.amplitude = amplitude
        self.frequency = frequency

    def apply(self, img: np.ndarray, **params) -> np.ndarray:
        """Apply baseline wave transformation."""
        rows, cols = img.shape[:2]
        result = np.zeros_like(img)

        # Randomize phase untuk variasi
        phase = np.random.uniform(0, 2 * np.pi)

        for y in range(rows):
            shift_x = int(
                self.amplitude * np.sin(
                    2 * np.pi * self.frequency * y + phase
                )
            )
            if shift_x >= 0:
                if shift_x < cols:
                    result[y, shift_x:] = img[y, :cols - shift_x]
            else:
                abs_shift = abs(shift_x)
                if abs_shift < cols:
                    result[y, :cols - abs_shift] = img[y, abs_shift:]

        return result

    def get_transform_init_args_names(self):
        return ("amplitude", "frequency")


class LocalElasticDistortion(ImageOnlyTransform):
    """
    Elastic distortion yang diterapkan hanya pada region
    tertentu dari gambar, bukan global.

    Mensimulasikan tremor lokal pada huruf-huruf tertentu,
    bukan seluruh baris tulisan.
    """

    def __init__(
        self,
        alpha: float = 2.0,
        sigma: float = 30.0,
        region_ratio: float = 0.4,
        always_apply: bool = False,
        p: float = 0.5
    ):
        super().__init__(always_apply, p)
        self.alpha = alpha
        self.sigma = sigma
        self.region_ratio = region_ratio

    def apply(self, img: np.ndarray, **params) -> np.ndarray:
        """Apply local elastic distortion to random region."""
        rows, cols = img.shape[:2]
        result = img.copy()

        # Pilih region random
        region_w = int(cols * self.region_ratio)
        region_h = rows
        x_start = np.random.randint(0, max(1, cols - region_w))

        # Apply elastic transform hanya di region
        region = img[:region_h, x_start:x_start + region_w]

        rr, rc = region.shape[:2]
        dx = np.random.uniform(-1, 1, (rr, rc)).astype(np.float32) * self.alpha
        dy = np.random.uniform(-1, 1, (rr, rc)).astype(np.float32) * self.alpha

        # Gaussian blur untuk smoothness
        k = int(self.sigma) * 2 + 1
        if k % 2 == 0:
            k += 1
        dx = cv2.GaussianBlur(dx, (k, k), self.sigma)
        dy = cv2.GaussianBlur(dy, (k, k), self.sigma)

        x, y = np.meshgrid(np.arange(rc), np.arange(rr))
        map_x = (x + dx).astype(np.float32)
        map_y = (y + dy).astype(np.float32)

        distorted = cv2.remap(
            region, map_x, map_y, cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT, borderValue=0
        )

        result[:region_h, x_start:x_start + region_w] = distorted
        return result

    def get_transform_init_args_names(self):
        return ("alpha", "sigma", "region_ratio")


class SpacingPerturbation(ImageOnlyTransform):
    """
    Menerapkan perturbasi spasi lokal pada tulisan.

    Menggeser kolom pixel secara random untuk mensimulasikan
    spasi antar huruf yang tidak konsisten.
    """

    def __init__(
        self,
        max_shift: int = 5,
        segment_width: int = 20,
        always_apply: bool = False,
        p: float = 0.5
    ):
        super().__init__(always_apply, p)
        self.max_shift = max_shift
        self.segment_width = segment_width

    def apply(self, img: np.ndarray, **params) -> np.ndarray:
        """Apply spacing perturbation."""
        rows, cols = img.shape[:2]
        result = np.zeros_like(img)

        x = 0
        dest_x = 0
        while x < cols:
            seg_w = min(self.segment_width, cols - x)
            shift = np.random.randint(-self.max_shift, self.max_shift + 1)

            dest_start = max(0, dest_x + shift)
            dest_end = min(cols, dest_start + seg_w)
            src_end = min(cols, x + (dest_end - dest_start))

            if dest_start < dest_end and x < src_end:
                actual_w = min(dest_end - dest_start, src_end - x)
                result[:, dest_start:dest_start + actual_w] = img[:, x:x + actual_w]

            x += seg_w
            dest_x += seg_w

        return result

    def get_transform_init_args_names(self):
        return ("max_shift", "segment_width")


# ═══════════════════════════════════════════════════════════
# AUGMENTASI AMAN (Label-Safe — kedua kelas)
# ═══════════════════════════════════════════════════════════

safe_augmentation = A.Compose([
    # Rotasi ringan — variasi natural posisi kertas
    A.Rotate(
        limit=5,
        border_mode=cv2.BORDER_CONSTANT,
        value=0,
        p=0.5
    ),

    # Variasi pencahayaan — simulasi kondisi foto berbeda
    A.RandomBrightnessContrast(
        brightness_limit=0.15,
        contrast_limit=0.15,
        p=0.4
    ),

    # Noise kamera
    A.GaussNoise(
        var_limit=(10, 50),
        p=0.3
    ),

    # Elastic distortion RINGAN — variasi natural tulisan tangan
    A.ElasticTransform(
        alpha=1,
        sigma=50,
        p=0.3,
        border_mode=cv2.BORDER_CONSTANT,
        value=0
    ),

    # Shift dan scale ringan — variasi posisi scan/foto
    A.ShiftScaleRotate(
        shift_limit=0.05,
        scale_limit=0.05,
        rotate_limit=0,  # Rotasi sudah di atas
        border_mode=cv2.BORDER_CONSTANT,
        value=0,
        p=0.3
    ),

    # Simulasi kompresi JPEG (jika user upload foto)
    A.ImageCompression(
        quality_lower=70,
        quality_upper=95,
        p=0.2
    ),
])


# ═══════════════════════════════════════════════════════════
# AUGMENTASI PENGUAT DISLEKSIA (Label-Reinforcing — hanya dyslexic)
# ═══════════════════════════════════════════════════════════

dyslexic_reinforcement = A.Compose([
    # ── Baseline safe augmentations terlebih dahulu ──
    A.Rotate(
        limit=5,
        border_mode=cv2.BORDER_CONSTANT,
        value=0,
        p=0.5
    ),
    A.RandomBrightnessContrast(
        brightness_limit=0.15,
        contrast_limit=0.15,
        p=0.4
    ),
    A.GaussNoise(
        var_limit=(10, 50),
        p=0.3
    ),

    # ── Augmentasi penguat pola disleksia ──

    # Baseline wave — memperkuat efek huruf bergelombang
    BaselineWave(amplitude=4, frequency=0.015, p=0.4),

    # Elastic distortion KUAT — memperkuat stroke tremor
    A.ElasticTransform(
        alpha=2,
        sigma=30,
        p=0.4,
        border_mode=cv2.BORDER_CONSTANT,
        value=0
    ),

    # Local elastic distortion — tremor pada region tertentu
    LocalElasticDistortion(alpha=2.5, sigma=25, region_ratio=0.3, p=0.35),

    # Spacing perturbation — memperkuat spasi tidak konsisten
    SpacingPerturbation(max_shift=4, segment_width=15, p=0.35),

    # Perspective transform ringan
    A.Perspective(scale=(0.02, 0.05), p=0.3),
])


# ═══════════════════════════════════════════════════════════
# PIPELINE SELECTOR
# ═══════════════════════════════════════════════════════════

def get_augmentation_pipeline(label: str) -> A.Compose:
    """
    Return pipeline augmentasi yang tepat berdasarkan label kelas.

    Args:
        label: 'dyslexic' atau 'non_dyslexic'

    Returns:
        albumentations.Compose pipeline

    Raises:
        ValueError: Jika label tidak dikenali
    """
    if label == 'dyslexic':
        return dyslexic_reinforcement
    elif label == 'non_dyslexic':
        return safe_augmentation
    else:
        raise ValueError(
            f"Unknown label: '{label}'. "
            f"Expected 'dyslexic' or 'non_dyslexic'"
        )


# ═══════════════════════════════════════════════════════════
# BATCH AUGMENTATION
# ═══════════════════════════════════════════════════════════

def augment_batch(
    images: list,
    labels: list,
    n_augments: int = 3
) -> tuple:
    """
    Augmentasi batch gambar dengan pipeline yang tepat per label.

    Args:
        images: List np.ndarray gambar
        labels: List label string ('dyslexic' / 'non_dyslexic')
        n_augments: Jumlah augmentasi per gambar

    Returns:
        Tuple (augmented_images, augmented_labels)
    """
    aug_images = []
    aug_labels = []

    for img, label in zip(images, labels):
        pipeline = get_augmentation_pipeline(label)

        # Keep original
        aug_images.append(img)
        aug_labels.append(label)

        # Generate augmented versions
        for _ in range(n_augments):
            augmented = pipeline(image=img)['image']
            aug_images.append(augmented)
            aug_labels.append(label)

    logger.info(
        f"Augmented batch: {len(images)} → {len(aug_images)} images"
    )
    return aug_images, aug_labels


def augment_directory(
    input_dir: str,
    output_dir: str,
    label: str,
    n_augments: int = 3
) -> dict:
    """
    Augmentasi semua gambar dalam folder.

    Args:
        input_dir: Folder input berisi gambar
        output_dir: Folder output untuk gambar augmented
        label: 'dyslexic' atau 'non_dyslexic'
        n_augments: Jumlah augmentasi per gambar

    Returns:
        dict statistik
    """
    from pathlib import Path
    import shutil

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pipeline = get_augmentation_pipeline(label)
    stats = {'total': 0, 'augmented': 0, 'failed': 0}

    extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(ext))

    for img_file in sorted(image_files):
        stats['total'] += 1

        img = cv2.imread(str(img_file), cv2.IMREAD_GRAYSCALE)
        if img is None:
            stats['failed'] += 1
            continue

        # Copy original
        shutil.copy2(img_file, output_path / img_file.name)

        # Generate augmented
        for i in range(n_augments):
            try:
                augmented = pipeline(image=img)['image']
                aug_name = f"{img_file.stem}_aug{i:03d}{img_file.suffix}"
                cv2.imwrite(str(output_path / aug_name), augmented)
                stats['augmented'] += 1
            except Exception as e:
                logger.error(f"Error augmenting {img_file.name}: {e}")
                stats['failed'] += 1

    logger.info(f"Augmentation complete for '{label}': {stats}")
    return stats


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 2:
        image_path = sys.argv[1]
        label = sys.argv[2]

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"ERROR: Cannot load {image_path}")
            sys.exit(1)

        print(f"Input: {image_path} ({img.shape}), Label: {label}")

        pipeline = get_augmentation_pipeline(label)
        for i in range(5):
            aug = pipeline(image=img)['image']
            out_path = f"aug_{label}_{i}.png"
            cv2.imwrite(out_path, aug)
            print(f"  Saved: {out_path}")

        print("Done!")
    else:
        print("Usage: python augmentation.py <image_path> <dyslexic|non_dyslexic>")
