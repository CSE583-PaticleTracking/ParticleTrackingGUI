import numpy as np
import warnings

def operate_on_grid(grid, vector, operation):
    """
    Perform addition, subtraction, multiplication, or division 
    of a vector on a grid. The vector can be a scalar or 
    a 2D numpy array with the same shape as grid. If a scalar,
    the same value is added to each element in the grid. If a
    2D numpy array, the vector is added element-wise to the grid.

    Parameters:
        grid (numpy.ndarray): 2D numpy array.
        vector (scalar or numpy.ndarray): Scalar or 2D numpy array with the same shape as grid.
        operation (str): The mathematical operation to be performed. 
            Options: 'add', 'subtract', 'multiply', 'divide'.

    Returns:
        result (numpy.ndarray): 2D numpy array with the same shape as grid.

    Raises:
        ValueError: If the shape of the vector is not the same as the shape of the grid.
        ValueError: If the vector contains NaN values.
        TypeError: If the input vector is neither a scalar nor a numpy.ndarray.
        ValueError: If the operation is not one of 'add', 'subtract', 'multiply', or 'divide'.
    """
    # Validate operation
    valid_operations = {'add', 'subtract', 'multiply', 'divide'}
    if operation not in valid_operations:
        raise ValueError("Invalid operation. Choose from 'add', 'subtract', 'multiply', or 'divide'.")

    # Check if the vector is a scalar or a 2D numpy array
    if not isinstance(vector, (int, float, np.ndarray)):
        raise TypeError("Vector must be a scalar or a numpy.ndarray of valid type.")

    if np.isscalar(vector):
        vector = np.full_like(grid, vector)  # Broadcast scalar to grid shape

    # Perform additional checks for vector as 2D numpy array
    if isinstance(vector, np.ndarray):
        if vector.shape != grid.shape:
            raise ValueError("Vector shape must be the same as grid shape.")
        if np.isnan(vector).any():
            raise ValueError("Vector contains NaN values.")
    else:
        raise TypeError("Vector must be a scalar or a numpy.ndarray.")

    # Perform element-wise operations based on the specified operation
    with np.errstate(divide='warn', invalid='warn'):
        if operation == 'add':
            result = grid + vector
        elif operation == 'subtract':
            result = grid - vector
        elif operation == 'multiply':
            result = grid * vector
        elif operation == 'divide':
            result = grid / vector
            result[np.isinf(result)] = np.nan

    # Issue warning if NaN values are present in the result
    if np.any(np.isnan(result)):
        warnings.warn("Division by zero occurred. Result contains NaN values.")

    return result
