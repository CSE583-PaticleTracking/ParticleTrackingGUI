# Load the functions in read_and_reshape_csv.py into the playground.py file. 
import numpy as np
import csv
import os
import read_and_reshape_csv as rrc

# Create a test CSV file with metadata and data
test_file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/coding/Additional/turbulent_frames/metadata.csv'
test_metadata = {'Sampling frequency': 3303, 
                 'Sampling units': 'Hz', 
                 'Number of samples per column': 1000, 
                 'Number of columns': 4, 
                 'Calibration status': True,
                 'Spatial units': 'mm', 
                 'Parameter units': 'm/s', 
                 'Temporal units': 's'}

# rrc.add_metadata_to_csv(test_file_path, test_metadata)

# Create a test for extracting metadata from the CSV file
extracted_metadata = rrc.extract_metadata_from_csv(test_file_path)
print(extracted_metadata)













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