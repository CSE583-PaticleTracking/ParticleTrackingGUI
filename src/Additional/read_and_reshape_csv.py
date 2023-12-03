"""
read_csv_file is responsible for reading and extracting data from a single CSV file,
and reshape_csv_file takes the extracted data and reshapes it into a grid. The 
process_csv_folder function then processes all CSV files in a folder and returns 
a list of reshaped data for each file.

The metadata is stored in a dictionary, and the data is stored in NumPy arrays. 
The metadata should contain the following information:
- Sampling frequency (float)
- Sampling units (str) (Hz, frames per second)
- Number of samples (data rows) per column (int)
- Number of columns (int)
- Calibration status (bool) (calibrated = true or uncalibrated = flase)
- Spatial units (str) (e.g., mm, cm, m)
- Parameter units (str) (e.g., m/s, mm/s, cm/s)
- Temporal units (str) (e.g., s, ms, min, hr)

Check that the csv files are correctly formatted.
Check that the csv files do not contain empty spaces.
Check that the spatial coordinates do not contain NaN values.
Check that the metadata file exists and contains complete and correct information.
Check that frame numbers are consecutive and there are no gaps.
Check that the frame numbers are padded.
Check that there are frames in the folder.
Check that there are enough frames in the folder.
Check that there is enough information inside each file.
Check that the spatial grids make sense.
check that the spatial grids values and sizes are consistent across files.
"""
import os
import csv
import re
import pdb
import warnings
import numpy as np

def extract_metadata_from_csv(file_path):
    """
    Extract metadata from a CSV file and return it as a dictionary.
    Metadata is assumed to be in the comments at the beginning of the file.
    Example usage:
    csv_file_path = 'path/to/your/file.csv'
    metadata = extract_metadata_from_csv(csv_file_path)

    Print or use the extracted metadata as needed
    for key, value in metadata.items():
        print(f"{key}: {value}")
    """
    metadata = {}

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        # Read until a non-comment line is encountered
        for line in csv_reader:
            if not line[0].startswith('#'):
                break

            # Extract metadata from comments
            key_value = line[0][1:].strip().split(':')
            if len(key_value) == 2:
                key, value = key_value
                metadata[key.strip()] = value.strip()

    # Validate the metadata dictionary
    expected_keys = [
        'Sampling frequency',
        'Sampling units',
        'Number of samples per column',
        'Number of columns',
        'Calibration status',
        'Spatial units',
        'Parameter units',
        'Temporal units'
    ]

    for key in expected_keys:
        if key not in metadata:
            raise ValueError(f"Metadata key '{key}' is missing.")

    # Validate data types for specific keys
    try:
        metadata['Sampling frequency'] = float(metadata['Sampling frequency'])
        metadata['Number of samples per column'] = int(metadata['Number of samples per column'])
        metadata['Number of columns'] = int(metadata['Number of columns'])
        metadata['Calibration status'] = bool(metadata['Calibration status'])
    except ValueError as e:
        raise ValueError(f"Invalid data type for key: {str(e)}")

    return metadata


def extract_and_check_consecutive_numbers(directory):
    """
    Extracts numbers from CSV file names in the given directory and checks if the numbers are consecutive.

    Parameters:
    - directory (str): The path to the directory containing CSV files with frame numbers in their names.

    Raises:
    - Warning: If the extracted numbers are not consecutive or if there are missing numbers.

    Prints:
    - If the directory does not exist.
    - If no CSV files are found in the directory.
    - If no frame numbers are found in the file names.

    Example:
    >>> extract_and_check_consecutive_numbers('/path/to/your/directory')
    Extracted Numbers: [1, 2, 3, ...]

    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Get a list of all files in the directory
    file_list = os.listdir(directory)

    # Check if there are CSV files in the directory
    csv_files = [file_name for file_name in file_list if file_name.lower().endswith('.csv')]
    if not csv_files:
        print(f"No CSV files found in the directory '{directory}'.")
        return

    # Use a regular expression to extract numbers from file names
    pattern = re.compile(r'frame_(\d+)')

    # Extract numbers and check for consecutiveness
    numbers = []
    for file_name in csv_files:
        # Check if the file matches the pattern
        match = pattern.match(file_name)
        if match:
            extracted_number = int(match.group(1))
            numbers.append(extracted_number)

    # Check if the extracted numbers are consecutive
    if not numbers:
        print("No frame numbers found in the file names.")
        return

    start_number = min(numbers)
    expected_numbers = set(range(start_number, start_number + len(numbers)))
    actual_numbers = set(numbers)

    if expected_numbers != actual_numbers:
        warnings.warn("Warning: The extracted numbers are not consecutive or there are missing numbers.")

    # Print the extracted numbers
    # print(f"Extracted Numbers: {numbers}")
    return numbers

def read_csv_file(file_path):
    """
    The function reads a CSV file and extracts the x and y positions, and u and v velocities.
    This version should be more efficient for large CSV files as it takes advantage of the optimized 
    routines in NumPy and the csv module. The csv.reader is used only for reading metadata lines, and 
    np.loadtxt handles the numeric data efficiently.
    """

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError('The CSV file does not exist.')

    # Read CSV file using csv.reader for metadata and np.loadtxt for data
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        # Read until a non-comment line is encountered
        for line in csv_reader:
            if not line[0].startswith('#'):
                break

        # Use np.loadtxt to efficiently load numeric data
        try:
            # Use np.loadtxt to efficiently load numeric data
            data = np.loadtxt(file, delimiter=',', comments='#')

            # Check if the data is empty
            if data.size == 0:
                raise ValueError('The CSV file does not contain any data.')

        except UserWarning as e:
            # Handle the warning and raise a ValueError with a custom message
            raise ValueError(f'The CSV file is empty. {str(e)}')

        # Check if the data has the correct number of columns
        if data.shape[1] != 4:
            raise ValueError('The CSV file does not contain the correct number of columns.')

        # Check if the data has enough rows
        if data.shape[0] < 2:
            raise ValueError('The CSV file does not contain enough rows.')

    # Extract data columns
    x_positions = data[:, 0]
    y_positions = data[:, 1]
    u_velocities = data[:, 2]
    v_velocities = data[:, 3]

    # Check if either x_positions or y_positions have NaN values
    if np.isnan(x_positions).any() or np.isnan(y_positions).any():
        raise ValueError('The spatial coordinates contain NaN values.')

    # Check if either u_velocities or v_velocities have NaN values
    if np.isnan(u_velocities).any() or np.isnan(v_velocities).any():
        raise ValueError('The velocity components contain NaN values.') # This should be a warning instead of an error

    return x_positions, y_positions, u_velocities, v_velocities



