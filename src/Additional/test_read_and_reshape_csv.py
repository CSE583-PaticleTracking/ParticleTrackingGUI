import unittest
import tempfile
import shutil
import os
import numpy as np

class TestCSVProcessing(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for our test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_add_metadata_to_csv(self):
        test_file_path = os.path.join(self.test_dir, 'test.csv')
        test_metadata = {'Author': 'John Doe', 'Date': '2023-11-24', 'Description': 'This is a sample CSV file with metadata.'}

        # Create a test CSV file
        with open(test_file_path, 'w') as f:
            f.write('1,2,3,4\n5,6,7,8\n')

        # Add metadata to the CSV file
        add_metadata_to_csv(test_file_path, test_metadata)

        # Check if the metadata was correctly added
        with open(test_file_path, 'r') as f:
            lines = f.readlines()

        self.assertEqual(lines[0], '# METADATA\n')
        self.assertEqual(lines[1], '# Author: John Doe\n')
        self.assertEqual(lines[2], '# Date: 2023-11-24\n')
        self.assertEqual(lines[3], '# Description: This is a sample CSV file with metadata.\n')

    def test_extract_metadata_from_csv(self):
        test_file_path = os.path.join(self.test_dir, 'test.csv')
        test_metadata = {'Author': 'John Doe', 'Date': '2023-11-24', 'Description': 'This is a sample CSV file with metadata.'}

        # Create a test CSV file with metadata
        with open(test_file_path, 'w') as f:
            f.write('# METADATA\n')
            for key, value in test_metadata.items():
                f.write(f'# {key}: {value}\n')
            f.write('1,2,3,4\n5,6,7,8\n')

        # Extract metadata from the CSV file
        extracted_metadata = extract_metadata_from_csv(test_file_path)

        self.assertEqual(extracted_metadata, test_metadata)

    def test_extract_frame_number(self):
        test_file_name = 'data_frame_123.csv'
        frame_number = extract_frame_number(test_file_name)
        self.assertEqual(frame_number, 123)

    def test_read_csv_file(self):
        test_file_path = os.path.join(self.test_dir, 'test.csv')
        test_metadata = {'Author': 'John Doe', 'Date': '2023-11-24', 'Description': 'This is a sample CSV file with metadata.'}

        # Create a test CSV file with metadata and data
        with open(test_file_path, 'w') as f:
            f.write('# METADATA\n')
            for key, value in test_metadata.items():
                f.write(f'# {key}: {value}\n')
            f.write('1,2,3,4\n5,6,7,8\n')

        # Read CSV file
        metadata, x_positions, y_positions, u_velocities, v_velocities = read_csv_file(test_file_path)

        self.assertEqual(metadata, test_metadata)
        np.testing.assert_array_equal(x_positions, np.array([1, 5]))
        np.testing.assert_array_equal(y_positions, np.array([2, 6]))
        np.testing.assert_array_equal(u_velocities, np.array([3, 7]))
        np.testing.assert_array_equal(v_velocities, np.array([4, 8]))

    def test_reshape_csv_file(self):
        x_positions = np.array([1, 2, 1, 2])
        y_positions = np.array([1, 1, 2, 2])
        u_velocities = np.array([1, 2, 3, 4])
        v_velocities = np.array([5, 6, 7, 8])

        x_grid, y_grid, u_grid, v_grid = reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

        np.testing.assert_array_equal(x_grid, np.array([[1, 2], [1, 2]]))
        np.testing.assert_array_equal(y_grid, np.array([[1, 1], [2, 2]]))
        np.testing.assert_array_equal(u_grid, np.array([[1, 2], [3, 4]]))
        np.testing.assert_array_equal(v_grid, np.array([[5, 6], [7, 8]]))

if __name__ == '__main__':
    unittest.main()
