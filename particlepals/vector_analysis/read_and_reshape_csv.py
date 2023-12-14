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
import warnings

from datetime import datetime
import pandas as pd
import numpy as np

try:
    import vector_analysis.vector_operations as vo
except ModuleNotFoundError:
    import vector_operations as vo

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

    Input:
    - file_path: The path to the CSV file.
    Output:
    - metadata: A dictionary containing metadata.
    Example usage:
    >>> file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames/metadata.csv'
    >>> metadata = extract_metadata_from_csv(file_path)
    >>> metadata = {'Sampling frequency': 3303.0, 
                    'Sampling units': 'Hz', 
                    'Number of samples per column': 1000, 
                    'Number of columns': 4, 
                    'Calibration status': True, 
                    'Spatial units': 'mm', 
                    'Parameter units': 'm/s', 
                    'Temporal units': 's'}
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
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")

    # Get a list of all files in the directory
    file_list = os.listdir(directory)

    # Check if there are CSV files in the directory
    csv_files = [file_name for file_name in file_list if file_name.lower().endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in the directory '{directory}'.")

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
    Input:
    - file_path: The path to the CSV file.
    Output:
    - x_positions: A 1D array containing x positions.
    - y_positions: A 1D array containing y positions.
    - u_velocities: A 1D array containing u velocities.
    - v_velocities: A 1D array containing v velocities.
    Example usage:
    >>> file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames/frame_1.csv'
    >>> x_positions, y_positions, u_velocities, v_velocities = read_csv_file(file_path)
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

def reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities):
    """
    The function reshapes the extracted data into a grid.
    Input:
    - x_positions: A 1D array containing x positions.
    - y_positions: A 1D array containing y positions.
    - u_velocities: A 1D array containing u velocities.
    - v_velocities: A 1D array containing v velocities.
    Output:
    - x_grid: A 2D array containing x positions.
    - y_grid: A 2D array containing y positions.
    - u_grid: A 2D array containing u velocities.
    - v_grid: A 2D array containing v velocities. 
    Example usage:
    >>> x_positions = [1, 2, 3, 1, 2, 3]
    >>> y_positions = [4, 4, 4, 5, 5, 5]
    >>> u_velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    >>> v_velocities = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
    >>> x_grid, y_grid, u_grid, v_grid = reshape_csv_file(
                x_positions, y_positions, u_velocities, v_velocities)
    """
    # Check if any of the input arrays are empty
    if len(x_positions) == 0 or len(y_positions) == 0 or len(u_velocities) == 0 or len(v_velocities) == 0:
        raise IndexError("Arrays x_positions, y_positions, u_velocities, v_velocities are empty.")

    try:
        # Create a grid using x and y positions
        x_grid, y_grid = np.meshgrid(np.unique(x_positions), np.unique(y_positions))
    except ValueError:
        # Raised if shapes of x_positions, y_positions are not compatible
        raise ValueError("Shapes of x_positions, y_positions are not compatible for reshaping into a grid.")

    # Reshape velocity components to match the grid
    u_grid = np.zeros_like(x_grid)
    v_grid = np.zeros_like(y_grid)

    for x, y, u, v in zip(x_positions, y_positions, u_velocities, v_velocities):
        try:
            # Find indices corresponding to x and y in the grid
            i = np.where(x_grid[0, :] == x)[0][0]
            j = np.where(y_grid[:, 0] == y)[0][0]
        except IndexError:
            # Raised if unable to find x or y in the grid
            raise IndexError("Unable to find x or y in the grid.")

        # Assign velocity components to the grid
        u_grid[j, i] = u
        v_grid[j, i] = v

    return x_grid, y_grid, u_grid, v_grid

def convert_grid_to_csv(x_grid, y_grid, u_grid, v_grid, file_path):
    """
    The function converts a grid to a CSV file and saves the CSV file in file_path.
    Input:
    - x_grid: A 2D array containing x positions.
    - y_grid: A 2D array containing y positions.
    - u_grid: A 2D array containing u velocities.
    - v_grid: A 2D array containing v velocities.
    - file_path: The path to the CSV file.
    Output:
    - None
    Example usage:
    >>> x_grid = np.array([[1, 2, 3], [1, 2, 3]])
    >>> y_grid = np.array([[4, 4, 4], [5, 5, 5]])
    >>> u_grid = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
    >>> v_grid = np.array([[1.1, 1.2, 1.3], [1.4, 1.5, 1.6]])
    >>> file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames'
    >>> convert_grid_to_csv(x_grid, y_grid, u_grid, v_grid, file_path)
    """
    
    # # Check if the folder exists
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError('The specified directory does not exist.')

    # Check if the grid shapes are compatible
    if x_grid.shape != y_grid.shape or x_grid.shape != u_grid.shape or x_grid.shape != v_grid.shape:
        raise ValueError('The grid shapes are not compatible.')

    # Check if the grid shapes are empty
    if x_grid.size == 0 or y_grid.size == 0 or u_grid.size == 0 or v_grid.size == 0:
        raise ValueError('The grid shapes are empty.')

    # Check if the grid shapes are 2D
    if len(x_grid.shape) != 2 or len(y_grid.shape) != 2 or len(u_grid.shape) != 2 or len(v_grid.shape) != 2:
        raise ValueError('The grid shapes are not 2D.')

    # Check if the grid shapes are not empty
    if x_grid.size == 0 or y_grid.size == 0 or u_grid.size == 0 or v_grid.size == 0:
        raise ValueError('The grid shapes are empty.')

    # Convert x_grid, y_grid, u_grid, v_grid to csv file
    # Flatten the 2D arrays to 1D arrays
    x_flat = x_grid.flatten()
    y_flat = y_grid.flatten()
    u_flat = u_grid.flatten()
    v_flat = v_grid.flatten()

    # Create a DataFrame with the flattened data
    data = {'x': x_flat, 'y': y_flat, 'u': u_flat, 'v': v_flat}
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    # print(f"Grid data saved to '{file_path}'.")

def process_csv_folder(folder_path, operation=None, vector=None):
    """
    The function processes all CSV files in a folder located in the original folder.
    It loads all the CSV files in the folder using the functions in 
    'read_and_reshape_csv'. It performs any processing that you want to do on 
    the data from functions in module 'vector_operations'. The user inputs 
    which vector operation to be performed.
    Analyze each frame and plot the processed frame at each step.

    The processed data is saved in a new folder located in the original folder.
    The name of the new folder is the same as the original folder with the 
    suffix '_processed_'and the date. The processed data is saved with the same name files. 
    It attaches a csv file with the metadata of the processed data.
    It also attaches a csv file with a list of the processes/operations performed on the data.

    Inputs:
        folder_path (str): Path to the folder containing the CSV files.
    Outputs:
        New folder with processed csv files, metadata, and list of operations performed.
    Examples:
        process_csv_folder(folder_path)
    """
    # Check if the input folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The specified folder '{folder_path}' does not exist.")

    numbers = extract_and_check_consecutive_numbers(folder_path)

    # Create a new folder for processed data
    processed_folder_name = f"{os.path.basename(folder_path)}_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    processed_folder_path = os.path.join(folder_path, processed_folder_name)
    os.makedirs(processed_folder_path)

    # Get a list of all CSV files in the input folder
    csv_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.csv')]

    # Process each CSV file
    for csv_file in csv_files:
        # Read and reshape CSV data
        file_path = os.path.join(folder_path, csv_file)
        # original_data = read_and_reshape_csv(file_path)
        # Read CSV file
        x_positions, y_positions, u_velocities, v_velocities = read_csv_file(file_path)
        # Reshape CSV file
        x_grid, y_grid, u_grid, v_grid = reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

        # Perform the specified vector operation
        if operation in {'add', 'subtract', 'multiply', 'divide'}:
            u_processed_data = vo.operate_on_grid(u_grid, vector=vector[0], operation=operation)
            v_processed_data = vo.operate_on_grid(v_grid, vector=vector[1], operation=operation)
        elif operation in {'mean', 'median'}:
            u_processed_data = vo.fill_in_nan_values_using_filter(u_grid, method=operation)
            v_processed_data = vo.fill_in_nan_values_using_filter(v_grid, method=operation)
        elif operation is None:
            # If operation is empty, don't process data
            pass
            # processed_data = original_data
        else:
            raise ValueError(f"Invalid operation '{operation}'. Valid operations are 'add', 'subtract', 'multiply', 'divide', 'mean', and 'median'.")
            

    if operation is not None:
        # Save metadata CSV file
        # metadata_file_path = os.path.join(processed_folder_path, 'metadata.csv')
        # metadata_df = pd.DataFrame({'ProcessedDate': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        #                             'OperationPerformed': [operation]})
        # metadata_df.to_csv(metadata_file_path, index=False)

        # Save list of operations performed CSV file
        operations_file_path = os.path.join(processed_folder_path, 'operations_performed.csv')
        operations_df = pd.DataFrame({'ProcessedDate': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                                        'Operation': [operation]})
        operations_df.to_csv(operations_file_path, index=False)

        # Save the processed data
        processed_file_path = os.path.join(processed_folder_path, csv_file)
        # processed_data.to_csv(processed_file_path, index=False)
        convert_grid_to_csv(x_grid, y_grid, u_processed_data, v_processed_data, processed_file_path)

        print(f"Processing complete. Processed data saved in '{processed_folder_path}'.")

    return u_processed_data, v_processed_data, numbers