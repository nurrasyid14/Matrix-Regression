#__init__.py

from .linear_regression import LinearRegression
from .metrics import r2_score, mean_squared_error
from .preprocessing import MatrixPreprocessor

__all__ = ['LinearRegression', 'r2_score', 'mean_squared_error', 'MatrixPreprocessor']
