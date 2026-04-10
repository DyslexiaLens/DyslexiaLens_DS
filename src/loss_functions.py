"""
loss_functions.py
==================
Custom loss functions untuk menangani class imbalance
dalam training model CNN DysRead Helper.

Tersedia:
    1. FocalLoss — Down-weight easy examples, fokus pada hard examples
    2. WeightedBinaryCrossentropy — BCE dengan class weights
    3. compute_class_weights — Utility untuk menghitung weights otomatis

Usage:
    from src.loss_functions import FocalLoss, compute_class_weights

    model.compile(
        optimizer='adam',
        loss=FocalLoss(gamma=2.0, alpha=0.75),
        metrics=['accuracy', tf.keras.metrics.Recall()]
    )

    # Atau gunakan class_weight di model.fit():
    weights = compute_class_weights(y_train)
    model.fit(x_train, y_train, class_weight=weights)
"""

import tensorflow as tf
import numpy as np
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class FocalLoss(tf.keras.losses.Loss):
    """
    Focal Loss untuk binary classification dengan class imbalance.

    Formula: FL(p_t) = -α_t * (1 - p_t)^γ * log(p_t)

    Keunggulan vs BCE biasa:
        - Down-weight sampel yang mudah diklasifikasikan (well-classified)
        - Fokus training pada hard examples (biasanya minority class)
        - γ mengontrol seberapa agresif down-weighting
        - α mengontrol balance antar kelas

    Rekomendasi parameter:
        - γ = 2.0 (standar, tingkatkan ke 3-5 jika imbalance parah)
        - α = inverse class frequency (misal: 0.75 jika dyslexic = 25%)

    Args:
        gamma: Focusing parameter (≥0). Semakin tinggi, semakin agresif
               down-weighting sampel mudah.
        alpha: Balancing factor (0-1). Weight untuk positive class.
               Set ke fraksi yang lebih besar untuk minority class.

    Reference:
        Lin et al., "Focal Loss for Dense Object Detection" (ICCV 2017)
    """

    def __init__(
        self,
        gamma: float = 2.0,
        alpha: float = 0.25,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.gamma = gamma
        self.alpha = alpha

    def call(
        self,
        y_true: tf.Tensor,
        y_pred: tf.Tensor
    ) -> tf.Tensor:
        """
        Compute focal loss.

        Args:
            y_true: Ground truth labels, shape (batch_size,) or (batch_size, 1)
            y_pred: Predicted probabilities, shape (batch_size,) or (batch_size, 1)

        Returns:
            Scalar loss value
        """
        # Clip untuk menghindari log(0)
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        y_true = tf.cast(y_true, tf.float32)

        # Binary cross entropy per sample
        bce = -(
            y_true * tf.math.log(y_pred) +
            (1.0 - y_true) * tf.math.log(1.0 - y_pred)
        )

        # p_t = probability of correct class
        p_t = y_true * y_pred + (1.0 - y_true) * (1.0 - y_pred)

        # α_t = α for positive, (1-α) for negative
        alpha_t = y_true * self.alpha + (1.0 - y_true) * (1.0 - self.alpha)

        # Focal weight: (1 - p_t)^γ
        focal_weight = alpha_t * tf.pow(1.0 - p_t, self.gamma)

        # Final loss
        focal_loss = focal_weight * bce

        return tf.reduce_mean(focal_loss)

    def get_config(self):
        """Serialization support."""
        config = super().get_config()
        config.update({
            'gamma': self.gamma,
            'alpha': self.alpha,
        })
        return config


class WeightedBinaryCrossentropy(tf.keras.losses.Loss):
    """
    Binary Cross Entropy dengan class weights terintegrasi.

    Alternatif yang lebih sederhana dari Focal Loss.
    Berguna jika Anda tidak ingin menggunakan parameter class_weight
    di model.fit() (misalnya saat menggunakan custom training loop).

    Args:
        pos_weight: Weight untuk positive class (dyslexic).
                    Biasanya = n_negative / n_positive.

    Example:
        # Dataset: 8000 normal, 800 dyslexic
        loss = WeightedBinaryCrossentropy(pos_weight=10.0)
    """

    def __init__(self, pos_weight: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.pos_weight = pos_weight

    def call(
        self,
        y_true: tf.Tensor,
        y_pred: tf.Tensor
    ) -> tf.Tensor:
        """Compute weighted BCE."""
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        y_true = tf.cast(y_true, tf.float32)

        # Weighted BCE
        loss = -(
            self.pos_weight * y_true * tf.math.log(y_pred) +
            (1.0 - y_true) * tf.math.log(1.0 - y_pred)
        )

        return tf.reduce_mean(loss)

    def get_config(self):
        config = super().get_config()
        config.update({'pos_weight': self.pos_weight})
        return config


# ═══════════════════════════════════════════════════════════
# UTILITY: COMPUTE CLASS WEIGHTS
# ═══════════════════════════════════════════════════════════

def compute_class_weights(
    y_train: np.ndarray
) -> Dict[int, float]:
    """
    Hitung class weights inversely proportional to frequency.

    Digunakan sebagai parameter `class_weight` di model.fit().

    Formula: weight_i = total / (n_classes × count_i)

    Args:
        y_train: Array label training (0 atau 1)

    Returns:
        dict: {0: weight_0, 1: weight_1}

    Example:
        >>> y = np.array([0]*8000 + [1]*800)
        >>> compute_class_weights(y)
        {0: 0.55, 1: 5.5}
    """
    try:
        from sklearn.utils.class_weight import compute_class_weight

        classes = np.unique(y_train)
        weights = compute_class_weight(
            'balanced', classes=classes, y=y_train
        )
        weight_dict = dict(zip(classes.astype(int), weights))
    except ImportError:
        # Fallback tanpa sklearn
        logger.warning("sklearn not available, computing weights manually")
        total = len(y_train)
        classes, counts = np.unique(y_train, return_counts=True)
        n_classes = len(classes)
        weight_dict = {
            int(cls): total / (n_classes * cnt)
            for cls, cnt in zip(classes, counts)
        }

    logger.info(f"Class weights: {weight_dict}")
    return weight_dict


def compute_focal_alpha(
    y_train: np.ndarray
) -> float:
    """
    Hitung α optimal untuk Focal Loss berdasarkan distribusi kelas.

    α = fraksi minority class (sehingga minority diberi weight lebih).

    Args:
        y_train: Array label training

    Returns:
        float: α value untuk FocalLoss

    Example:
        >>> y = np.array([0]*8000 + [1]*800)
        >>> compute_focal_alpha(y)
        0.909  # ~90% weight untuk minority
    """
    n_pos = np.sum(y_train == 1)
    n_neg = np.sum(y_train == 0)
    total = n_pos + n_neg

    if total == 0:
        return 0.5

    # α = proporsi negative class (sehingga positive diberi lebih)
    alpha = n_neg / total

    logger.info(
        f"Focal Loss α = {alpha:.3f} "
        f"(pos={n_pos}, neg={n_neg})"
    )
    return float(alpha)


# ═══════════════════════════════════════════════════════════
# RECOMMENDED METRICS
# ═══════════════════════════════════════════════════════════

def get_evaluation_metrics() -> list:
    """
    Return list metrik evaluasi yang direkomendasikan
    untuk binary classification dengan class imbalance.

    JANGAN gunakan Accuracy sebagai metrik utama!
    Pada dataset 10:1, model yang selalu prediksi 'Normal'
    sudah mendapat 90% accuracy.

    Returns:
        List of Keras metric instances
    """
    return [
        tf.keras.metrics.BinaryAccuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),        # PALING PENTING
        tf.keras.metrics.AUC(name='auc_roc'),
        tf.keras.metrics.AUC(
            name='auc_prc',
            curve='PR'     # Precision-Recall curve — lebih informatif
        ),
    ]


if __name__ == '__main__':
    # Quick demo
    print("=== Focal Loss Demo ===")

    # Simulasi dataset imbalanced
    y = np.array([0] * 800 + [1] * 100)
    print(f"Dataset: {len(y)} samples, pos={np.sum(y==1)}, neg={np.sum(y==0)}")

    # Class weights
    weights = compute_class_weights(y)
    print(f"Class weights: {weights}")

    # Focal alpha
    alpha = compute_focal_alpha(y)
    print(f"Focal Loss alpha: {alpha:.3f}")

    # Test Focal Loss
    focal = FocalLoss(gamma=2.0, alpha=alpha)
    y_true = tf.constant([1.0, 0.0, 1.0, 0.0])
    y_pred = tf.constant([0.9, 0.1, 0.3, 0.8])  # 2 correct, 2 wrong
    loss = focal(y_true, y_pred)
    print(f"Focal Loss value: {loss.numpy():.4f}")

    # Test weighted BCE
    wbce = WeightedBinaryCrossentropy(pos_weight=8.0)
    loss_wbce = wbce(y_true, y_pred)
    print(f"Weighted BCE value: {loss_wbce.numpy():.4f}")

    # Recommended metrics
    metrics = get_evaluation_metrics()
    print(f"Recommended metrics: {[m.name for m in metrics]}")
