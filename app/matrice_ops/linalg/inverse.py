#inverse.py

import numpy as np

def inverse(A):
    """Return the inverse of matrix A."""
    A = np.array(A)
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square to compute inverse.")
    try:
        return np.linalg.inv(A)
    except np.linalg.LinAlgError:
        raise ValueError("Matrix is singular and cannot be inverted.")

__all__ = ['inverse']