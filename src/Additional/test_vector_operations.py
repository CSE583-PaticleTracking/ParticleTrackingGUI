"""
Test the function operate_on_grid() in vector_operations.py.
"""
import unittest
from unittest.mock import patch
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


class TestCalculateMagnitudeAndAngle(unittest.TestCase):
    """
    Class for testing the functions in vector_operations.py.
    """

    def test_valid_input(self):
        """
        Test that the function returns the correct magnitude and angle
        of a vector field.
        """
        u_grid = np.array([[1, 2], [3, 4]])
        v_grid = np.array([[5, 6], [7, 8]])
        magnitude, angle = vo.calculate_magnitude_and_angle(u_grid, v_grid)
        np.testing.assert_array_almost_equal(magnitude, np.sqrt(u_grid**2 + v_grid**2))
        np.testing.assert_array_almost_equal(angle, np.arctan2(v_grid, u_grid))

    def test_input_with_nan_values(self):
        """
        Test that the function raises error if
        the input grids contain NaN values.
        """
        u_grid = np.array([[1, 2], [np.nan, 4]])
        v_grid = np.array([[5, 6], [7, 8]])
        with self.assertRaises(ValueError) as context:
            vo.calculate_magnitude_and_angle(u_grid, v_grid)
        self.assertEqual(str(context.exception), "Input grids contain NaN values.")

    def test_output_with_nan_values(self):
        """
        Test that the function raises error if
        the output grids contain NaN values.
        """
        u_grid = np.array([[1, 2], [3, 4]])
        v_grid = np.array([[5, 6], [7, np.nan]])
        with self.assertRaises(ValueError) as context:
            vo.calculate_magnitude_and_angle(u_grid, v_grid)
        self.assertEqual(str(context.exception), "Input grids contain NaN values.")

    def test_general_exception_handling(self):
        """
        Test that the function raises error if
        an exception occurs during calculation.
        """
        u_grid = np.array([[1, 2], [3, 4]])
        v_grid = np.array([[5, 6], [7, 8]])

        # Introduce a mock exception for testing
        with self.assertRaises(ValueError) as context:
            with unittest.mock.patch('numpy.sqrt', side_effect=ValueError("Mocked exception")):
                vo.calculate_magnitude_and_angle(u_grid, v_grid)

        self.assertEqual(str(context.exception), "Mocked exception")


class TestFillInNaNValuesUsingFilter(unittest.TestCase):
    """
    Class for testing the functions in vector_operations.py.
    """

    def test_replace_nan_with_mean(self):
        """
        Test that the function replaces NaN values with the mean
        of the values immediately next to them.
        """
        grid = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='mean')
        expected_result = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
        np.testing.assert_array_almost_equal(result, expected_result)

        # Check if the result is a numpy array
        self.assertIsInstance(result, np.ndarray)

        # Check if the shape of the result is the same as the input grid
        self.assertEqual(result.shape, grid.shape)

        # Check the counts
        self.assertEqual(replaced_count, 1)
        self.assertEqual(unsuccessful_count, 0)
        self.assertEqual(total_points, 9)

    def test_replace_nan_with_median(self):
        """
        Test that the function replaces NaN values with the median
        of the values immediately next to them.
        """
        grid = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='median')
        expected_result = np.array([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
        np.testing.assert_array_almost_equal(result, expected_result)

        # Check if the result is a numpy array
        self.assertIsInstance(result, np.ndarray)

        # Check if the shape of the result is the same as the input grid
        self.assertEqual(result.shape, grid.shape)

        # Check the counts
        self.assertEqual(replaced_count, 1)
        self.assertEqual(unsuccessful_count, 0)
        self.assertEqual(total_points, 9)

    def test_replace_close_nans_with_mean(self):
        """
        Test that the function replaces NaN values with the mean
        of the values immediately next to them and skips values
        that have already been replaced.
        """
        grid = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='mean')
        expected_result = np.array([[1., 2., 4.], [4., 5.285714, 6.], [7., 8., 9.]])
        np.testing.assert_allclose(result, expected_result, atol=1e-6)

        # Check the counts
        self.assertEqual(replaced_count, 2)
        self.assertEqual(unsuccessful_count, 0)
        self.assertEqual(total_points, 9)

    def test_replace_close_nans_with_median(self):
        """
        Test that the function replaces NaN values with the median
        of the values immediately next to them and skips values
        that have already been replaced.
        """
        grid = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='median')
        expected_result = np.array([[1., 2., 4.], [4., 6., 6.], [7., 8., 9.]])
        np.testing.assert_array_almost_equal(result, expected_result)

        # Check the counts
        self.assertEqual(replaced_count, 2)
        self.assertEqual(unsuccessful_count, 0)
        self.assertEqual(total_points, 9)

    def test_no_nans(self):
        """
        Test that the function does not modify the grid if
        there are no NaN values.
        """
        grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='mean')
        np.testing.assert_array_almost_equal(result, grid)

        # Check the counts
        self.assertEqual(replaced_count, 0)
        self.assertEqual(unsuccessful_count, 0)
        self.assertEqual(total_points, 9)

    def test_all_nans(self):
        """
        Test that the function does not modify the grid if
        all values are NaN.
        """
        grid = np.array([[np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='mean')
        np.testing.assert_array_almost_equal(result, grid)

        # Check the counts
        self.assertEqual(replaced_count, 0)
        self.assertEqual(unsuccessful_count, 9)
        self.assertEqual(total_points, 9)

    def test_nan_at_boundary(self):
        """
        Test that the function does modify the grid if
        the NaN value is at the boundary.
        """
        grid = np.array([[1, np.nan, 3], [4, 5, 6], [7, 8, 9]])
        result, replaced_count, unsuccessful_count, total_points = vo.fill_in_nan_values_using_filter(grid, method='mean')
        expected_result = np.array([[1., 3.8, 3.], [4., 5., 6.], [7., 8., 9.]])
        np.testing.assert_array_almost_equal(result, expected_result)

        # Check the counts
        self.assertEqual(replaced_count, 1)
        self.assertEqual(unsuccessful_count, 0)
        self.assertEqual(total_points, 9)

    def test_invalid_method(self):
        """
        Test that the function raises error if
        the method is not one of 'mean' or 'median'.
        """
        grid = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
        with self.assertRaises(ValueError) as context:
            vo.fill_in_nan_values_using_filter(grid, method='invalid_method')
        self.assertEqual(str(context.exception), "Invalid method. Choose from 'mean' or 'median'.")

    def test_invalid_input_type(self):
        """
        Test that the function raises error if
        the input is not a 2D numpy array.
        """
        grid = [[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]]  # Invalid input type (not a numpy array)
        with self.assertRaises(TypeError) as context:
            vo.fill_in_nan_values_using_filter(grid, method='mean')
        self.assertEqual(str(context.exception), "Input must be a 2D numpy array.")

class TestCalculateVorticity(unittest.TestCase):
    """
    Class for testing the functions in vector_operations.py.
    """

    def test_valid_inputs(self):
        """
        Test that the function returns the correct vorticity
        of a vector field.
        """
        # Test with valid inputs
        u_grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        v_grid = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        result = vo.calculate_vorticity(u_grid, v_grid)

        # Check if the result is a numpy array
        self.assertIsInstance(result, np.ndarray)

        # Check if the shape of the result is the same as input grids
        self.assertEqual(result.shape, u_grid.shape)

    def test_invalid_input_type(self):
        """
        Test that the function raises error if
        the input is not a 2D numpy array.
        """
        # Test with invalid input type
        with self.assertRaises(TypeError):
            vo.calculate_vorticity(1, np.array([[1, 2], [3, 4]]))

    def test_mismatched_shapes(self):
        """
        Test that the function raises error if
        the input arrays have mismatched shapes.
        """
        # Test with input arrays of mismatched shapes
        with self.assertRaises(ValueError):
            vo.calculate_vorticity(np.array([[1, 2], [3, 4]]), np.array([[1, 2, 3], [4, 5, 6]]))

    def test_nan_values_warning(self):
        """
        Test that the function raises warning if
        the input arrays contain NaN values.
        """
        # Test with input arrays containing NaN values
        u_grid = np.array([[1, 2, 3], [4, np.nan, 6], [7, 8, 9]])
        v_grid = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

        with self.assertWarns(UserWarning):
            vo.calculate_vorticity(u_grid, v_grid)