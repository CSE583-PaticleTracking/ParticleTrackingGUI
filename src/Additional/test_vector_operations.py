"""
Test the function operate_on_grid() in vector_operations.py.
"""
import unittest
import numpy as np
import vector_operations as vo

class TestOperateOnGridFunction(unittest.TestCase):
    """
    Class for testing the functions in vector_operations.py.
    """

    def test_add_scalar_to_grid(self):
        """
        Test that the function adds a scalar to a grid.
        """
        grid = np.zeros((2, 2))
        vector = 5
        operation = 'add'
        result = vo.operate_on_grid(grid, vector, operation)
        expected_result = np.full_like(grid, 5)
        np.testing.assert_array_equal(result, expected_result)

    def test_multiply_vector_to_grid(self):
        """
        Test that the function multiplies a vector to a grid.
        """
        grid = np.ones((2, 2))
        vector = np.array([[2, 3], [4, 5]])
        operation = 'multiply'
        result = vo.operate_on_grid(grid, vector, operation)
        expected_result = np.array([[2, 3], [4, 5]])
        np.testing.assert_array_equal(result, expected_result)

    def test_divide_vector_with_zeros(self):
        """
        Test that the function raises error if
        divides a vector with zeros.
        """
        grid = np.ones((2, 2))
        vector = np.zeros((2, 2))
        operation = 'divide'
        result = vo.operate_on_grid(grid, vector, operation)
        expected_result = np.full_like(grid, np.nan)
        np.testing.assert_array_equal(result, expected_result)

    def test_invalid_operation(self):
        """
        Test that the function raises error if
        the operation is not one of 'add', 'subtract', 
        'multiply', or 'divide'.
        """
        grid = np.zeros((2, 2))
        vector = 2
        operation = 'invalid_operation'
        with self.assertRaises(ValueError):
            vo.operate_on_grid(grid, vector, operation)

    def test_vector_with_nan_values(self):
        """
        Test that the function raises error if
        the vector contains NaN values.
        """
        grid = np.zeros((2, 2))
        vector = np.array([[1, 2], [3, np.nan]])
        operation = 'add'
        with self.assertRaises(ValueError):
            vo.operate_on_grid(grid, vector, operation)

    def test_vector_shape_mismatch(self):
        """
        Test that the function raises error if
        the vector shape is not the same as the grid shape.
        """
        grid = np.zeros((2, 2))
        vector = np.ones((2, 3))  # Mismatched shape
        operation = 'add'
        with self.assertRaises(ValueError):
            vo.operate_on_grid(grid, vector, operation)

    def test_invalid_vector_type(self):
        """
        Test that the function raises error if
        the vector is neither a scalar nor a numpy.ndarray.
        """
        grid = np.ones((2, 2))
        vector = 'invalid_type'
        operation = 'add'
        with self.assertRaises(TypeError) as context:
            vo.operate_on_grid(grid, vector, operation)
        self.assertEqual(str(context.exception), "Vector must be a scalar or a numpy.ndarray of valid type.")


    def test_scalar_broadcasting(self):
        """
        Test that the function broadcasts a scalar to a grid.
        """
        grid = np.ones((2, 2))
        vector = 2
        operation = 'add'
        result = vo.operate_on_grid(grid, vector, operation)
        expected_result = np.full_like(grid, 3)
        np.testing.assert_array_equal(result, expected_result)

    def test_valid_operations(self):
        """
        Test that the function performs addition, subtraction,
        multiplication, and division.
        """
        grid = np.ones((2, 2))
        vector = np.ones((2, 2))
        for operation in ['add', 'subtract', 'multiply', 'divide']:
            result = vo.operate_on_grid(grid, vector, operation)
            self.assertIsInstance(result, np.ndarray)