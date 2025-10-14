import numpy as np

def multiplication(A, B):
    """Return the matrix multiplication (dot product) of A and B."""
    A, B = np.array(A), np.array(B)
    if A.shape[1] != B.shape[0]:
        raise ValueError("Number of columns in A must equal number of rows in B for multiplication.")
    return np.dot(A, B)

__all__ = ['multiplication']
