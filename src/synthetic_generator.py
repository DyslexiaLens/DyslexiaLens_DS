"""
synthetic_generator.py
=======================
Modul untuk menghasilkan gambar tulisan tangan sintetis
dengan karakteristik disleksia dari sampel tulisan normal.

Teknik Simulasi:
    1. Letter Reversal — Pembalikan huruf horizontal (b↔d, p↔q)
    2. Irregular Spacing — Spasi antar huruf tidak konsisten
    3. Size Inconsistency — Ukuran huruf bervariasi dalam satu kata
    4. Rotation Jitter — Huruf miring ke arah berbeda-beda
    5. Baseline Drift — Huruf melayang dari garis dasar
    6. Stroke Tremor — Gemetar pada goresan (kontrol motorik lemah)

Usage:
    from src.synthetic_generator import DyslexiaSimulator

    simulator = DyslexiaSimulator()
    dyslexic_sample = simulator.generate_dyslexic_sample(normal_image)

PERINGATAN: Sampel sintetis HARUS divalidasi oleh ahli psikologi/terapis
sebelum digunakan untuk training model produksi.
"""

import cv2
import numpy as np
from scipy.ndimage import rotate, shift
from pathlib import Path
from typing import List, Tuple, Optional, Callable
import random
import logging

logger = logging.getLogger(__name__)


class DyslexiaSimulator:
    """
    Simulator pola disleksia pada gambar tulisan tangan.

    Menerapkan transformasi yang secara klinis relevan pada
    tulisan normal untuk menghasilkan sampel sintetis disleksia.

    Args:
        reversal_prob: Probabilitas letter reversal per karakter (0-1)
        spacing_jitter: Intensitas jitter spasi (0-1, relatif terhadap lebar karakter)
        size_variation: Intensitas variasi ukuran (0-1)
        rotation_range: Range rotasi dalam derajat
        baseline_drift: Intensitas drift baseline (0-1, relatif terhadap tinggi karakter)
        tremor_intensity: Intensitas gemetar stroke (0-1)
        seed: Random seed untuk reproducibility (opsional)
    """

    def __init__(
        self,
        reversal_prob: float = 0.3,
        spacing_jitter: float = 0.4,
        size_variation: float = 0.3,
        rotation_range: float = 15.0,
        baseline_drift: float = 0.2,
        tremor_intensity: float = 0.15,
        seed: Optional[int] = None
    ):
        self.reversal_prob = reversal_prob
        self.spacing_jitter = spacing_jitter
        self.size_variation = size_variation
        self.rotation_range = rotation_range
        self.baseline_drift = baseline_drift
        self.tremor_intensity = tremor_intensity

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    # ── 1. LETTER REVERSAL (Pembalikan Huruf) ──────────────

    def apply_reversal(self, char_img: np.ndarray) -> np.ndarray:
        """
        Membalik huruf secara horizontal (mirror).

        Target huruf dalam tulisan nyata: b↔d, p↔q, 6↔9, n↔u, m↔w.
        Secara klinis, ini adalah ciri paling khas disleksia.

        Args:
            char_img: Gambar karakter individual (grayscale/binary)

        Returns:
            Gambar yang mungkin dibalik (berdasarkan probabilitas)
        """
        if random.random() < self.reversal_prob:
            return cv2.flip(char_img, 1)  # 1 = horizontal flip
        return char_img.copy()

    # ── 2. IRREGULAR SPACING (Spasi Tidak Konsisten) ───────

    def apply_irregular_spacing(
        self,
        chars: List[np.ndarray],
        base_spacing: int = 10,
        canvas_width: int = 500,
        canvas_height: int = 100
    ) -> np.ndarray:
        """
        Susun karakter dengan jarak yang tidak konsisten.

        Disleksia sering menunjukkan spasi yang sangat bervariasi:
        kadang terlalu rapat, kadang terlalu renggang.

        Args:
            chars: List gambar karakter individual
            base_spacing: Jarak dasar antar karakter (pixel)
            canvas_width: Lebar canvas output
            canvas_height: Tinggi canvas output

        Returns:
            Gambar canvas dengan karakter tersusun
        """
        canvas = np.zeros((canvas_height, canvas_width), dtype=np.uint8)
        x_offset = random.randint(5, 20)

        for char_img in chars:
            h, w = char_img.shape[:2]

            # Jitter spasi: bisa negatif (overlap) atau positif (gap)
            jitter = int(np.random.normal(0, base_spacing * self.spacing_jitter))
            x_offset += max(0, jitter)

            # Pastikan tidak keluar canvas
            if x_offset + w >= canvas_width:
                break

            # Vertical centering dengan sedikit jitter
            y_offset = max(0, (canvas_height - h) // 2 + random.randint(-3, 3))
            y_end = min(y_offset + h, canvas_height)
            x_end = min(x_offset + w, canvas_width)

            # Paste karakter (additive untuk handle overlap)
            roi = canvas[y_offset:y_end, x_offset:x_end]
            char_crop = char_img[:y_end-y_offset, :x_end-x_offset]
            canvas[y_offset:y_end, x_offset:x_end] = np.maximum(roi, char_crop)

            x_offset += w + base_spacing

        return canvas

    # ── 3. SIZE INCONSISTENCY (Ukuran Huruf Tidak Konsisten)─

    def apply_size_variation(self, char_img: np.ndarray) -> np.ndarray:
        """
        Memperbesar/mengecilkan huruf secara random.

        Anak disleksia sering menulis huruf dengan ukuran yang
        sangat bervariasi dalam satu kata.

        Args:
            char_img: Gambar karakter individual

        Returns:
            Gambar karakter yang di-resize secara random
        """
        scale = 1.0 + np.random.uniform(
            -self.size_variation, self.size_variation
        )
        scale = max(0.5, min(2.0, scale))  # Clamp ke range wajar

        h, w = char_img.shape[:2]
        new_h = max(5, int(h * scale))
        new_w = max(5, int(w * scale))

        return cv2.resize(
            char_img, (new_w, new_h),
            interpolation=cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        )

    # ── 4. ROTATION JITTER (Kemiringan Huruf) ─────────────

    def apply_rotation_jitter(self, char_img: np.ndarray) -> np.ndarray:
        """
        Memutar huruf pada sudut random.

        Tulisan disleksia sering menunjukkan huruf yang miring
        ke arah yang tidak konsisten (bukan slant global yang seragam).

        Args:
            char_img: Gambar karakter individual

        Returns:
            Gambar karakter yang dirotasi
        """
        angle = np.random.uniform(
            -self.rotation_range, self.rotation_range
        )
        return rotate(
            char_img, angle, reshape=False,
            mode='constant', cval=0
        )

    # ── 5. BASELINE DRIFT (Garis Dasar Melayang) ──────────

    def apply_baseline_drift(
        self,
        char_img: np.ndarray,
        char_height: Optional[int] = None
    ) -> np.ndarray:
        """
        Menggeser huruf ke atas/bawah dari baseline.

        Disleksia menyebabkan huruf 'melompat-lompat'
        dari garis dasar tulisan.

        Args:
            char_img: Gambar karakter individual
            char_height: Tinggi referensi untuk menghitung max shift.
                         Jika None, gunakan tinggi gambar.

        Returns:
            Gambar karakter yang digeser secara vertikal
        """
        if char_height is None:
            char_height = char_img.shape[0]

        max_shift = max(1, int(char_height * self.baseline_drift))
        dy = np.random.randint(-max_shift, max_shift + 1)

        return shift(char_img, [dy, 0], mode='constant', cval=0)

    # ── 6. STROKE TREMOR (Gemetar pada Goresan) ───────────

    def apply_stroke_tremor(self, img: np.ndarray) -> np.ndarray:
        """
        Menambahkan distorsi 'gemetar' pada goresan menggunakan
        elastic deformation ringan.

        Mensimulasikan kontrol motorik halus yang lemah,
        umum pada anak disleksia.

        Args:
            img: Gambar tulisan (bisa per-karakter atau per-baris)

        Returns:
            Gambar dengan efek tremor
        """
        rows, cols = img.shape[:2]

        # Random displacement fields
        dx = np.random.uniform(-1, 1, (rows, cols)).astype(np.float32)
        dy = np.random.uniform(-1, 1, (rows, cols)).astype(np.float32)

        # Scale by tremor intensity
        intensity = self.tremor_intensity * min(rows, cols)
        dx *= intensity
        dy *= intensity

        # Gaussian smoothing agar distorsi terlihat natural
        # (bukan noise random per-pixel)
        sigma = max(3, min(rows, cols) // 10)
        kernel_size = sigma * 2 + 1
        if kernel_size % 2 == 0:
            kernel_size += 1

        dx = cv2.GaussianBlur(dx, (kernel_size, kernel_size), sigma)
        dy = cv2.GaussianBlur(dy, (kernel_size, kernel_size), sigma)

        # Buat remap coordinates
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))
        map_x = (x + dx).astype(np.float32)
        map_y = (y + dy).astype(np.float32)

        return cv2.remap(
            img, map_x, map_y, cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )

    # ── FULL PIPELINE ──────────────────────────────────────

    def generate_dyslexic_sample(
        self,
        normal_img: np.ndarray,
        apply_all: bool = False,
        n_transforms: Optional[int] = None
    ) -> np.ndarray:
        """
        Terapkan kombinasi random transformasi disleksia pada gambar.

        Args:
            normal_img: Gambar tulisan normal (grayscale/binary)
            apply_all: Jika True, terapkan semua transformasi
            n_transforms: Jumlah transformasi spesifik (override random)

        Returns:
            Gambar dengan karakteristik disleksia sintetis
        """
        transforms: List[Callable] = [
            self.apply_reversal,
            self.apply_size_variation,
            self.apply_rotation_jitter,
            lambda img: self.apply_baseline_drift(img),
            self.apply_stroke_tremor,
        ]

        result = normal_img.copy()

        if apply_all:
            for t in transforms:
                result = t(result)
        else:
            # Pilih N transformasi secara random
            if n_transforms is None:
                n_transforms = random.randint(2, 4)
            n_transforms = min(n_transforms, len(transforms))

            selected = random.sample(transforms, n_transforms)
            for t in selected:
                result = t(result)

        return result

    def generate_batch(
        self,
        normal_images: List[np.ndarray],
        samples_per_image: int = 3,
        apply_all: bool = False
    ) -> List[np.ndarray]:
        """
        Generate multiple sampel disleksia dari batch gambar normal.

        Args:
            normal_images: List gambar tulisan normal
            samples_per_image: Jumlah sampel sintetis per gambar input
            apply_all: Jika True, terapkan semua transformasi

        Returns:
            List gambar sintetis disleksia
        """
        synthetic_samples = []

        for img in normal_images:
            for _ in range(samples_per_image):
                syn = self.generate_dyslexic_sample(img, apply_all=apply_all)
                synthetic_samples.append(syn)

        logger.info(
            f"Generated {len(synthetic_samples)} synthetic dyslexic samples "
            f"from {len(normal_images)} normal images"
        )
        return synthetic_samples


# ═══════════════════════════════════════════════════════════
# BATCH GENERATION DARI FOLDER
# ═══════════════════════════════════════════════════════════

def generate_synthetic_dataset(
    input_dir: str,
    output_dir: str,
    samples_per_image: int = 3,
    simulator: Optional[DyslexiaSimulator] = None,
    image_extensions: List[str] = None
) -> dict:
    """
    Generate dataset sintetis disleksia dari folder gambar normal.

    Args:
        input_dir: Folder berisi gambar tulisan normal
        output_dir: Folder output untuk sampel sintetis
        samples_per_image: Jumlah sampel per gambar input
        simulator: Instance DyslexiaSimulator (opsional, buat baru jika None)
        image_extensions: List ekstensi file gambar

    Returns:
        dict statistik: {'total_input', 'total_generated', 'failed'}
    """
    if simulator is None:
        simulator = DyslexiaSimulator()

    if image_extensions is None:
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stats = {'total_input': 0, 'total_generated': 0, 'failed': 0}

    # Kumpulkan semua file gambar
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(ext))
    image_files = sorted(image_files)

    for img_file in image_files:
        stats['total_input'] += 1

        img = cv2.imread(str(img_file), cv2.IMREAD_GRAYSCALE)
        if img is None:
            stats['failed'] += 1
            continue

        for i in range(samples_per_image):
            try:
                synthetic = simulator.generate_dyslexic_sample(img)
                out_name = f"{img_file.stem}_syn{i:03d}.png"
                cv2.imwrite(str(output_path / out_name), synthetic)
                stats['total_generated'] += 1
            except Exception as e:
                logger.error(f"Error generating from {img_file.name}: {e}")
                stats['failed'] += 1

    logger.info(
        f"Synthetic generation complete: "
        f"{stats['total_generated']} samples from "
        f"{stats['total_input']} inputs "
        f"({stats['failed']} failures)"
    )
    return stats


# ═══════════════════════════════════════════════════════════
# PRESET CONFIGURATIONS
# ═══════════════════════════════════════════════════════════

def get_mild_simulator() -> DyslexiaSimulator:
    """Simulator dengan parameter disleksia ringan."""
    return DyslexiaSimulator(
        reversal_prob=0.15,
        spacing_jitter=0.2,
        size_variation=0.15,
        rotation_range=8.0,
        baseline_drift=0.1,
        tremor_intensity=0.08,
    )


def get_moderate_simulator() -> DyslexiaSimulator:
    """Simulator dengan parameter disleksia sedang (default)."""
    return DyslexiaSimulator()


def get_severe_simulator() -> DyslexiaSimulator:
    """Simulator dengan parameter disleksia berat."""
    return DyslexiaSimulator(
        reversal_prob=0.5,
        spacing_jitter=0.6,
        size_variation=0.45,
        rotation_range=25.0,
        baseline_drift=0.35,
        tremor_intensity=0.25,
    )


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 2:
        input_img = sys.argv[1]
        output_prefix = sys.argv[2]

        img = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"ERROR: Cannot load {input_img}")
            sys.exit(1)

        print(f"Input: {input_img} ({img.shape})")
        print(f"Generating 3 severity levels × 3 samples each...")

        for name, sim in [
            ('mild', get_mild_simulator()),
            ('moderate', get_moderate_simulator()),
            ('severe', get_severe_simulator()),
        ]:
            for i in range(3):
                result = sim.generate_dyslexic_sample(img)
                out_path = f"{output_prefix}_{name}_{i}.png"
                cv2.imwrite(out_path, result)
                print(f"  Saved: {out_path}")

        print("Done!")
    else:
        print("Usage: python synthetic_generator.py <input_image> <output_prefix>")
