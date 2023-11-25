"""
read_csv_file is responsible for reading and extracting data from a single CSV file,
and reshape_csv_file takes the extracted data and reshapes it into a grid. The 
process_csv_folder function then processes all CSV files in a folder and returns 
a list of reshaped data for each file.

The metadata is stored in a dictionary, and the data is stored in NumPy arrays. 
The metadata should contain the following information:
- Sampling frequency (Hz, frames per second)
- Number of samples (data rows) per column
- Number of columns 
- Frame number (frame_0000001, frame_0000002, etc.)
- Calibration status (calibrated = 1 or uncalibrated = 0)
- Spatial units (e.g., mm, cm, m)
- Parameter units (e.g., m/s, mm/s, cm/s)
- Temporal units (e.g., s, ms, min, hr)

Check that the csv files are correctly formatted and contain the correct frame number.
Check that the spatial coordinates do not contain NaN values.
Check that the metadata file exists and contains complete and correct information.
Check that there are frames in the folder.
Check that there are enough frames in the folder.
Check that there is enough information inside each file.
Check that the spatial grids make sense.
check that the spatial grids values and sizes are consistent across files.
"""
import os
import csv
import re
import numpy as np

def add_metadata_to_csv(file_path, metadata):
    """
    The function adds metadata to a CSV file.
    Example usage:
    csv_file_path = 'path/to/your/file.csv'
    metadata_to_add = {'Author': 'John Doe', 'Date': '2023-11-24', 'Description': 'This is a sample CSV file with metadata.'} 
    """
    # Read existing CSV data
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        lines = list(csv_reader)

    # Insert metadata at the beginning of the file
    lines.insert(0, ['# METADATA'] + [f'# {key}: {value}' for key, value in metadata.items()])

    # Write the modified data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(lines)

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

def process_csv_folder(folder_path):
    """
    The function processes all CSV files in a folder and returns a list of reshaped data for each file.
    """
    # Get a list of all files in the folder
    all_files = os.listdir(folder_path)

    # Filter out only CSV files
    csv_files = [file for file in all_files if file.endswith('.csv')]

    # Initialize empty lists to store reshaped data
    reshaped_data_list = []

    # Loop through each CSV file
    for csv_file in csv_files:
        # Construct the full path to the CSV file
        file_path = os.path.join(folder_path, csv_file)

        # Read CSV file
        x_positions, y_positions, u_velocities, v_velocities = read_csv_file(file_path)

        # Reshape CSV file
        x_grid, y_grid, u_grid, v_grid = reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

        # You can do more processing here

        # Append reshaped data to the list
        reshaped_data_list.append((x_grid, y_grid, u_grid, v_grid))

    return reshaped_data_list

# Example usage
# folder_path = '/path/to/your/csv/files/'
# reshaped_data_list = process_csv_folder(folder_path)

# Now, reshaped_data_list contains a list of tuples, each containing the reshaped data from one CSV file
