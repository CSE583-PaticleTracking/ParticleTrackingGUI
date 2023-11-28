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
- Frame number (int) (frame_0000001, frame_0000002, etc.)
- Calibration status (bool) (calibrated = 1 or uncalibrated = 0)
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

def add_metadata_to_csv(file_path, metadata):
    """
    Add or update metadata in a CSV file.
    If the file doesn't exist, create it and add the metadata.
    If the file already has metadata, update the values for existing keys.
    Check specific keys for correct values and types using exceptions.
    Ensure only required keys are present in the file.
    """
    # Check if the file exists
    file_exists = os.path.exists(file_path)

    # If the file exists, read the existing metadata
    existing_metadata = {}
    if file_exists:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            metadata_found = False
            #pdb.set_trace()
            for row in reader:
                if row and row[0].strip() == '# METADATA':
                    metadata_found = True
                    break
            if metadata_found:
                for row in reader:
                    #writer.writerow(['# METADATA']) # Write the METADATA header
                    if row and ':' in row[0]:
                        key, value = [item.strip() for item in row[0][1:].split(':', 1)]
                        existing_metadata[key] = value
                    #else:
                        #break
            else:
                # If no metadata found, create an empty dictionary
                existing_metadata = {}

                # Move the cursor to the end of the file to append new metadata
                file.seek(0, os.SEEK_END)

    # Update existing metadata or add new metadata
    for key, value in metadata.items():
        try:
            # Check if the key is required
            # if key not in existing_metadata:
                # raise KeyError(f"Key '{key}' is not present in the existing metadata.")
  
            # Check if the type of the value is correct
            # existing_type = type(existing_metadata[key])
            # if existing_type != type(value):
                # raise TypeError(f"Type mismatch for key '{key}': Expected {existing_type}, got {type(value)}.")

            # Update the value
            existing_metadata[key] = value
        except KeyError as key_error:
            print(f"Error: {key_error}")
        except TypeError as type_error:
            print(f"Error: {type_error}")

    # Write the updated metadata to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        if file_exists:
            writer.writerow(['# METADATA'])

        # If the file didn't exist, write the METADATA header
        if not file_exists:
            writer.writerow(['# METADATA'])

        # Write each key-value pair as a comment in the file
        for key, value in existing_metadata.items():
            writer.writerow([f'# {key} : {value}'])

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

    return metadata

def extract_frame_number(file_name):
    """
    Extract the frame number from a CSV file name.
    Assumes the frame number is present in the file name.
    Example usage:
    csv_file_name = 'data_frame_123.csv'
    frame_number = extract_frame_number(csv_file_name)

    if frame_number is not None:
        print(f"Frame Number: {frame_number}")
    else:
        print("Frame number not found in the file name.")
    """
    # Use regular expression to find the frame number in the file name
    match = re.search(r'\b\d+\b', file_name)

    if match:
        return int(match.group())
    else:
        # Handle the case when no frame number is found
        return None
    
def extract_and_check_consecutive_numbers(folder_path):
    """
    Extract frame numbers from CSV file names in a folder and check if they are consecutive.
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Check if there are CSV files in the folder
    csv_files = [file_name for file_name in file_list if file_name.lower().endswith('.csv')]
    if not csv_files:
        print(f"No CSV files found in the folder '{folder_path}'.")
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
    expected_numbers = set(range(1, max(numbers) + 1))
    actual_numbers = set(numbers)

    if expected_numbers != actual_numbers:
        warnings.warn("Warning: The frame numbers are not consecutive or there are missing frames.")

    # Print the results
    print(f"Extracted Numbers: {numbers}")


def read_csv_file(file_path):
    """
    The function reads a CSV file and extracts the metadata, x and y positions, and u and v velocities.
    This version should be more efficient for large CSV files as it takes advantage of the optimized 
    routines in NumPy and the csv module. The csv.reader is used only for reading metadata lines, and 
    np.loadtxt handles the numeric data efficiently.
    """
    # Initialize variables to store metadata and data
    metadata = {}

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
            # Extract metadata from comments
            key_value = line[0][1:].strip().split(':')
            if len(key_value) == 2:
                key, value = key_value
                metadata[key.strip()] = value.strip()

        # Use np.loadtxt to efficiently load numeric data
        data = np.loadtxt(file, delimiter=',', comments='#')

        # Check if the data is empty
        if data.size == 0:
            raise ValueError('The CSV file does not contain any data.')

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

    return metadata, x_positions, y_positions, u_velocities, v_velocities

def reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities):
    """
    The function reshapes the extracted data into a grid. 
    """
    # Create a grid using x and y positions
    x_grid, y_grid = np.meshgrid(np.unique(x_positions), np.unique(y_positions))

    # Reshape velocity components to match the grid
    u_grid = np.zeros_like(x_grid)
    v_grid = np.zeros_like(y_grid)

    for x, y, u, v in zip(x_positions, y_positions, u_velocities, v_velocities):
        # Find indices corresponding to x and y in the grid
        i = np.where(x_grid[0, :] == x)[0][0]
        j = np.where(y_grid[:, 0] == y)[0][0]

        # Assign velocity components to the grid
        u_grid[j, i] = u
        v_grid[j, i] = v

    return x_grid, y_grid, u_grid, v_grid


