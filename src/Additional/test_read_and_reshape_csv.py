import unittest
import tempfile
import shutil
import os
import numpy as np
import warnings
import read_and_reshape_csv as rrc

class TestReadAndReshapeCSV(unittest.TestCase):

    test_directory = 'test_directory'

    def setUp(self):
        # Create a temporary directory for testing if it doesn't exist
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)

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
        csv_file_path = os.path.join(self.test_directory, 'test_file.csv')
        with open(csv_file_path, 'w') as file:
            file.write("# Sampling frequency: 100\n")
            file.write("# Sampling units: Hz\n")
            file.write("# Number of samples per column: 10\n")
            file.write("# Number of columns: 5\n")
            file.write("# Calibration status: calibrated\n")
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


if __name__ == '__main__':
    unittest.main()
