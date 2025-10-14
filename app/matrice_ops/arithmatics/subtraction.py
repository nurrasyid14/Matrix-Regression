import numpy as np

def subtraction(A, B):
    """Return the matrix subtraction of A and B."""
    A, B = np.array(A), np.array(B)
    if A.shape != B.shape:
        raise ValueError("Matrices must have the same shape for subtraction.")
    return A - B

__all__ = ['subtraction']
