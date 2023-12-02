import unittest
import tempfile
import shutil
import os
import numpy as np
import read_and_reshape_csv as rrc

class TestReadAndReshapeCSV(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_directory = 'test_directory'
        os.makedirs(self.test_directory)

    def tearDown(self):
        # Remove the temporary directory and its contents after testing
        os.rmdir(self.test_directory)

    def test_extract_metadata_from_csv(self):
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
        # Create a temporary directory with consecutive frame-numbered CSV files
        for i in range(1, 6):
            file_path = os.path.join(self.test_directory, f'frame_{i}.csv')
            with open(file_path, 'w') as file:
                pass

        with self.assertWarns(Warning):
            rrc.extract_and_check_consecutive_numbers(self.test_directory)


if __name__ == '__main__':
    unittest.main()
