#rank.py

import numpy as np

def rank(A):
    """Return the rank of matrix A."""
    return np.linalg.matrix_rank(np.array(A))

__all__ = ['rank']
