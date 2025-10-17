import numpy as np
from matrice_ops.linalg import inverse
from matrice_ops.linalg import transpose
from matrice_ops.arithmatics import multiplication
from .model_base import BaseRegressor


class LinearRegression(BaseRegressor):
    """
    Linear Regression using pure matrix operations.

    Formula:
        β = (XᵀX)⁻¹ Xᵀy
    """

    def __init__(self, fit_intercept: bool = True):
        self.fit_intercept = fit_intercept
        self.coefficients = None
        self.fitted = False

    def _add_intercept(self, X: np.ndarray) -> np.ndarray:
        """Add a column of ones to include the intercept."""
        if not self.fit_intercept:
            return X
        ones = np.ones((X.shape[0], 1))
        return np.hstack((ones, X))

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the linear regression model using normal equations."""
        X = self._add_intercept(X)
        X_T = transpose(X)

        # β = (XᵀX)⁻¹ Xᵀy
        XTX = multiplication(X_T, X)
        XTX_inv = inverse(XTX)
        XTy = multiplication(X_T, y.reshape(-1, 1))
        beta = multiplication(XTX_inv, XTy)

        self.coefficients = beta.flatten()
        self.fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the fitted model."""
        if not self.fitted:
            raise ValueError("Model is not fitted yet.")
        X = self._add_intercept(X)
        y_pred = multiplication(X, self.coefficients.reshape(-1, 1))
        return y_pred.flatten()

    def summary(self) -> str:
        """Return a readable summary of the coefficients."""
        if not self.fitted:
            return "Model not yet fitted."
        coef_str = "\n".join(
            [f"β{i}: {coef:.4f}" for i, coef in enumerate(self.coefficients)]
        )
        return f"Linear Regression Coefficients:\n{coef_str}"
