"""
rebalancing.py
===============
Teknik rebalancing dataset untuk DysRead Helper.

Strategi bertingkat untuk mengatasi class imbalance:
    Layer 1 (Data-Level): Targeted augmentation + synthetic generation
    Layer 2 (Algorithm-Level): Class weighting + focal loss
    Layer 3 (Sampling-Level): Balanced batch sampling

Usage:
    from src.rebalancing import (
        analyze_class_distribution,
        compute_augmentation_factor,
        rebalance_dataset
    )

    stats = analyze_class_distribution('processed/train/')
    factors = compute_augmentation_factor(stats)
    rebalance_dataset('processed/train/', factors)
"""

import numpy as np
import cv2
from pathlib import Path
from collections import Counter
from typing import Dict, Optional, List
import shutil
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════
# ANALISIS DISTRIBUSI
# ═══════════════════════════════════════════════════════════

def analyze_class_distribution(
    dataset_dir: str,
    class_names: List[str] = None
) -> Dict[str, int]:
    """
    Analisis distribusi kelas dalam dataset.

    Args:
        dataset_dir: Root folder dataset (berisi subfolder per kelas)
        class_names: Nama kelas (default: ['dyslexic', 'non_dyslexic'])

    Returns:
        dict: {class_name: count}

    Example:
        >>> analyze_class_distribution('processed/train/')
        {'dyslexic': 800, 'non_dyslexic': 8000}
    """
    if class_names is None:
        class_names = ['dyslexic', 'non_dyslexic']

    dataset_path = Path(dataset_dir)
    distribution = {}

    for cls in class_names:
        cls_dir = dataset_path / cls
        if cls_dir.exists():
            # Count all image files
            count = sum(
                1 for f in cls_dir.iterdir()
                if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.npy']
            )
            distribution[cls] = count
        else:
            distribution[cls] = 0
            logger.warning(f"Class directory not found: {cls_dir}")

    # Log summary
    total = sum(distribution.values())
    logger.info(f"Class distribution (total={total}):")
    for cls, count in distribution.items():
        pct = (count / total * 100) if total > 0 else 0
        logger.info(f"  {cls}: {count} ({pct:.1f}%)")

    if len(distribution) >= 2:
        counts = list(distribution.values())
        ratio = max(counts) / max(min(counts), 1)
        logger.info(f"  Imbalance ratio: {ratio:.1f}:1")

    return distribution


def compute_augmentation_factor(
    class_counts: Dict[str, int],
    target_ratio: float = 1.0,
    max_factor: int = 10
) -> Dict[str, int]:
    """
    Hitung berapa kali tiap kelas harus di-augmentasi
    untuk mencapai rasio target.

    Args:
        class_counts: {'dyslexic': 800, 'non_dyslexic': 8000}
        target_ratio: 1.0 = seimbang sempurna, 0.5 = minority setengah majority
        max_factor: Faktor augmentasi maksimum (hindari over-augmentation)

    Returns:
        dict: {class_name: augmentation_factor}

    Example:
        >>> compute_augmentation_factor({'dyslexic': 800, 'non_dyslexic': 8000})
        {'dyslexic': 8, 'non_dyslexic': 1}
    """
    if not class_counts:
        return {}

    max_count = max(class_counts.values())
    factors = {}

    for cls, count in class_counts.items():
        if count == 0:
            factors[cls] = 0
            logger.warning(f"Class '{cls}' has 0 samples!")
            continue

        target = int(max_count * target_ratio)
        factor = max(1, min(target // count, max_factor))
        factors[cls] = factor

    logger.info(f"Augmentation factors: {factors}")
    return factors


# ═══════════════════════════════════════════════════════════
# REBALANCING VIA AUGMENTATION
# ═══════════════════════════════════════════════════════════

def targeted_augmentation(
    input_dir: str,
    output_dir: str,
    n_augments: int = 5,
    label: str = 'dyslexic'
) -> Dict[str, int]:
    """
    Generate n_augments variasi augmentasi per gambar.
    Dirancang untuk MINORITY class (dyslexic).

    Args:
        input_dir: Folder berisi gambar minority class
        output_dir: Folder output (originals + augmented)
        n_augments: Jumlah augmentasi per gambar
        label: Label kelas untuk memilih pipeline augmentasi

    Returns:
        dict statistik: {'originals', 'augmented', 'total'}
    """
    from src.augmentation import get_augmentation_pipeline

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pipeline = get_augmentation_pipeline(label)
    stats = {'originals': 0, 'augmented': 0, 'failed': 0}

    extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(ext))

    for img_file in sorted(image_files):
        # Copy original
        shutil.copy2(img_file, output_path / img_file.name)
        stats['originals'] += 1

        img = cv2.imread(str(img_file), cv2.IMREAD_GRAYSCALE)
        if img is None:
            stats['failed'] += 1
            continue

        # Generate augmented versions
        for i in range(n_augments):
            try:
                augmented = pipeline(image=img)['image']
                aug_name = f"{img_file.stem}_aug{i:03d}{img_file.suffix}"
                cv2.imwrite(str(output_path / aug_name), augmented)
                stats['augmented'] += 1
            except Exception as e:
                logger.error(f"Error augmenting {img_file.name}[{i}]: {e}")
                stats['failed'] += 1

    stats['total'] = stats['originals'] + stats['augmented']
    logger.info(f"Targeted augmentation complete: {stats}")
    return stats


# ═══════════════════════════════════════════════════════════
# CLASS WEIGHTING
# ═══════════════════════════════════════════════════════════

def compute_class_weights(y_train: np.ndarray) -> Dict[int, float]:
    """
    Hitung class weights yang inversely proportional to frequency.

    Digunakan sebagai parameter `class_weight` di model.fit().

    Args:
        y_train: Array label training (0 atau 1)

    Returns:
        dict: {class_id: weight}

    Example:
        >>> compute_class_weights(np.array([0,0,0,0,0,0,0,0,1,1]))
        {0: 0.625, 1: 2.5}
    """
    from sklearn.utils.class_weight import compute_class_weight

    classes = np.unique(y_train)
    weights = compute_class_weight(
        'balanced', classes=classes, y=y_train
    )
    weight_dict = dict(zip(classes.astype(int), weights))

    logger.info(f"Computed class weights: {weight_dict}")
    return weight_dict


def compute_class_weights_manual(
    class_counts: Dict[str, int]
) -> Dict[int, float]:
    """
    Hitung class weights secara manual tanpa sklearn.

    Formula: weight_i = total_samples / (n_classes * count_i)

    Args:
        class_counts: {'non_dyslexic': 8000, 'dyslexic': 800}

    Returns:
        dict: {0: weight_normal, 1: weight_dyslexic}
    """
    total = sum(class_counts.values())
    n_classes = len(class_counts)

    # Mapping: non_dyslexic=0, dyslexic=1
    label_map = {'non_dyslexic': 0, 'dyslexic': 1}
    weights = {}

    for cls_name, count in class_counts.items():
        if cls_name in label_map and count > 0:
            label_id = label_map[cls_name]
            weights[label_id] = total / (n_classes * count)

    logger.info(f"Manual class weights: {weights}")
    return weights


# ═══════════════════════════════════════════════════════════
# FULL REBALANCING PIPELINE
# ═══════════════════════════════════════════════════════════

def rebalance_dataset(
    dataset_dir: str,
    output_dir: Optional[str] = None,
    target_ratio: float = 1.0,
    max_augmentation_factor: int = 8,
    use_synthetic: bool = True
) -> Dict[str, any]:
    """
    Pipeline rebalancing end-to-end.

    Strategi:
        1. Analisis distribusi kelas
        2. Hitung faktor augmentasi per kelas
        3. Augmentasi targeted pada minority class
        4. (Opsional) Generate sampel sintetis
        5. Report distribusi akhir

    Args:
        dataset_dir: Root folder dataset (subfolder per kelas)
        output_dir: Output folder (default: dataset_dir + '_balanced')
        target_ratio: Target rasio minority/majority
        max_augmentation_factor: Max augmentasi per gambar
        use_synthetic: Jika True, tambahkan synthetic generation

    Returns:
        dict report: distribusi sebelum/sesudah, faktor yang digunakan
    """
    dataset_path = Path(dataset_dir)

    if output_dir is None:
        output_dir = str(dataset_path.parent / f"{dataset_path.name}_balanced")
    output_path = Path(output_dir)

    # Step 1: Analisis distribusi
    distribution_before = analyze_class_distribution(dataset_dir)

    # Step 2: Hitung faktor
    factors = compute_augmentation_factor(
        distribution_before, target_ratio, max_augmentation_factor
    )

    # Step 3: Copy/augment per kelas
    for cls_name, factor in factors.items():
        src_dir = dataset_path / cls_name
        dst_dir = output_path / cls_name
        dst_dir.mkdir(parents=True, exist_ok=True)

        if factor <= 1:
            # Majority class: just copy
            logger.info(f"Copying {cls_name} (factor=1)...")
            for f in src_dir.iterdir():
                if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                    shutil.copy2(f, dst_dir / f.name)
        else:
            # Minority class: augment
            logger.info(f"Augmenting {cls_name} (factor={factor})...")
            targeted_augmentation(
                str(src_dir), str(dst_dir),
                n_augments=factor - 1,  # -1 karena original sudah di-copy
                label=cls_name
            )

    # Step 4: Opsional synthetic generation
    if use_synthetic and 'dyslexic' in factors and factors.get('dyslexic', 1) > 1:
        from src.synthetic_generator import DyslexiaSimulator, generate_synthetic_dataset

        # Generate dari sampel normal
        normal_dir = dataset_path / 'non_dyslexic'
        syn_dst = output_path / 'dyslexic'

        if normal_dir.exists():
            logger.info("Generating synthetic dyslexic samples from normal data...")
            generate_synthetic_dataset(
                str(normal_dir),
                str(syn_dst),
                samples_per_image=1,  # Conservative
                simulator=DyslexiaSimulator()
            )

    # Step 5: Report
    distribution_after = analyze_class_distribution(output_dir)

    report = {
        'before': distribution_before,
        'after': distribution_after,
        'factors': factors,
        'output_dir': output_dir,
    }

    logger.info(f"Rebalancing complete. Output: {output_dir}")
    return report


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    if len(sys.argv) > 1:
        dataset_dir = sys.argv[1]
        print(f"Analyzing: {dataset_dir}")

        dist = analyze_class_distribution(dataset_dir)
        factors = compute_augmentation_factor(dist)

        print(f"\nDistribution: {dist}")
        print(f"Augmentation factors: {factors}")

        if len(sys.argv) > 2 and sys.argv[2] == '--rebalance':
            print("\nStarting rebalancing...")
            report = rebalance_dataset(dataset_dir)
            print(f"\nFinal distribution: {report['after']}")
    else:
        print("Usage: python rebalancing.py <dataset_dir> [--rebalance]")
