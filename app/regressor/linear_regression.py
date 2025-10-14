import numpy as np
from .preprocessing import MatrixPreprocessor
from .metrics import r2_score
from .model_base import BaseRegressor

class LinearRegression(BaseRegressor):
    """
    Linear Regression implemented via matrix operations.
    β = (XᵀX)⁻¹Xᵀy
    """

    def __init__(self, normalize=True):
        self.preprocessor = MatrixPreprocessor(normalize)
        self.beta_ = None
        self.fitted_ = False

    def fit(self, X, y):
        X = self.preprocessor.fit_transform(X)
        y = np.array(y, dtype=float).reshape(-1, 1)

        X = np.hstack((np.ones((X.shape[0], 1)), X))  # Add bias term
        self.beta_ = np.linalg.pinv(X.T @ X) @ X.T @ y
        self.fitted_ = True
        return self

    def predict(self, X):
        if not self.fitted_:
            raise RuntimeError("Model must be fitted before prediction.")

        X = self.preprocessor.transform(X)
        X = np.hstack((np.ones((X.shape[0], 1)), X))
        return X @ self.beta_

    def score(self, X, y):
        y_pred = self.predict(X)
        return r2_score(y, y_pred)

    def coefficients(self):
        if not self.fitted_:
            raise RuntimeError("Model is not yet fitted.")
        return self.beta_.flatten()
