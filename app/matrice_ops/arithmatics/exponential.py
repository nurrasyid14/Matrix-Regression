import numpy as np
from scipy.linalg import expm

def exponential(A, power=None, matrix_exp=False):
    """
    Compute the exponential of a matrix.
    
    Parameters:
        A (array-like): Input matrix.
        power (float or int, optional): If given, raises A element-wise to this power.
        matrix_exp (bool, optional): If True, computes the matrix exponential e^A.
        
    Returns:
        np.ndarray: Resulting matrix.
    """
    A = np.array(A, dtype=float)
    
    if matrix_exp:
        # Compute true matrix exponential e^A
        return expm(A)
    elif power is not None:
        # Element-wise exponentiation
        return np.power(A, power)
    else:
        # Default to element-wise e^A
        return np.exp(A)

__all__ = ['exponential']
