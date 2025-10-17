import numpy as np
from .linear_regression import LinearRegression
from .model_base import BaseRegressor


class PolynomialRegression(BaseRegressor):
    """
    Polynomial Regression using pure matrix operations.

    Formula:
        y = β₀ + β₁x + β₂x² + ... + βₙxⁿ

    This class expands input features to polynomial terms
    and fits a LinearRegression model.
    """

    def __init__(self, degree: int = 2, fit_intercept: bool = True):
        self.degree = degree
        self.fit_intercept = fit_intercept
        self.model = LinearRegression(fit_intercept=fit_intercept)
        self.fitted = False

    def _expand_polynomial_features(self, X: np.ndarray) -> np.ndarray:
        """
        Expand feature matrix X to include polynomial terms up to given degree.

        Example:
            X = [[2],
                 [3]]
            degree = 3
            => [[2, 4, 8],
                [3, 9, 27]]
        """
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        poly_features = [X ** i for i in range(1, self.degree + 1)]
        return np.hstack(poly_features)

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit polynomial regression model."""
        X_poly = self._expand_polynomial_features(X)
        self.model.fit(X_poly, y)
        self.fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the polynomial regression model."""
        if not self.fitted:
            raise ValueError("Model is not fitted yet.")
        X_poly = self._expand_polynomial_features(X)
        return self.model.predict(X_poly)

    def summary(self) -> str:
        """Return a summary of the fitted coefficients."""
        if not self.fitted:
            return "Model not yet fitted."
        return f"Polynomial Regression (degree={self.degree})\n" + self.model.summary()
