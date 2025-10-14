#determinant.py

import numpy as np

def determinant(A):
    """Return the determinant of matrix A."""
    A = np.array(A)
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square to compute determinant.")
    return np.linalg.det(A)

__all__ = ['determinant']
