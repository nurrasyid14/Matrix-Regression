#transpose.py

import numpy as np

def transpose(A):
    """Return the transpose of matrix A."""
    return np.transpose(np.array(A))

__all__ = ['transpose']