import numpy as np

def fraction(A, B):
    """
    Perform matrix division: A * inverse(B).
    
    Parameters:
        A (array-like): Left-hand matrix.
        B (array-like): Right-hand matrix (must be square and invertible).
    
    Returns:
        np.ndarray: Result of A * B^-1.
    """
    A, B = np.array(A), np.array(B)
    if B.shape[0] != B.shape[1]:
        raise ValueError("Matrix B must be square to compute its inverse.")
    try:
        B_inv = np.linalg.inv(B)
    except np.linalg.LinAlgError:
        raise ValueError("Matrix B is singular and cannot be inverted.")
    return np.dot(A, B_inv)

__all__ = ['fraction']
