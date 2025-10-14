#preprocessing.py
import numpy as np

class MatrixPreprocessor:
    """
    Handles normalization and matrix preprocessing for regression models.
    """

    def __init__(self, normalize: bool = True):
        self.normalize = normalize
        self.mean_ = None
        self.std_ = None

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit normalization parameters and return transformed matrix."""
        X = np.array(X, dtype=float)
        if self.normalize:
            self.mean_ = np.mean(X, axis=0)
            self.std_ = np.std(X, axis=0)
            X = (X - self.mean_) / (self.std_ + 1e-8)
        return X

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Apply learned normalization parameters to new data."""
        X = np.array(X, dtype=float)
        if self.normalize and self.mean_ is not None:
            X = (X - self.mean_) / (self.std_ + 1e-8)
        return X
