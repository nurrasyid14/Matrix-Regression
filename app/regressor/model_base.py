#model_base.py

import numpy as np

class BaseRegressor:
    """
    Base class defining the interface for regression models.
    """

    def fit(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError

    def predict(self, X: np.ndarray):
        raise NotImplementedError

    def score(self, X: np.ndarray, y: np.ndarray):
        raise NotImplementedError
