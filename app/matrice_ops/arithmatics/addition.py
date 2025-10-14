import numpy as np

def addition(A, B):
    """Return the matrix addition of A and B."""
    A, B = np.array(A), np.array(B)
    if A.shape != B.shape:
        raise ValueError("Matrices must have the same shape for addition.")
    return A + B

__all__ = ['addition']
