# app/regressor/__init__.py

"""
RegressorMatrice — Regression Models and Utilities
==================================================
This module exposes all major regression classes and metrics
for easy imports across the application.
"""

from .linear_regression import LinearRegression
from .ridge_regression import RidgeRegression
from .polynomial_regression import PolynomialRegression
from .metrics import (
    r2_score,
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_error,
    explained_variance_score,
)
from .preprocessing import MatrixPreprocessor

__all__ = [
    'LinearRegression',
    'RidgeRegression',
    'PolynomialRegression',
    'r2_score',
    'mean_squared_error',
    'root_mean_squared_error',
    'mean_absolute_error',
    'explained_variance_score',
    'MatrixPreprocessor',
]
