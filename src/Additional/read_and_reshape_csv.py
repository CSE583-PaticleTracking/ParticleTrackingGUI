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
        metadata['Calibration status'] = metadata['Calibration status'].lower() == 'calibrated'
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
    print(f"Extracted Numbers: {numbers}")
    return numbers




