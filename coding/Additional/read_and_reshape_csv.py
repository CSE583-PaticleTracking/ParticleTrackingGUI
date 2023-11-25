"""
read_csv_file is responsible for reading and extracting data from a single CSV file,
and reshape_csv_file takes the extracted data and reshapes it into a grid. The 
process_csv_folder function then processes all CSV files in a folder and returns 
a list of reshaped data for each file.
"""
import os
import numpy as np

def read_csv_file(file_path):
    """
    The function reads a CSV file and extracts the x and y positions, and u and v velocities. 
    """
    # Read CSV file using numpy
    data = np.genfromtxt(file_path, delimiter=',', skip_header=1)

    # Extract data columns
    x_positions = data[:, 0]
    y_positions = data[:, 1]
    u_velocities = data[:, 2]
    v_velocities = data[:, 3]

    return x_positions, y_positions, u_velocities, v_velocities

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
folder_path = '/path/to/your/csv/files/'
reshaped_data_list = process_csv_folder(folder_path)

# Now, reshaped_data_list contains a list of tuples, each containing the reshaped data from one CSV file
