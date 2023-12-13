# Load the functions in read_and_reshape_csv.py into the playground.py file. 
import numpy as np
import csv
import os
from datetime import datetime
import pandas as pd
import read_and_reshape_csv as rrc
import vector_operations as vo

# Create a test CSV file with metadata and data
# test_file_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames/metadata.csv'
# test_metadata = {'Sampling frequency': 3303, 
#                  'Sampling units': 'Hz', 
#                  'Number of samples per column': 1000, 
#                  'Number of columns': 4, 
#                  'Calibration status': True,
#                  'Spatial units': 'mm', 
#                  'Parameter units': 'm/s', 
#                  'Temporal units': 's'}

# rrc.add_metadata_to_csv(test_file_path, test_metadata)

# Create a test for extracting metadata from the CSV file
# extracted_metadata = rrc.extract_metadata_from_csv(test_file_path)
# print(extracted_metadata)

# Create a test for extracting frame number from the CSV file
# directory_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames'
# rrc.extract_and_check_consecutive_numbers(directory_path)

# Create a test for reading the CSV file
# test_frame_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames/frame_1.csv'
# x_positions, y_positions, u_velocities, v_velocities = rrc.read_csv_file(test_frame_path)
# print(x_positions)
# print(y_positions)
# print(u_velocities)
# print(v_velocities)

# Create a test for reshaping the CSV file
# x_grid, y_grid, u_grid, v_grid = rrc.reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)
# print(x_grid)
# print(y_grid)
# print(u_grid)
# print(v_grid)

# # Create a test for operating on a grid
# # Create a grid
# grid = 2 * np.ones((2, 2))
# # Create a vector
# vector = 0 * np.ones((2, 2))
# # Specify the operation
# operation = 'divide'
# # Perform the operation on the grid
# result = vo.operate_on_grid(grid, vector, operation)
# print("Original Grid:")
# print(grid)
# print("\nVector:")
# print(vector)
# print("\nResult after {}ing the vector to the grid:".format(operation.capitalize()))
# print(result)

# # Create a test for calculating the magnitude and angle of a vector field
# # Create a grid
# grid = np.array([[np.nan, 0], [0, 1]])
# # Calculate the magnitude and angle of the vector field
# magnitude_grid, angle_grid = vo.calculate_magnitude_and_angle(grid, grid)
# print("Magnitude:")
# print(magnitude_grid)
# print("\nAngle:")
# print(angle_grid)

# Create test for filling in NaN values using filter
# Create a grid
# grid = np.array([[np.nan, 2, np.nan], [np.nan, np.nan, 6], [7, 8, 9]])
# grid = np.array([[1, 2, np.nan], [4, np.nan, 6], [7, 8, 9]])
# grid = np.array([[1, np.nan, 3], [4, 5, 6], [7, 8, 9]])
# print(grid.size)
# Specify the filter method
# methd = 'mean'
# Fill in NaN values using filter
# result = vo.fill_in_nan_values_using_filter(grid, methd)
# print("Original Grid:")
# print(grid)
# print("\nResult after filling in NaN values using {} filter:".format(methd))
# print(result)

def process_csv_folder(folder_path, operation=None):
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

    numbers = rrc.extract_and_check_consecutive_numbers(folder_path)

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
        x_positions, y_positions, u_velocities, v_velocities = rrc.read_csv_file(file_path)
        # Reshape CSV file
        x_grid, y_grid, u_grid, v_grid = rrc.reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

        # Perform the specified vector operation
        if operation in {'add', 'subtract', 'multiply', 'divide'}:
            u_processed_data = vo.operate_on_grid(u_grid, vector=2, operation=operation)
            v_processed_data = vo.operate_on_grid(v_grid, vector=2, operation=operation)
        elif operation in {'mean', 'median'}:
            u_processed_data = vo.fill_in_nan_values_using_filter(u_grid, method=operation)
            u_processed_data = vo.fill_in_nan_values_using_filter(u_grid, method=operation)
        elif operation is None:
            # If operation is empty, don't process data
            pass
            # processed_data = original_data
        else:
            raise ValueError(f"Invalid operation '{operation}'. Valid operations are 'add', 'subtract', 'multiply', 'divide', 'mean', and 'median'.")

        if operation is not None:
            # Save the processed data
            processed_file_path = os.path.join(processed_folder_path, csv_file)
            # processed_data.to_csv(processed_file_path, index=False)
            rrc.convert_grid_to_csv(x_grid, y_grid, u_processed_data, v_processed_data, processed_file_path)

    if operation is not None:
        # Save metadata CSV file
        metadata_file_path = os.path.join(processed_folder_path, 'metadata.csv')
        metadata_df = pd.DataFrame({'ProcessedDate': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                                    'OperationPerformed': [operation]})
        metadata_df.to_csv(metadata_file_path, index=False)

        # Save list of operations performed CSV file
        operations_file_path = os.path.join(processed_folder_path, 'operations_performed.csv')
        operations_df = pd.DataFrame({'Operation': [operation]})
        operations_df.to_csv(operations_file_path, index=False)

        print(f"Processing complete. Processed data saved in '{processed_folder_path}'.")
    


    # # Get a list of all files in the folder
    # all_files = os.listdir(folder_path)

    # # Filter out only CSV files
    # csv_files = [file for file in all_files if file.endswith('.csv')]

    # # Initialize empty lists to store reshaped data
    # reshaped_data_list = []

    # # Loop through each CSV file
    # for csv_file in csv_files:
    #     # Construct the full path to the CSV file
    #     file_path = os.path.join(folder_path, csv_file)

    #     # Read CSV file
    #     x_positions, y_positions, u_velocities, v_velocities = rrc.read_csv_file(file_path)

    #     # Reshape CSV file
    #     x_grid, y_grid, u_grid, v_grid = rrc.reshape_csv_file(x_positions, y_positions, u_velocities, v_velocities)

    #     # You can do more processing here
    #     # Get vector and operation from user
    #     operation = 'add'
    #     x_vector = 1 * np.ones((x_grid.shape[0], x_grid.shape[1]))
    #     y_vector = 0.5 * np.ones((y_grid.shape[0], y_grid.shape[1]))
    #     operate_result = vo.operate_on_grid(x_grid, x_vector, operation)
    #     operate_result = vo.operate_on_grid(y_grid, y_vector, operation)

    #     # Append reshaped data to the list
    #     reshaped_data_list.append((x_grid, y_grid, u_grid, v_grid))

    # return reshaped_data_list

# Example usage
# folder_path = '/Users/juliochavez/Desktop/cse583/ParticleTrackingGUI/src/Additional/turbulent_frames'
# reshaped_data_list = process_csv_folder(folder_path)

# Now, reshaped_data_list contains a list of tuples, each containing the reshaped data from one CSV file