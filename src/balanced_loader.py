"""
balanced_loader.py
====================
Data loader dengan balanced sampling per batch untuk TensorFlow/Keras.

Menjamin setiap training batch berisi representasi seimbang
dari kedua kelas, terlepas dari distribusi dataset keseluruhan.

Strategi: 50% dyslexic + 50% non_dyslexic per batch
(oversampling minority via random sampling with replacement)

Usage:
    from src.balanced_loader import BalancedDataGenerator

    train_gen = BalancedDataGenerator(x_train, y_train, batch_size=32)
    model.fit(train_gen, epochs=50)
"""

import numpy as np
import tensorflow as tf
from pathlib import Path
from typing import Tuple, Optional, List
import cv2
import logging

logger = logging.getLogger(__name__)


class BalancedDataGenerator(tf.keras.utils.Sequence):
    """
    Keras Sequence generator yang menjamin setiap batch berisi
    representasi seimbang dari kedua kelas.

    50% dyslexic (label=1) + 50% non_dyslexic (label=0) per batch.
    Minority class di-sample dengan replacement.

    Args:
        x_data: Array gambar, shape (N, H, W, C) atau (N, H, W)
        y_data: Array label, shape (N,) — 0 atau 1
        batch_size: Ukuran batch (harus genap)
        shuffle: Shuffle dalam batch
        augmentation_fn: Fungsi augmentasi opsional f(image) -> image
    """

    def __init__(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        batch_size: int = 32,
        shuffle: bool = True,
        augmentation_fn=None
    ):
        # Pastikan batch_size genap
        self.batch_size = batch_size if batch_size % 2 == 0 else batch_size + 1
        self.shuffle = shuffle
        self.augmentation_fn = augmentation_fn

        # Pisahkan data per kelas
        pos_mask = (y_data == 1)
        neg_mask = (y_data == 0)

        self.x_pos = x_data[pos_mask]   # dyslexic (minority)
        self.x_neg = x_data[neg_mask]   # non_dyslexic (majority)

        self.n_per_class = self.batch_size // 2

        # Jumlah steps dihitung dari majority class
        self.steps = max(
            len(self.x_pos), len(self.x_neg)
        ) // self.n_per_class

        # Pastikan minimal 1 step
        self.steps = max(1, self.steps)

        logger.info(
            f"BalancedDataGenerator initialized: "
            f"pos={len(self.x_pos)}, neg={len(self.x_neg)}, "
            f"batch_size={self.batch_size}, steps={self.steps}"
        )

    def __len__(self) -> int:
        """Jumlah batches per epoch."""
        return self.steps

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate satu balanced batch.

        Minority class di-sample WITH replacement (oversampling).
        Majority class di-sample WITHOUT replacement.
        """
        # Sample dari positive class (with replacement jika perlu)
        replace_pos = len(self.x_pos) < self.n_per_class
        pos_idx = np.random.choice(
            len(self.x_pos), self.n_per_class,
            replace=replace_pos
        )

        # Sample dari negative class (without replacement jika cukup)
        replace_neg = len(self.x_neg) < self.n_per_class
        neg_idx = np.random.choice(
            len(self.x_neg), self.n_per_class,
            replace=replace_neg
        )

        # Gabungkan
        x_batch = np.concatenate([
            self.x_pos[pos_idx],
            self.x_neg[neg_idx]
        ])
        y_batch = np.concatenate([
            np.ones(self.n_per_class),
            np.zeros(self.n_per_class)
        ])

        # Opsional: augmentasi
        if self.augmentation_fn is not None:
            for i in range(len(x_batch)):
                x_batch[i] = self.augmentation_fn(x_batch[i])

        # Shuffle dalam batch
        if self.shuffle:
            shuffle_idx = np.random.permutation(len(x_batch))
            x_batch = x_batch[shuffle_idx]
            y_batch = y_batch[shuffle_idx]

        return x_batch, y_batch

    def on_epoch_end(self):
        """Called at the end of each epoch."""
        pass  # Re-shuffling handled in __getitem__ via random sampling


class DirectoryBalancedGenerator(tf.keras.utils.Sequence):
    """
    Generator yang membaca langsung dari folder tanpa
    memuat semua data ke memory (memory-efficient).

    Folder structure:
        train/
        ├── dyslexic/      (*.png / *.npy)
        └── non_dyslexic/  (*.png / *.npy)

    Args:
        data_dir: Root folder dataset
        target_size: Ukuran output gambar (H, W)
        batch_size: Ukuran batch (harus genap)
        file_format: 'image' (PNG/JPG) atau 'npy' (numpy arrays)
        augmentation_fn: Fungsi augmentasi opsional
    """

    def __init__(
        self,
        data_dir: str,
        target_size: Tuple[int, int] = (128, 128),
        batch_size: int = 32,
        file_format: str = 'image',
        augmentation_fn=None
    ):
        self.data_dir = Path(data_dir)
        self.target_size = target_size
        self.batch_size = batch_size if batch_size % 2 == 0 else batch_size + 1
        self.file_format = file_format
        self.augmentation_fn = augmentation_fn
        self.n_per_class = self.batch_size // 2

        # Kumpulkan file paths per kelas
        if file_format == 'npy':
            exts = ['*.npy']
        else:
            exts = ['*.png', '*.jpg', '*.jpeg', '*.bmp']

        self.pos_files = []  # dyslexic
        self.neg_files = []  # non_dyslexic

        for ext in exts:
            self.pos_files.extend(
                sorted((self.data_dir / 'dyslexic').glob(ext))
            )
            self.neg_files.extend(
                sorted((self.data_dir / 'non_dyslexic').glob(ext))
            )

        self.steps = max(
            len(self.pos_files), len(self.neg_files)
        ) // self.n_per_class
        self.steps = max(1, self.steps)

        logger.info(
            f"DirectoryBalancedGenerator: "
            f"dyslexic={len(self.pos_files)}, "
            f"non_dyslexic={len(self.neg_files)}, "
            f"steps={self.steps}"
        )

    def _load_image(self, path: Path) -> np.ndarray:
        """Load satu gambar dari file."""
        if self.file_format == 'npy':
            return np.load(str(path))
        else:
            img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                return np.zeros((*self.target_size, 1), dtype=np.float32)
            img = cv2.resize(img, self.target_size[::-1])
            img = img.astype(np.float32) / 255.0
            return np.expand_dims(img, axis=-1)

    def __len__(self) -> int:
        return self.steps

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate satu balanced batch dari disk."""
        # Sample file paths
        replace_pos = len(self.pos_files) < self.n_per_class
        replace_neg = len(self.neg_files) < self.n_per_class

        pos_idx = np.random.choice(
            len(self.pos_files), self.n_per_class, replace=replace_pos
        )
        neg_idx = np.random.choice(
            len(self.neg_files), self.n_per_class, replace=replace_neg
        )

        # Load images
        x_batch = []
        for i in pos_idx:
            img = self._load_image(self.pos_files[i])
            if self.augmentation_fn:
                img = self.augmentation_fn(img)
            x_batch.append(img)

        for i in neg_idx:
            img = self._load_image(self.neg_files[i])
            if self.augmentation_fn:
                img = self.augmentation_fn(img)
            x_batch.append(img)

        x_batch = np.array(x_batch)
        y_batch = np.concatenate([
            np.ones(self.n_per_class),
            np.zeros(self.n_per_class)
        ])

        # Shuffle
        shuffle_idx = np.random.permutation(len(x_batch))
        return x_batch[shuffle_idx], y_batch[shuffle_idx]

    def on_epoch_end(self):
        pass


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
        print(f"Testing DirectoryBalancedGenerator on: {data_dir}")

        gen = DirectoryBalancedGenerator(
            data_dir, target_size=(128, 128), batch_size=8
        )

        print(f"Steps per epoch: {len(gen)}")

        if len(gen) > 0:
            x, y = gen[0]
            print(f"Batch shape: x={x.shape}, y={y.shape}")
            print(f"Labels in batch: {y}")
            print(f"Positive ratio: {y.mean():.2f}")
    else:
        print("Usage: python balanced_loader.py <data_dir>")
        print("  data_dir should contain 'dyslexic/' and 'non_dyslexic/' subdirs")
