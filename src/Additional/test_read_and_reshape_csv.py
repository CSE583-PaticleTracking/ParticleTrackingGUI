"""
Test the functions in the read_and_reshape_csv module.
"""
import unittest
import os
import warnings

import numpy as np
import read_and_reshape_csv as rrc

class TestReadAndReshapeCSV(unittest.TestCase):
    """
    Class for testing the functions in the read_and_reshape_csv module.
    """

    test_directory = 'test_directory'

    def setUp(self):
        # Create a temporary directory for testing if it doesn't exist
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)

        # Create a temporary CSV file for testing
        self.frame_000123 = 'frame_000123.csv'

    def tearDown(self):
        # Remove the files in the temporary directory
        for file_name in os.listdir(self.test_directory):
            file_path = os.path.join(self.test_directory, file_name)
            os.remove(file_path)

        # Remove the temporary directory
        os.rmdir(self.test_directory)

    def test_extract_metadata_from_csv(self):
        """
        Test that the function extracts metadata from a CSV file.
        """
        # Create a temporary CSV file with metadata
        csv_file_path = os.path.join(self.test_directory, 'metadata.csv')
        with open(csv_file_path, 'w') as file:
            file.write("# Sampling frequency: 100\n")
            file.write("# Sampling units: Hz\n")
            file.write("# Number of samples per column: 10\n")
            file.write("# Number of columns: 5\n")
            file.write("# Calibration status: True\n")
            file.write("# Spatial units: mm\n")
            file.write("# Parameter units: m/s\n")
            file.write("# Temporal units: s\n")

        metadata = rrc.extract_metadata_from_csv(csv_file_path)

        expected_metadata = {
            'Sampling frequency': 100.0,
            'Sampling units': 'Hz',
            'Number of samples per column': 10,
            'Number of columns': 5,
            'Calibration status': True,
            'Spatial units': 'mm',
            'Parameter units': 'm/s',
            'Temporal units': 's'
        }

        self.assertDictEqual(metadata, expected_metadata)

    def test_extract_and_check_consecutive_numbers(self):
        """
        Test that the function extracts frame numbers from CSV file names 
        in a directory and checks if the numbers are consecutive.
        """
        # Create a temporary directory with non-consecutive frame-numbered CSV files
        with open(os.path.join(self.test_directory, 'frame_1.csv'), 'w'):
            pass
        with open(os.path.join(self.test_directory, 'frame_3.csv'), 'w'):
            pass

        with warnings.catch_warnings(record=True) as w:
            # Cause a warning by having non-consecutive frame numbers
            rrc.extract_and_check_consecutive_numbers(self.test_directory)

            # Check that a warning was issued
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, Warning))
            self.assertIn("Warning: The extracted numbers are not consecutive or there are missing numbers.", str(w[-1].message))

    def test_valid_csv_file(self):
        """
        Test that the function checks if a CSV file is valid.
        """
        # Create a valid CSV file
        with open(self.frame_000123, 'w') as file:
            file.write("x, y, u, v\n")
            file.write("1.0, 2.0, 3.0, 4.0\n")
            file.write("2.0, 3.0, 4.0, 5.0\n")
        # Test the function
        x_positions, y_positions, u_velocities, v_velocities = rrc.read_csv_file(self.frame_000123)

        # Check data
        expected_x_positions = np.array([1.0, 2.0])
        expected_y_positions = np.array([2.0, 3.0])
        expected_u_velocities = np.array([3.0, 4.0])
        expected_v_velocities = np.array([4.0, 5.0])

        np.testing.assert_array_equal(x_positions, expected_x_positions)
        np.testing.assert_array_equal(y_positions, expected_y_positions)
        np.testing.assert_array_equal(u_velocities, expected_u_velocities)
        np.testing.assert_array_equal(v_velocities, expected_v_velocities)

    def test_file_not_exist(self):
        """
        Test when the CSV file does not exist.
        """
        # Test when the file does not exist
        with self.assertRaises(FileNotFoundError):
            rrc.read_csv_file('nonexistent_file.csv')

    def test_empty_csv_file(self):
        """
        Test when the CSV file does not contain any data.
        """
        # Test when the CSV file is empty
        with open(self.frame_000123, 'w'):
            pass

        with self.assertRaises(ValueError, msg='The CSV file does not contain any data.'):
            rrc.read_csv_file(self.frame_000123)

    def test_invalid_column_number(self):
        """
        Test when the CSV file does not contain the correct number of columns.
        """
        # Test when the CSV file does not have the correct number of columns
        with open(self.frame_000123, 'w') as file:
            file.write("x, y, u\n")
            file.write("1.0, 2.0, 3.0\n")
            file.write("2.0, 3.0, 4.0\n")

        with self.assertRaises(ValueError, msg='The CSV file does not contain the correct number of columns.'):
            rrc.read_csv_file(self.frame_000123)

    # def test_insufficient_rows(self):
    #     """
    #     Test when the CSV file does not contain enough rows.
    #     """
    #     # Test when the CSV file does not contain enough rows
    #     with open(self.frame_000123, 'w') as file:
    #         file.write("x, y, u, v\n")
    #         file.write("1.0, 2.0, 3.0, 4.0\n")

    #     with self.assertRaises(ValueError, msg='The CSV file does not contain enough rows.'):
    #         rrc.read_csv_file(self.frame_000123)

    def test_nan_values_in_coordinates(self):
        """
        Test when spatial coordinates contain NaN values.
        """
        # Test when spatial coordinates contain NaN values
        with open(self.frame_000123, 'w') as file:
            file.write("x, y, u, v\n")
            file.write("1.0, NaN, 3.0, 4.0\n")
            file.write("2.0, 3.0, 4.0, 5.0\n")

        with self.assertRaises(ValueError, msg='The spatial coordinates contain NaN values.'):
            rrc.read_csv_file(self.frame_000123)

    # def test_nan_values_in_velocities(self):
    #     """
    #     Test when velocity components contain NaN values.
    #     """
    #     # Test when velocity components contain NaN values
    #     with open(self.frame_000123, 'w') as file:
    #         file.write("x, y, u, v\n")
    #         file.write("1.0, 2.0, NaN, 4.0\n")
    #         file.write("2.0, 3.0, 4.0, 5.0\n")

    #     with self.assertWarns(Warning, msg='The velocity components contain NaN values.'):
    #         rrc.read_csv_file(self.frame_000123)

    def test_reshape_csv_file(self):
        """
        Test that the function reshapes the extracted data into a grid.
        """
        # Test case with valid input data
        x_positions = [1, 2, 3, 1, 2, 3]
        y_positions = [4, 4, 4, 5, 5, 5]
        u_velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        v_velocities = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]

        x_grid, y_grid, u_grid, v_grid = rrc.reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

        # Assert that the output grids have the expected shapes
        self.assertEqual(x_grid.shape, (2, 3))
        self.assertEqual(y_grid.shape, (2, 3))
        self.assertEqual(u_grid.shape, (2, 3))
        self.assertEqual(v_grid.shape, (2, 3))

        # Test case with empty input arrays
        with self.assertRaises(IndexError):
            rrc.reshape_csv_file([], [], [], [])

        # # Test case with incompatible shapes of input arrays
        # with self.assertRaises(ValueError):
        #     try:
        #         rrc.reshape_csv_file([1, 2, 3], [4, 5, 6, 7], [0.1, 0.2, 0.3], [1.1, 1.2, 1.3])
        #     except ValueError as e:
        #         self.assertIn("Shapes of x_positions, y_positions are not compatible for reshaping into a grid.", str(e))

        # # Test case with x or y not found in the grid
        # with self.assertRaises(IndexError):
        #     rrc.reshape_csv_file([1, 2, 3], [4, 5, 6], [0.1, 0.2, 0.3], [1.1, 1.2, 1.3])

if __name__ == '__main__':
    unittest.main()
