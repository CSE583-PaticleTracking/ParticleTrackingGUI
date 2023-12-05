"""
Module containing functions for performing operations on vector fields.
"""
import warnings
import numpy as np
import pdb

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
            with np.errstate(divide='ignore'):
                result = grid / vector
            result[np.isinf(result)] = np.nan

    # Issue warning if NaN values are present in the result
    # if np.any(np.isnan(result)):
    #     warnings.warn("Division by zero occurred. Result contains NaN values.")

    return result

def calculate_magnitude_and_angle(u_grid, v_grid):
    """
    Calculate the magnitude and angle of a vector field.

    Input:
        u_grid (numpy.ndarray): 2D numpy array containing the x-component of the vector field.
        v_grid (numpy.ndarray): 2D numpy array containing the y-component of the vector field.

    Output:
        magnitude_grid (numpy.ndarray): 2D numpy array containing the magnitude of the vector field.
        angle_grid (numpy.ndarray): 2D numpy array containing the angle of the vector field.
    Usage:
        magnitude_grid, angle_grid = calculate_magnitude_and_angle(u_grid, v_grid)
    """
    try:
        # Check for NaN values in the input grids
        if np.isnan(u_grid).any() or np.isnan(v_grid).any():
            raise ValueError("Input grids contain NaN values.")

        # Calculate magnitude
        magnitude_grid = np.sqrt(u_grid**2 + v_grid**2)

        # Calculate angle
        angle_grid = np.arctan2(v_grid, u_grid)

        # Check for NaN values in the results
        if np.isnan(magnitude_grid).any() or np.isnan(angle_grid).any():
            raise ValueError("Calculation resulted in NaN values.")

        return magnitude_grid, angle_grid

    except Exception as e:
        # Handle any other exceptions
        raise e

def fill_in_nan_values_using_filter(grid, method):
    """
    Locate NaN values in a grid and replace them with either the
    mean or median of the values immediately next to them.

    Parameters:
        grid (numpy.ndarray): 2D numpy array.
        method (str): The method to be applied. Options: 'mean' or 'median'.

    Returns:
        result (numpy.ndarray): 2D numpy array with the same shape as grid.
        replaced_count (int): Number of NaN values successfully replaced.
        unsuccessful_count (int): Number of NaN values unsuccessfully replaced.
        total_points (int): Total number of non-NaN points in the grid.

    Notes:
        The function iterates over each NaN value in the grid and replaces it with the
        mean or median of the non-NaN values in its 3x3 neighborhood, excluding itself.
        Values that have already been replaced by the mean or median filter are ignored
        in future replacements to prevent reusing them. If more than 3 out of the 9 values
        used to compute the mean or median are NaN values, the NaN value is not replaced.

    Example:
        >>> grid = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
        >>> result, replaced_count, unsuccessful_count, total_points = fill_in_nan_values_using_filter(grid, method='mean')
        >>> print(result)
        [[1. 2. NaN]
         [4. 5. 6.]
         [7. 8. 9.]]
        >>> print(replaced_count)
        1
        >>> print(unsuccessful_count)
        1
        >>> print(total_points)
        9
    """
    # Check if the input is a 2D numpy array
    if not isinstance(grid, np.ndarray) or grid.ndim != 2:
        raise TypeError("Input must be a 2D numpy array.")

    # Check for a valid method
    if method not in {'mean', 'median'}:
        raise ValueError("Invalid method. Choose from 'mean' or 'median'.")

    result = grid.copy()

    # Find the indices of NaN values in the grid
    nan_indices = np.isnan(grid)

    # Set a flag for each replaced NaN value to avoid reusing them
    replaced_flags = np.zeros_like(grid, dtype=bool)

    # Initialize counters
    replaced_count = 0
    unsuccessful_count = 0
    total_points = grid.size # np.sum(~nan_indices)

    # Iterate over each NaN value and replace it
    for i, j in zip(*np.where(nan_indices)):
        if not replaced_flags[i, j]:
            neighbors = []

            # Iterate over the 3x3 neighborhood around the NaN value
            nan_count = 0
            for x in range(max(0, i - 1), min(grid.shape[0], i + 2)):
                for y in range(max(0, j - 1), min(grid.shape[1], j + 2)):
                    if not (x == i and y == j):
                        if np.isnan(grid[x, y]):
                            nan_count += 1
                        elif not replaced_flags[x, y]:
                            neighbors.append(grid[x, y])

            # Replace NaN only if fewer than 4 NaN values in the neighborhood
            # pdb.set_trace()
            if len(neighbors) > (len(neighbors) + nan_count) // 2:
                # Replace NaN with mean or median of neighbors
                if method == 'mean':
                    result[i, j] = np.mean(neighbors)
                elif method == 'median':
                    result[i, j] = np.median(neighbors)

                # Set the flag for the replaced NaN value
                replaced_flags[i, j] = True
                replaced_count += 1
            else:
                unsuccessful_count += 1

    return result, replaced_count, unsuccessful_count, total_points

def calculate_vorticity(u_grid, v_grid):
    """
    Calculate the vorticity of a 2D vector field.

    Parameters:
        u_grid (numpy.ndarray): 2D numpy array representing the x-component of the vector field.
        v_grid (numpy.ndarray): 2D numpy array representing the y-component of the vector field.

    Returns:
        numpy.ndarray: 2D numpy array containing the vorticity of the vector field.

    Raises:
        TypeError: If either u_grid or v_grid is not a 2D numpy array.
        ValueError: If u_grid and v_grid do not have the same shape.

    Warns:
        UserWarning: If either u_grid or v_grid contains NaN values. A warning is issued, and the percentage
                     of NaN values is displayed.

    Notes:
        The vorticity is calculated as the difference between the y-component partial derivative of u_grid
        and the x-component partial derivative of v_grid.

    Example:
        >>> u_grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> v_grid = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        >>> vorticity = calculate_vorticity(u_grid, v_grid)
    """
    # Check if inputs are numpy arrays
    if not isinstance(u_grid, np.ndarray) or not isinstance(v_grid, np.ndarray) or u_grid.ndim != 2 or v_grid.ndim != 2:
        raise TypeError("Input must be 2D numpy arrays.")

    # Check if inputs have the same shape
    if u_grid.shape != v_grid.shape:
        raise ValueError("Input arrays must have the same shape.")

    # Check for NaN values in inputs
    if np.isnan(u_grid).any() or np.isnan(v_grid).any():
        nan_percentage = np.sum(np.isnan(u_grid) | np.isnan(v_grid)) / u_grid.size * 100
        warning_msg = f"UserWarning: Input arrays contain {nan_percentage:.2f}% NaN values. Results may be affected."
        warnings.warn(warning_msg)

    # Calculate the partial derivatives using central differences
    du_dx = np.gradient(u_grid, axis=1)
    dv_dy = np.gradient(v_grid, axis=0)

    # Calculate the vorticity
    vorticity = dv_dy - du_dx

    return vorticity

