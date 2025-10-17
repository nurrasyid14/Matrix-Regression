import numpy as np
from app.matrice_ops.linalg import inverse, transpose
from app.matrice_ops import multiplication
from .model_base import BaseRegressor


class RidgeRegression(BaseRegressor):
    """
    Ridge Regression using pure matrix operations.

    Formula:
        β = (XᵀX + λI)⁻¹ Xᵀy

    Where:
        λ (lambda) = regularization strength
        I = identity matrix
    """

    def __init__(self, alpha: float = 1.0, fit_intercept: bool = True):
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.coefficients = None
        self.fitted = False

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """Add column of ones if intercept is to be fitted."""
        if not self.fit_intercept:
            return X
        ones = np.ones((X.shape[0], 1))
        return np.hstack((ones, X))

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the Ridge Regression model."""
        X = self._add_intercept(X)
        X_T = transpose(X)

        # Ridge formula: β = (XᵀX + λI)⁻¹ Xᵀy
        XTX = multiplication(X_T, X)
        I = np.eye(XTX.shape[0])
        ridge_term = XTX + self.alpha * I

        ridge_inv = inverse(ridge_term)
        XTy = multiplication(X_T, y.reshape(-1, 1))
        beta = multiplication(ridge_inv, XTy)

        self.coefficients = beta.flatten()
        self.fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the Ridge model."""
        if not self.fitted:
            raise ValueError("Model is not fitted yet.")
        X = self._add_intercept(X)
        y_pred = multiplication(X, self.coefficients.reshape(-1, 1))
        return y_pred.flatten()

    def summary(self) -> str:
        """Readable summary of coefficients."""
        if not self.fitted:
            return "Model not yet fitted."
        coef_str = "\n".join(
            [f"β{i}: {coef:.4f}" for i, coef in enumerate(self.coefficients)]
        )
        return f"Ridge Regression Coefficients (λ={self.alpha}):\n{coef_str}"
